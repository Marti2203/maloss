#!/usr/bin/python3
import os
import ast
import sys
import logging
import argparse
from collections import Counter
from os.path import isdir, abspath, basename, dirname, relpath, join, isfile

sys.path.append("../")

import asttokens
import proto.python.ast_pb2 as ast_pb2
from util.job_util import read_proto_from_file, write_proto_to_file
from proto.python.ast_pb2 import PkgAstResults, AstLookupConfig, FileInfo, AstNode


class PythonDeclRefVisitor(ast.NodeVisitor):
    def __init__(self, asttok, configpb=None, debug=False):
        self.asttok = asttok
        self.debug = debug
        self.save_feature = configpb.save_feature if configpb else False
        self.func_only = configpb.func_only if configpb else False

        # initialize the declaration filters
        self.declrefs_filter_set = None
        if configpb is not None:
            self.declrefs_filter_set = set()
            for api in configpb.apis:
                if api.type == ast_pb2.AstNode.FUNCTION_DECL_REF_EXPR:
                    if self.func_only:
                        name_to_check = '.' + api.name if api.base_type else api.name
                        self.declrefs_filter_set.add(name_to_check)
                    else:
                        self.declrefs_filter_set.add(api.full_name)
        self.name2module = {}
        self.alias2name = {}
        # TODO: Module-based filter may reduce false positives, but can also introduce false negatives if not support cross file/module check.
        # the modules imported in the current file
        self.modules = set()
        # the collected declaration references
        self.declrefs = []

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        if self.debug:
            if hasattr(node, 'lineno'):
                logging.warning('visiting %s node at line %d', type(node).__name__, node.lineno)
            else:
                logging.warning('visiting %s node', type(node).__name__)

    def visit_ImportFrom(self, node):
        logging.debug('visiting ImportFrom node (line %d)', node.lineno)
        for name in node.names:
            self.name2module.setdefault(name.name, node.module)
            if name.asname is not None:
                self.alias2name.setdefault(name.asname, name.name)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        logging.debug('visiting FunctionDef node (line %d)', node.lineno)
        # FIXME: warn about redefined functions?
        if node.name in self.alias2name or node.name in self.name2module:
            logging.warning("redefined imported function %s!", node.name)
        ast.NodeVisitor.generic_visit(self, node)
        if self.save_feature:
            logging.warning("set root_nodes")

    def visit_ClassDef(self, node):
        logging.debug('visiting ClassDef node (line %d)', node.lineno)
        ast.NodeVisitor.generic_visit(self, node)
        if self.save_feature:
            logging.warning("set root_nodes")

    def visit_Call(self, node):
        logging.debug('visiting Call node (line %d)', node.lineno)

        # debug code
        if self.debug:
            for fieldname, value in ast.iter_fields(node):
                logging.warning('fieldname %s, value %s', fieldname, value)
                if fieldname == 'func':
                    for f_fieldname, f_value in ast.iter_fields(value):
                        logging.info('func fieldname %s, func value %s', f_fieldname, f_value)
                        if f_fieldname == 'id':
                            logging.warning('func id: %s', f_value)

        # compute base and func
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr

            if isinstance(node.func.value, ast.Name):
                base = node.func.value.id
            elif isinstance(node.func.value, ast.Call):
                base = self.asttok.get_text(node.func.value)
                logging.debug("node.func.value is ast.Call, Ignoring!")
            elif isinstance(node.func.value, ast.Subscript):
                base = self.asttok.get_text(node.func.value)
                # NOTE: currently, we use text of chained functions (i.e. foo().bar(), foo() is used),
                # because Python is runtime type language, and it is not possible to get the type statically
                logging.warning("node.func.value type ast.Subscript, fields: %s",
                                list(ast.iter_fields(node.func.value)))
            else:
                base = self.asttok.get_text(node.func.value)
                logging.error("node.func.value type: %s, fields: %s",
                              type(node.func.value), list(ast.iter_fields(node.func.value)))
        else:
            # NOTE: we assume the imported functions are not redefined! this may not be true!
            if isinstance(node.func, ast.Name):
                name = node.func.id
            else:
                name = self.asttok.get_text(node.func)
                logging.warning("node.func type: %s, name: %s", type(node.func), name)
            name = self.alias2name[name] if name in self.alias2name else name
            base = self.name2module[name] if name in self.name2module else None

        # compute arguments
        args = []
        for arg_index, arg_node in enumerate(node.args):
            args.append(self.asttok.get_text(arg_node))
        for keyword_index, keyword_node in enumerate(node.keywords):
            args.append(self.asttok.get_text(keyword_node))
        if hasattr(node, 'starargs') and node.starargs is not None:
            # append '*' to reproduce the calling text
            args.append('*' + self.asttok.get_text(node.starargs))
        if hasattr(node, 'kwargs') and node.kwargs is not None:
            # append '**' to reproduce the calling text
            args.append('**' + self.asttok.get_text(node.kwargs))

        # log stuff
        if base:
            logging.warning("calling function %s.%s with args %s at line %d", base, name, args, node.lineno)
        else:
            logging.warning("calling function %s with args %s at line %d", name, args, node.lineno)

        full_name = name if base is None else '%s.%s' % (base, name)
        source_text = self.asttok.get_text(node)
        source_range = (node.first_token.start, node.last_token.end)
        if self.func_only:
            name_to_check = '.' + name if base else name
        else:
            name_to_check = full_name
        if self.declrefs_filter_set is None or name_to_check in self.declrefs_filter_set:
            self.declrefs.append((base, name, tuple(args), source_text, source_range))
        ast.NodeVisitor.generic_visit(self, node)

    def get_declrefs(self):
        return self.declrefs


