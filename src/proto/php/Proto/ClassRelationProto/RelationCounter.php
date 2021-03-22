<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: class_sig.proto

namespace Proto\ClassRelationProto;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Generated from protobuf message <code>proto.ClassRelationProto.RelationCounter</code>
 */
class RelationCounter extends \Google\Protobuf\Internal\Message
{
    /**
     * Generated from protobuf field <code>.proto.ClassRelationProto.RelationType relation_type = 1;</code>
     */
    private $relation_type = 0;
    /**
     * Generated from protobuf field <code>int32 relation_count = 2;</code>
     */
    private $relation_count = 0;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type int $relation_type
     *     @type int $relation_count
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\ClassSig::initOnce();
        parent::__construct($data);
    }

    /**
     * Generated from protobuf field <code>.proto.ClassRelationProto.RelationType relation_type = 1;</code>
     * @return int
     */
    public function getRelationType()
    {
        return $this->relation_type;
    }

    /**
     * Generated from protobuf field <code>.proto.ClassRelationProto.RelationType relation_type = 1;</code>
     * @param int $var
     * @return $this
     */
    public function setRelationType($var)
    {
        GPBUtil::checkEnum($var, \Proto\ClassRelationProto_RelationType::class);
        $this->relation_type = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>int32 relation_count = 2;</code>
     * @return int
     */
    public function getRelationCount()
    {
        return $this->relation_count;
    }

    /**
     * Generated from protobuf field <code>int32 relation_count = 2;</code>
     * @param int $var
     * @return $this
     */
    public function setRelationCount($var)
    {
        GPBUtil::checkInt32($var);
        $this->relation_count = $var;

        return $this;
    }

}

// Adding a class alias for backwards compatibility with the previous class name.
class_alias(RelationCounter::class, \Proto\ClassRelationProto_RelationCounter::class);
