<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: behavior.proto

namespace Proto;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Generated from protobuf message <code>proto.NetworkActivity</code>
 */
class NetworkActivity extends \Google\Protobuf\Internal\Message
{
    /**
     * Query domain or contact specific IPs
     *
     * Generated from protobuf field <code>string domain = 1;</code>
     */
    private $domain = '';
    /**
     * Generated from protobuf field <code>string url = 2;</code>
     */
    private $url = '';
    /**
     * Generated from protobuf field <code>string ip = 3;</code>
     */
    private $ip = '';
    /**
     * Generated from protobuf field <code>int32 port = 4;</code>
     */
    private $port = 0;
    /**
     * ICMP, UDP, TCP
     *
     * Generated from protobuf field <code>string protocol = 5;</code>
     */
    private $protocol = '';
    /**
     * Generated from protobuf field <code>string send_content = 6;</code>
     */
    private $send_content = '';
    /**
     * Generated from protobuf field <code>int32 send_content_size = 7;</code>
     */
    private $send_content_size = 0;
    /**
     * Generated from protobuf field <code>string receive_content = 8;</code>
     */
    private $receive_content = '';
    /**
     * Generated from protobuf field <code>int32 receive_content_size = 9;</code>
     */
    private $receive_content_size = 0;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type string $domain
     *           Query domain or contact specific IPs
     *     @type string $url
     *     @type string $ip
     *     @type int $port
     *     @type string $protocol
     *           ICMP, UDP, TCP
     *     @type string $send_content
     *     @type int $send_content_size
     *     @type string $receive_content
     *     @type int $receive_content_size
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Behavior::initOnce();
        parent::__construct($data);
    }

    /**
     * Query domain or contact specific IPs
     *
     * Generated from protobuf field <code>string domain = 1;</code>
     * @return string
     */
    public function getDomain()
    {
        return $this->domain;
    }

    /**
     * Query domain or contact specific IPs
     *
     * Generated from protobuf field <code>string domain = 1;</code>
     * @param string $var
     * @return $this
     */
    public function setDomain($var)
    {
        GPBUtil::checkString($var, True);
        $this->domain = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>string url = 2;</code>
     * @return string
     */
    public function getUrl()
    {
        return $this->url;
    }

    /**
     * Generated from protobuf field <code>string url = 2;</code>
     * @param string $var
     * @return $this
     */
    public function setUrl($var)
    {
        GPBUtil::checkString($var, True);
        $this->url = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>string ip = 3;</code>
     * @return string
     */
    public function getIp()
    {
        return $this->ip;
    }

    /**
     * Generated from protobuf field <code>string ip = 3;</code>
     * @param string $var
     * @return $this
     */
    public function setIp($var)
    {
        GPBUtil::checkString($var, True);
        $this->ip = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>int32 port = 4;</code>
     * @return int
     */
    public function getPort()
    {
        return $this->port;
    }

    /**
     * Generated from protobuf field <code>int32 port = 4;</code>
     * @param int $var
     * @return $this
     */
    public function setPort($var)
    {
        GPBUtil::checkInt32($var);
        $this->port = $var;

        return $this;
    }

    /**
     * ICMP, UDP, TCP
     *
     * Generated from protobuf field <code>string protocol = 5;</code>
     * @return string
     */
    public function getProtocol()
    {
        return $this->protocol;
    }

    /**
     * ICMP, UDP, TCP
     *
     * Generated from protobuf field <code>string protocol = 5;</code>
     * @param string $var
     * @return $this
     */
    public function setProtocol($var)
    {
        GPBUtil::checkString($var, True);
        $this->protocol = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>string send_content = 6;</code>
     * @return string
     */
    public function getSendContent()
    {
        return $this->send_content;
    }

    /**
     * Generated from protobuf field <code>string send_content = 6;</code>
     * @param string $var
     * @return $this
     */
    public function setSendContent($var)
    {
        GPBUtil::checkString($var, True);
        $this->send_content = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>int32 send_content_size = 7;</code>
     * @return int
     */
    public function getSendContentSize()
    {
        return $this->send_content_size;
    }

    /**
     * Generated from protobuf field <code>int32 send_content_size = 7;</code>
     * @param int $var
     * @return $this
     */
    public function setSendContentSize($var)
    {
        GPBUtil::checkInt32($var);
        $this->send_content_size = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>string receive_content = 8;</code>
     * @return string
     */
    public function getReceiveContent()
    {
        return $this->receive_content;
    }

    /**
     * Generated from protobuf field <code>string receive_content = 8;</code>
     * @param string $var
     * @return $this
     */
    public function setReceiveContent($var)
    {
        GPBUtil::checkString($var, True);
        $this->receive_content = $var;

        return $this;
    }

    /**
     * Generated from protobuf field <code>int32 receive_content_size = 9;</code>
     * @return int
     */
    public function getReceiveContentSize()
    {
        return $this->receive_content_size;
    }

    /**
     * Generated from protobuf field <code>int32 receive_content_size = 9;</code>
     * @param int $var
     * @return $this
     */
    public function setReceiveContentSize($var)
    {
        GPBUtil::checkInt32($var);
        $this->receive_content_size = $var;

        return $this;
    }

}

