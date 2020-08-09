import json
import os
import datetime

from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA224, Hash

try:
    import telegram.vendor.ptb_urllib3.urllib3 as urllib3
except ImportError:
    import urllib3

class InlineTotalityButton(InlineKeyboardButton):

    def __init__(self, text, call, gasPrice, gasLimit, weiValue=0):
        if not hasattr(call, "abi") or not hasattr(call, "address") or not hasattr(call, "fn_name"):
            raise ValueError("Expecting contract call")

        InlineKeyboardButton.__init__(
            self,
            text
        )

        params = {}
        i = 0
        for input in call.abi["inputs"]:
            params[input["name"]] = call.arguments[i]
            i += 1

        self.data = json.dumps({
            "address": call.address,
            "function": call.fn_name,
            "params": params,
            "gasPrice": gasPrice,
            "gasLimit": gasLimit,
            "weiValue": weiValue,
            "abi": call.abi
        })

    def upload_call(self):
        endpoint = os.environ.get("TOTALITY_ENDPOINT")
        digest = Hash(SHA224(), backend=default_backend())
        digest.update(str.encode(self.data))
        digest.update(str.encode(str(datetime.datetime.utcnow().microsecond)))
        self.secret_hash = digest.finalize().hex()
        
        http = urllib3.PoolManager()
        r = http.request(
            "POST", "%s/call/%s" % (endpoint, self.secret_hash),
            headers={'Content-Type': 'application/json'},
            body=self.data
        )
        if r.status != 200:
            raise ValueError("Something went wrong")

    def to_dict(self):
        self.upload_call()
        self.callback_data = "tgtotal-%s" % self.secret_hash
        return InlineKeyboardButton.to_dict(self)