def get_infiles(inpath, root):
    infiles = []
    if isfile(inpath):
        if root is None:
            root = dirname(inpath)
        root = abspath(root)
        infiles.append(abspath(inpath))
    elif isdir(inpath):
        if root is None:
            root = inpath
        root = abspath(root)
        for i_root, _, i_files in os.walk(inpath):
            for fname in i_files:
                if fname.endswith(('.py',)):
                    infiles.append(abspath(join(i_root, fname)))
    if len(infiles) == 0:
        raise Exception("No input files from %s for language python3", inpath)
    return infiles, root


def get_filepb(infile, root):
    filepb = FileInfo()
    filepb.filename = basename(infile)
    filepb.relpath = relpath(dirname(infile), root)
    filepb.file = relpath(infile, root)
    filepb.directory = root
    return filepb


def get_api_result(base, name, args, source_text, source_range, filepb):
    api_result = AstNode()
    api_result.type = ast_pb2.AstNode.FUNCTION_DECL_REF_EXPR
    api_result.name = name
    if base is None:
        api_result.full_name = name
    else:
        api_result.base_type = base
        api_result.full_name = '%s.%s' % (base, name)
    for arg in args:
        api_result.arguments.append(arg)
    api_result.source = source_text
    source_start, source_end = source_range
    api_result.range.start.row = source_start[0]
    api_result.range.start.column = source_start[1]
    api_result.range.start.file_info.CopyFrom(filepb)
    api_result.range.end.row = source_end[0]
    api_result.range.end.column = source_end[1]
    api_result.range.end.file_info.CopyFrom(filepb)
    return api_result


def py3_astgen(inpath, outfile, configpb, root=None, pkg_name=None, pkg_version=None):
    # get input files
    infiles, root = get_infiles(inpath=inpath, root=root)

    # initialize resultpb
    resultpb = PkgAstResults()
    pkg = resultpb.pkgs.add()
    pkg.config.CopyFrom(configpb)
    pkg.pkg_name = pkg_name if pkg_name is not None else basename(inpath)
    if pkg_version is not None:
        pkg.pkg_version = pkg_version
    pkg.language = ast_pb2.PYTHON
    for infile in infiles:
        all_source = open(infile, 'r').read()
        try:
            tree = ast.parse(all_source, filename=infile)
        except SyntaxError as se:
            logging.warning("Syntax error %s parsing file %s in python2!", se, infile)
            raise se
        # mark the tree with tokens information
        asttok = asttokens.ASTTokens(source_text=all_source, tree=tree, filename=infile)
        visitor = PythonDeclRefVisitor(asttok=asttok, configpb=configpb)
        visitor.visit(tree)
        logging.warning("collected functions: %s", Counter(visitor.get_declrefs()).items())

        filepb = get_filepb(infile, root)
        for base, name, args, source_text, source_range in visitor.get_declrefs():
            api_result = get_api_result(base, name, args, source_text, source_range, filepb)
            pkg.api_results.add().CopyFrom(api_result)

    # save resultpb
    write_proto_to_file(resultpb, outfile, binary=False)


def parse_args(argv):
    parser = argparse.ArgumentParser(prog="astgen_py3", description="Parse arguments")
    parser.add_argument("inpath", help="Path to the input directory or file")
    parser.add_argument("outfile", help="Path to the output file.")
    parser.add_argument("-b", "--root", dest="root", help="Path to the root of the source.")
    parser.add_argument("-n", "--package_name", dest="package_name", help="Package name of the specified input.")
    parser.add_argument("-v", "--package_version", dest="package_version",
                        help="Package version of the specified input.")
    parser.add_argument("-c", "--configpath", dest="configpath",
            help="Optional path to the filter of nodes, stored in proto buffer format (AstLookupConfig in ast.proto).")
    return parser.parse_args(argv)


if __name__ == "__main__":
    # Parse options
    args = parse_args(sys.argv[1:])

    # Load config pb
    configpath = args.configpath
    configpb = AstLookupConfig()
    read_proto_from_file(configpb, configpath, binary=False)
    logging.debug("loaded lookup config from %s:\n%s", configpath, configpb)

    # Run the ast generation
    py3_astgen(inpath=args.inpath, outfile=args.outfile, configpb=configpb, root=args.root, pkg_name=args.package_name,
               pkg_version=args.package_version)

