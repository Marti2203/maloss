<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: module.proto

namespace Proto\ModuleTaintWrapper;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Generated from protobuf message <code>proto.ModuleTaintWrapper.TaintRule</code>
 */
class TaintRule extends \Google\Protobuf\Internal\Message
{
    /**
     * Generated from protobuf field <code>.proto.ModuleTaintWrapper.TaintPoint cause = 1;</code>
     */
    private $cause = null;
    /**
     * Generated from protobuf field <code>repeated .proto.ModuleTaintWrapper.TaintPoint effects = 2;</code>
     */
    private $effects;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type \Proto\ModuleTaintWrapper\TaintPoint $cause
     *     @type \Proto\ModuleTaintWrapper\TaintPoint[]|\Google\Protobuf\Internal\RepeatedField $effects
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Module::initOnce();
        parent::__construct($data);
    }

    /**
     * Generated from protobuf field <code>.proto.ModuleTaintWrapper.TaintPoint cause = 1;</code>
     * @return \Proto\ModuleTaintWrapper\TaintPoint
     */
    public function getCause()
    {
        return $this->cause;
    }

    /**
     * Generated from protobuf field <code>.proto.ModuleTaintWrapper.TaintPoint cause = 1;</code>
     * @param \Proto\ModuleTaintWrapper\TaintPoint $var
     * @return $this
     */
    public function setCause($var)
    {
        GPBUtil::checkMessage($var, \Proto\ModuleTaintWrapper_TaintPoint::class);
        $this->cause = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>repeated .proto.ModuleTaintWrapper.TaintPoint effects = 2;</code>
     * @return \Google\Protobuf\Internal\RepeatedField
     */
    public function getEffects()
    {
        return $this->effects;
    }

    /**
     * Generated from protobuf field <code>repeated .proto.ModuleTaintWrapper.TaintPoint effects = 2;</code>
     * @param \Proto\ModuleTaintWrapper\TaintPoint[]|\Google\Protobuf\Internal\RepeatedField $var
     * @return $this
     */
    public function setEffects($var)
    {
        $arr = GPBUtil::checkRepeatedField($var, \Google\Protobuf\Internal\GPBType::MESSAGE, \Proto\ModuleTaintWrapper\TaintPoint::class);
        $this->effects = $arr;

        return $this;
    }

}

// Adding a class alias for backwards compatibility with the previous class name.
class_alias(TaintRule::class, \Proto\ModuleTaintWrapper_TaintRule::class);

