import os
import json
import shutil
import logging
import requests
import tempfile
from xml.etree.ElementTree import fromstring, tostring
from os.path import join, exists, getsize, expanduser

from util.job_util import exec_command
from pm_proxy.pm_base import PackageManagerProxy


class JcenterProxy(PackageManagerProxy):
    def __init__(self, registry=None, cache_dir=None, isolate_pkg_info=False):
        super(JcenterProxy, self).__init__()
        self.registry = registry
        self.cache_dir = cache_dir
        self.isolate_pkg_info = isolate_pkg_info
        self.metadata_format = 'pom'
        self.dep_format = 'json'

    def _get_versions_info(self, pkg_name):
        gid, aid = pkg_name.split('/')
        try:
            # Maven URL for package information
            # https://repo1.maven.org/maven2/com/google/protobuf/protobuf-java/maven-metadata.xml
            versions_url = "http://jcenter.bintray.com/%s/%s/maven-metadata.xml" % (gid.replace('.', '/'), aid)
            versions_content = requests.request('GET', versions_url)
            # Parsing pom files
            # https://stackoverflow.com/questions/16802732/reading-maven-pom-xml-in-python
            return fromstring(versions_content.text)
        except:
            logging.error("fail to get latest version for pkg %s!", pkg_name)
            return None

    def _get_latest_version(self, pkg_name):
        versions_info = self._get_versions_info(pkg_name=pkg_name)
        if versions_info:
            return versions_info.find('./versioning/latest').text
        else:
            return None

    def _get_sanitized_version(self, pkg_name, pkg_version):
        if pkg_version is None:
            return self._get_latest_version(pkg_name=pkg_name)
        else:
            return pkg_version

    def _get_pkg_fname(self, pkg_name, pkg_version, suffix='jar'):
        _, aid = pkg_name.split('/')
        return '%s-%s.%s' % (aid, pkg_version, suffix)

    def _get_pkg_dir(self, pkg_name, pkg_version):
        gid, aid = pkg_name.split('/')
        return '%s/%s/%s' % (gid.replace('.', '/'), aid, pkg_version)

    def _get_pkg_path(self, pkg_name, pkg_version, suffix='jar'):
        return '%s/%s' % (self._get_pkg_dir(pkg_name=pkg_name, pkg_version=pkg_version),
                          self._get_pkg_fname(pkg_name=pkg_name, pkg_version=pkg_version, suffix=suffix))

    def download(self, pkg_name, pkg_version=None, outdir=None, binary=False, with_dep=False):
        # mvn dependency:get -DremoteRepositories=http://jcenter.bintray.com/ -Dartifact=com.google.protobuf:protobuf-java:3.5.1 -Dtransitive=false -Ddest=/tmp/
        pkg_version = self._get_sanitized_version(pkg_name=pkg_name, pkg_version=pkg_version)
        if binary:
            logging.warning("support for binary downloading is not added yet!")
        if with_dep:
            logging.warning("support for packing dependencies is not added yet!")
        possible_extensions = ('jar', 'aar', 'war')
        for extension in possible_extensions:
            # /tmp/protobuf-java-3.5.1.jar
            if extension != 'jar':
                download_artifact = '%s:%s:%s' % (pkg_name.replace('/', ':'), pkg_version, extension)
            else:
                download_artifact = '%s:%s' % (pkg_name.replace('/', ':'), pkg_version)
            download_cmd = ['mvn', 'dependency:get', '-DremoteRepositories=http://jcenter.bintray.com/',
                            '-Dartifact=%s' % download_artifact, '-Dtransitive=false', '-Ddest=%s' % outdir]
            exec_command('mvn dependency:get', download_cmd)
            # cleanup intermediate folders
            temp_install_path = expanduser(join('~/.m2/repository', self._get_pkg_dir(pkg_name=pkg_name, pkg_version=pkg_version)))
            shutil.rmtree(temp_install_path)
            # check if download path exists to see if the download is successful or not
            download_path = join(outdir, self._get_pkg_fname(pkg_name=pkg_name, pkg_version=pkg_version, suffix=extension))
            if exists(download_path):
                return download_path
        logging.error("failed to download pkg %s ver %s", pkg_name, pkg_version)
        return None

    def install(self, pkg_name, pkg_version=None, trace=False, trace_string_size=1024, install_dir=None, outdir=None,
                sudo=False):
        pass

    def install_file(self, infile, trace=False, trace_string_size=1024, sudo=False, install_dir=None, outdir=None):
        pass

    def uninstall(self, pkg_name, pkg_version=None, trace=False, trace_string_size=1024, sudo=False, install_dir=None,
                  outdir=None):
        pass

    def get_metadata(self, pkg_name, pkg_version=None):
        # load cached metadata information
        pkg_info_dir = self.get_pkg_info_dir(pkg_name=pkg_name)
        if pkg_info_dir is not None:
            metadata_fname = self.get_metadata_fname(pkg_name=pkg_name, pkg_version=pkg_version,
                                                     fmt=self.metadata_format)
            metadata_file = join(pkg_info_dir, metadata_fname)
            if exists(metadata_file):
                logging.warning("get_metadata: using cached metadata_file %s!", metadata_file)
                if self.metadata_format == 'pom':
                    return fromstring(open(metadata_file, 'r').read())
                else:
                    logging.error("get_metadata: output format %s is not supported!", self.metadata_format)
                    return None
        # Jcenter metadata is loaded in two steps.
        # First, load names and versions. Then load the latest/specified version
        try:
            # Jcenter URL for specific version
            # http://jcenter.bintray.com/com/google/protobuf/protobuf-java/3.6.1/protobuf-java-3.6.1.pom
            metadata_url = "http://jcenter.bintray.com/%s" % self._get_pkg_path(
                pkg_name=pkg_name, pkg_version=self._get_sanitized_version(pkg_name=pkg_name, pkg_version=pkg_version),
                suffix="pom")
            metadata_content = requests.request('GET', metadata_url)
            pkg_info = fromstring(metadata_content.text)
        except:
            logging.error("fail in get_metadata for pkg %s, ignoring!", pkg_name)
            return None
        if pkg_info_dir is not None:
            if not exists(pkg_info_dir):
                os.makedirs(pkg_info_dir)
            metadata_fname = self.get_metadata_fname(pkg_name=pkg_name, pkg_version=pkg_version,
                                                     fmt=self.metadata_format)
            metadata_file = join(pkg_info_dir, metadata_fname)
            if self.metadata_format == 'pom':
                open(metadata_file, 'w').write(metadata_content.text)
            else:
                logging.error("get_metadata: output format %s is not supported!", self.metadata_format)
        return pkg_info

    def get_versions(self, pkg_name, max_num=15, min_gap_days=30, with_time=False):
        # FIXME: the max_num and min_gap_days are not checked and enforced!
        # FIXME: the versions info is not cached
        # http://jcenter.bintray.com/com/google/protobuf/protobuf-java/maven-metadata.xml
        versions_info = self._get_versions_info(pkg_name=pkg_name)
        if versions_info is None:
            logging.error("fail to get versions_info for %s", pkg_name)
            return []
        return [ver.text for ver in versions_info.findall('./versioning/versions/version')]

    def get_author(self, pkg_name):
        pkg_info = self.get_metadata(pkg_name=pkg_name)
        if pkg_info is None:
            return {}
        groupid = pkg_name.split('/')[0]
        # developers
        # e.g. org.clojure..tools.logging, org.twitter4j..twitter4j
        # https://stackoverflow.com/questions/16802732/reading-maven-pom-xml-in-python
        nsmap = {'m': 'http://maven.apache.org/POM/4.0.0'}
        devs = pkg_info.findall('.//m:developer', nsmap)
        developers = []
        for dev in devs:
            dev_info = {}
            dev_id = dev.find('m:id', nsmap)
            if dev_id:
                dev_info['id'] = dev_id.text
            dev_name = dev.find('m:name', nsmap)
            if dev_name:
                dev_id['name'] = dev_name.text
            dev_email = dev.find('m:email', nsmap)
            if dev_email:
                dev_id['email'] = dev_email.text
            developers.append(dev_info)
        return {'groupid': groupid, 'developers': developers}

    def get_version_hash(self, pkg_name, pkg_version, algorithm='sha1'):
        if algorithm not in ('sha1', 'md5'):
            raise Exception("algorithm %s is not supported!", algorithm)
        temp_repo_dir = tempfile.mkdtemp(prefix='get_version_hash-')
        self.download(pkg_name=pkg_name, pkg_version=pkg_version, outdir=temp_repo_dir)
        possible_extensions = ('jar', 'aar', 'war')
        version_hash = None
        for extension in possible_extensions:
            temp_repo_filepath = join(temp_repo_dir, self._get_pkg_fname(pkg_name=pkg_name, pkg_version=pkg_version, suffix=extension))
            if not exists(temp_repo_filepath) or getsize(temp_repo_filepath) == 0:
                continue
            hash_command = '%ssum' % algorithm
            version_hash = exec_command(hash_command, [hash_command, temp_repo_filepath], ret_stdout=True)
            version_hash = version_hash.split(' ')[0]
            break
        shutil.rmtree(temp_repo_dir)
        if version_hash is None:
            logging.error("fail in get_version_hash for pkg %s ver %s, ignoring!", pkg_name, pkg_version)
            return None
        return version_hash

    def get_dep(self, pkg_name, pkg_version=None, flatten=False, cache_only=False):
        super(JcenterProxy, self).get_dep(pkg_name=pkg_name, pkg_version=pkg_version, flatten=flatten,
                                          cache_only=cache_only)
        raise Exception("not implemented yet! current version only deals with maven central and jar files!")
        # load cached dependency information
        pkg_info_dir = self.get_pkg_info_dir(pkg_name=pkg_name)
        if pkg_info_dir is not None:
            if flatten:
                dep_fname = self.get_flatten_dep_fname(pkg_name=pkg_name, pkg_version=pkg_version, fmt=self.dep_format)
            else:
                dep_fname = self.get_dep_fname(pkg_name=pkg_name, pkg_version=pkg_version, fmt=self.dep_format)
            dep_file = join(pkg_info_dir, dep_fname)
            if exists(dep_file):
                logging.warning("get_dep: using cached dep_file %s!", dep_file)
                if self.dep_format == 'json':
                    try:
                        return json.load(open(dep_file, 'r'))
                    except:
                        logging.debug("fail to load dep_file: %s, regenerating!", dep_file)
                else:
                    logging.error("get_dep: output format %s is not supported!", self.dep_format)
                    return None
        if cache_only:
            return None
        # use maven dependency to get the dependencies
        temp_repo_dir = tempfile.mkdtemp(prefix='get_dep-')
        # https://stackoverflow.com/questions/3342908/how-to-get-a-dependency-tree-for-an-artifact
        # http://maven.apache.org/plugins/maven-dependency-plugin/tree-mojo.html
        dep_pkgs = {}
        flatten_dep_pkgs = {}
        try:
            pom_filename = 'pom.xml'
            dep_tree_filename = 'dep_tree.txt'
            metadata_file = self.get_metadata_file(pkg_name=pkg_name, pkg_version=pkg_version)
            shutil.copy(metadata_file, join(temp_repo_dir, pom_filename))
            get_dep_cmd = ['mvn', 'dependency:tree', '-DoutputFile=%s' % dep_tree_filename, '-DoutputType=text']
            exec_command('mvn dependency:tree', get_dep_cmd, cwd=temp_repo_dir)
            dep_tree_file = join(temp_repo_dir, dep_tree_filename)
            for line in open(dep_tree_file, 'r'):
                line = line.strip('\n')
                if not line:
                    continue
                line_parts = line.split(' ')
                if len(line_parts) <= 1:
                    continue
                elif len(line_parts) == 2:
                    dep_pkg_info = line_parts[-1].split(':')
                    if len(dep_pkg_info) != 5:
                        logging.error("pkg %s has dependency with unexpected format: %s", pkg_name, line)
                    gid, aid, _, vid, dep_type = dep_pkg_info
                    # TODO: do we want compile dependency or test dependency (dep_type), currently recording both
                    dep_name = '%s/%s' % (gid, aid)
                    dep_pkgs[dep_name] = vid
                    flatten_dep_pkgs[dep_name] = vid
                else:
                    dep_pkg_info = line_parts[-1].split(':')
                    if len(dep_pkg_info) != 5:
                        logging.error("pkg %s has indirect dependency with unexpected format: %s", pkg_name, line)
                    gid, aid, _, vid, dep_type = dep_pkg_info
                    dep_name = '%s/%s' % (gid, aid)
                    flatten_dep_pkgs[dep_name] = vid
        except Exception as e:
            logging.error("failed while getting dependencies (%s) for pkg %s: %s!", flatten_dep_pkgs, pkg_name, str(e))
        logging.warning("%s has %d deps and %d flatten deps", pkg_name, len(dep_pkgs), len(flatten_dep_pkgs))
        if pkg_info_dir is not None:
            if not exists(pkg_info_dir):
                os.makedirs(pkg_info_dir)
            dep_fname = self.get_dep_fname(pkg_name=pkg_name, pkg_version=pkg_version, fmt=self.dep_format)
            dep_file = join(pkg_info_dir, dep_fname)
            flatten_dep_fname = self.get_flatten_dep_fname(pkg_name=pkg_name, pkg_version=pkg_version, fmt=self.dep_format)
            flatten_dep_file = join(pkg_info_dir, flatten_dep_fname)
            if self.dep_format == 'json':
                json.dump(dep_pkgs, open(dep_file, 'w'), indent=2)
                json.dump(flatten_dep_pkgs, open(flatten_dep_file, 'w'), indent=2)
            else:
                logging.error("get_dep: output format %s is not supported!", self.dep_format)
        # remove the repo directory
        shutil.rmtree(temp_repo_dir)
        return flatten_dep_pkgs if flatten else dep_pkgs
