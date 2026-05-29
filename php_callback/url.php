<?php
$TOKEN = "HjBDovyST";
$ENCODING_AES_KEY = "3a4PlyTJLsKSMLRm28l60q3u1YqHmrsEQt7heyo7qPz";
$CORP_ID = "wwf3c53a68a102c7ca";
$AGENT_ID = "1000002";

class WXBizMsgCrypt {
    private $token;
    private $encodingAesKey;
    private $corpId;
    private $key;

    public function __construct($token, $encodingAesKey, $corpId) {
        $this->token = $token;
        $this->encodingAesKey = $encodingAesKey;
        $this->corpId = $corpId;
        $this->key = base64_decode($encodingAesKey . "=");
    }

    public function VerifyURL($msgSignature, $timestamp, $nonce, $echoStr) {
        $signature = $this->getSHA1($this->token, $timestamp, $nonce, $echoStr);
        if ($signature !== $msgSignature) {
            return array("errcode" => 40001, "errmsg" => "signature mismatch");
        }
        $result = $this->decrypt($echoStr);
        if ($result["errcode"] !== 0) {
            return $result;
        }
        return array("errcode" => 0, "plaintext" => $result["plaintext"]);
    }

    public function DecryptMsg($msgSignature, $timestamp, $nonce, $encrypted) {
        $signature = $this->getSHA1($this->token, $timestamp, $nonce, $encrypted);
        if ($signature !== $msgSignature) {
            return array("errcode" => 40001, "errmsg" => "signature mismatch");
        }
        $result = $this->decrypt($encrypted);
        if ($result["errcode"] !== 0) {
            return $result;
        }
        $xml = $result["plaintext"];
        preg_match('/<Content><!\[CDATA\[(.*?)\]\]><\/Content>/', $xml, $matches);
        $content = isset($matches[1]) ? $matches[1] : "";
        preg_match('/<FromUserName><!\[CDATA\[(.*?)\]\]><\/FromUserName>/', $xml, $m2);
        $fromUser = isset($m2[1]) ? $m2[1] : "";
        preg_match('/<MsgType><!\[CDATA\[(.*?)\]\]><\/MsgType>/', $xml, $m3);
        $msgType = isset($m3[1]) ? $m3[1] : "";
        preg_match('/<AgentID><!\[CDATA\[(.*?)\]\]><\/AgentID>/', $xml, $m4);
        $agentId = isset($m4[1]) ? $m4[1] : "";

        return array(
            "errcode" => 0,
            "content" => $content,
            "from_user" => $fromUser,
            "msg_type" => $msgType,
            "agent_id" => $agentId,
            "xml" => $xml
        );
    }

    public function EncryptMsg($replyMsg, $nonce, $timestamp = null) {
        if ($timestamp === null) {
            $timestamp = time();
        }
        $encrypt = $this->encrypt($replyMsg);
        if ($encrypt["errcode"] !== 0) {
            return $encrypt;
        }
        $encrypted = $encrypt["ciphertext"];
        $signature = $this->getSHA1($this->token, $timestamp, $nonce, $encrypted);
        $xml = "<xml>
<Encrypt><![CDATA[{$encrypted}]]></Encrypt>
<MsgSignature><![CDATA[{$signature}]]></MsgSignature>
<TimeStamp>{$timestamp}</TimeStamp>
<Nonce><![CDATA[{$nonce}]]></Nonce>
</xml>";
        return array("errcode" => 0, "encrypted_msg" => $xml);
    }

    private function getSHA1($token, $timestamp, $nonce, $encrypt) {
        $arr = array($token, $timestamp, $nonce, $encrypt);
        sort($arr, SORT_STRING);
        $str = implode("", $arr);
        return sha1($str);
    }

