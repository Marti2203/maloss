<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: module.proto

namespace Proto\ModuleTaintWrapper;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Generated from protobuf message <code>proto.ModuleTaintWrapper.TaintPoint</code>
 */
class TaintPoint extends \Google\Protobuf\Internal\Message
{
    /**
     * Generated from protobuf field <code>int32 id = 1;</code>
     */
    private $id = 0;
    /**
     * Generated from protobuf field <code>repeated string access_paths = 2;</code>
     */
    private $access_paths;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type int $id
     *     @type string[]|\Google\Protobuf\Internal\RepeatedField $access_paths
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Module::initOnce();
        parent::__construct($data);
    }

    /**
     * Generated from protobuf field <code>int32 id = 1;</code>
     * @return int
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Generated from protobuf field <code>int32 id = 1;</code>
     * @param int $var
     * @return $this
     */
    public function setId($var)
    {
        GPBUtil::checkInt32($var);
        $this->id = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>repeated string access_paths = 2;</code>
     * @return \Google\Protobuf\Internal\RepeatedField
     */
    public function getAccessPaths()
    {
        return $this->access_paths;
    }

    /**
     * Generated from protobuf field <code>repeated string access_paths = 2;</code>
     * @param string[]|\Google\Protobuf\Internal\RepeatedField $var
     * @return $this
     */
    public function setAccessPaths($var)
    {
        $arr = GPBUtil::checkRepeatedField($var, \Google\Protobuf\Internal\GPBType::STRING);
        $this->access_paths = $arr;

        return $this;
    }

}

// Adding a class alias for backwards compatibility with the previous class name.
class_alias(TaintPoint::class, \Proto\ModuleTaintWrapper_TaintPoint::class);

