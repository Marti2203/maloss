<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ast.proto

namespace Proto;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Generated from protobuf message <code>proto.SourceRange</code>
 */
class SourceRange extends \Google\Protobuf\Internal\Message
{
    /**
     * Generated from protobuf field <code>.proto.SourceLocation start = 1;</code>
     */
    private $start = null;
    /**
     * Generated from protobuf field <code>.proto.SourceLocation end = 2;</code>
     */
    private $end = null;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type \Proto\SourceLocation $start
     *     @type \Proto\SourceLocation $end
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Ast::initOnce();
        parent::__construct($data);
    }

    /**
     * Generated from protobuf field <code>.proto.SourceLocation start = 1;</code>
     * @return \Proto\SourceLocation
     */
    public function getStart()
    {
        return $this->start;
    }

    /**
     * Generated from protobuf field <code>.proto.SourceLocation start = 1;</code>
     * @param \Proto\SourceLocation $var
     * @return $this
     */
    public function setStart($var)
    {
        GPBUtil::checkMessage($var, \Proto\SourceLocation::class);
        $this->start = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>.proto.SourceLocation end = 2;</code>
     * @return \Proto\SourceLocation
     */
    public function getEnd()
    {
        return $this->end;
    }

    /**
     * Generated from protobuf field <code>.proto.SourceLocation end = 2;</code>
     * @param \Proto\SourceLocation $var
     * @return $this
     */
    public function setEnd($var)
    {
        GPBUtil::checkMessage($var, \Proto\SourceLocation::class);
        $this->end = $var;

        return $this;
    }

}