    private function decrypt($encrypted) {
        $iv = substr($this->key, 0, 16);
        $decrypted = openssl_decrypt(base64_decode($encrypted), "AES-256-CBC", $this->key, OPENSSL_RAW_DATA | OPENSSL_ZERO_PADDING, $iv);
        if ($decrypted === false) {
            return array("errcode" => 40002, "errmsg" => "AES decrypt failed");
        }
        $pad = ord(substr($decrypted, -1));
        if ($pad < 1 || $pad > 32) {
            $pad = 0;
        }
        $decrypted = substr($decrypted, 0, strlen($decrypted) - $pad);
        $content = substr($decrypted, 16);
        $lenBytes = substr($content, 0, 4);
        $len = unpack("N", $lenBytes)[1];
        $xmlContent = substr($content, 4, $len);
        $fromCorpId = substr($content, 4 + $len);
        if ($fromCorpId !== $this->corpId) {
            return array("errcode" => 40003, "errmsg" => "CorpID mismatch");
        }
        return array("errcode" => 0, "plaintext" => $xmlContent);
    }

    private function encrypt($text) {
        $random = $this->getRandomStr();
        $lenBytes = pack("N", strlen($text));
        $plaintext = $random . $lenBytes . $text . $this->corpId;
        $blockSize = 32;
        $textLen = strlen($plaintext);
        $padLen = $blockSize - ($textLen % $blockSize);
        if ($padLen === 0) {
            $padLen = $blockSize;
        }
        $plaintext .= str_repeat(chr($padLen), $padLen);
        $iv = substr($this->key, 0, 16);
        $ciphertext = openssl_encrypt($plaintext, "AES-256-CBC", $this->key, OPENSSL_RAW_DATA | OPENSSL_ZERO_PADDING, $iv);
        if ($ciphertext === false) {
            return array("errcode" => 40004, "errmsg" => "AES encrypt failed");
        }
        return array("errcode" => 0, "ciphertext" => base64_encode($ciphertext));
    }

    private function getRandomStr() {
        $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        $str = "";
        for ($i = 0; $i < 16; $i++) {
            $str .= $chars[random_int(0, strlen($chars) - 1)];
        }
        return $str;
    }
}

$crypt = new WXBizMsgCrypt($TOKEN, $ENCODING_AES_KEY, $CORP_ID);

if ($_SERVER["REQUEST_METHOD"] === "GET") {
    $msgSignature = $_GET["msg_signature"] ?? "";
    $timestamp = $_GET["timestamp"] ?? "";
    $nonce = $_GET["nonce"] ?? "";
    $echoStr = $_GET["echostr"] ?? "";

    $result = $crypt->VerifyURL($msgSignature, $timestamp, $nonce, $echoStr);
    if ($result["errcode"] !== 0) {
        http_response_code(403);
        echo "failed: " . $result["errmsg"];
        exit;
    }
    header("Content-Type: text/plain; charset=utf-8");
    echo $result["plaintext"];
    exit;
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $msgSignature = $_GET["msg_signature"] ?? "";
    $timestamp = $_GET["timestamp"] ?? "";
    $nonce = $_GET["nonce"] ?? "";
    $encrypted = file_get_contents("php://input");

    $xmlObj = simplexml_load_string($encrypted, "SimpleXMLElement", LIBXML_NOCDATA);
    if ($xmlObj === false) {
        echo "invalid xml";
        exit;
    }
    $encryptedMsg = (string)$xmlObj->Encrypt;

    $result = $crypt->DecryptMsg($msgSignature, $timestamp, $nonce, $encryptedMsg);
    if ($result["errcode"] !== 0) {
        echo "failed: " . $result["errmsg"];
        exit;
    }

    $msgType = $result["msg_type"];
    $fromUser = $result["from_user"];
    $content = $result["content"];

    if ($msgType === "text") {
        $replyContent = "已收到您的消息：" . $content;
        $replyXml = "<xml>
<ToUserName><![CDATA[{$fromUser}]]></ToUserName>
<FromUserName><![CDATA[{$CORP_ID}]]></FromUserName>
<CreateTime>" . time() . "</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{$replyContent}]]></Content>
<AgentID><![CDATA[{$AGENT_ID}]]></AgentID>
</xml>";
        $replyResult = $crypt->EncryptMsg($replyXml, $nonce, $timestamp);
        if ($replyResult["errcode"] === 0) {
            header("Content-Type: application/xml; charset=utf-8");
            echo $replyResult["encrypted_msg"];
        } else {
            echo "encrypt failed: " . $replyResult["errmsg"];
        }
    } else {
        echo "success";
    }
    exit;
}

echo "invalid request";
