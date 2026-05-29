import sys
sys.path.append("weworkapi_python/callback")
from WXBizMsgCrypt import WXBizMsgCrypt
from flask import Flask, request
import os

app = Flask(__name__)

TOKEN = "HjBDovyST"
ENCODING_AES_KEY = "3a4PlyTJLsKSMLRm28l60q3u1YqHmrsEQt7heyo7qPz"
CORP_ID = "wwf3c53a68a102c7ca"

qy_api = WXBizMsgCrypt(TOKEN, ENCODING_AES_KEY, CORP_ID)

@app.route('/hook_path', methods=['GET', 'POST'])
def hook():
    if request.method == 'GET':
        msg_signature = request.args.get('msg_signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echo_str = request.args.get('echostr', '')
        ret, sEchoStr = qy_api.VerifyURL(msg_signature, timestamp, nonce, echo_str)
        if ret != 0:
            print(f"ERR: VerifyURL ret: {ret}")
            return "failed"
        return sEchoStr
    return "ok"

if __name__ == '__main__':
    port = 8066
    print(f"Starting callback server on port {port}...")
    app.run("0.0.0.0", port)
