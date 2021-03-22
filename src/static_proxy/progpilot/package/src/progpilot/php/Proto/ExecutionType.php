<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: behavior.proto

namespace Proto;

/**
 * Protobuf type <code>proto.ExecutionType</code>
 */
class ExecutionType
{
    /**
     * Install the package
     *
     * Generated from protobuf enum <code>INSTALL = 0;</code>
     */
    const INSTALL = 0;
    /**
     * Run the main binaries or executables of a package
     *
     * Generated from protobuf enum <code>MAIN = 1;</code>
     */
    const MAIN = 1;
    /**
     * Import and interact with a package
     *
     * Generated from protobuf enum <code>EXERCISE = 2;</code>
     */
    const EXERCISE = 2;
    /**
     * Run test script of a package
     *
     * Generated from protobuf enum <code>TEST = 3;</code>
     */
    const TEST = 3;
}
