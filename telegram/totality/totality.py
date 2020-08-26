import os
import json
try:
    import telegram.vendor.ptb_urllib3.urllib3 as urllib3
except ImportError:
    import urllib3

def get_totality_data(update):
    if not update:
        return

    if not update.callback_query:
        return

    data = update.callback_query["data"]
    if not (data.startswith("tgtotdo-") or data.startswith("tgtotca-")):
        return
    canceled = data.startswith("tgtotca-")
    hash = data[8:]
    endpoint = os.environ.get("TOTALITY_ENDPOINT")
    http = urllib3.PoolManager()
    r = http.request("GET", "%s/result/%s" % (endpoint, hash))
    if r.status != 200:
        return {"canceled": canceled, "tx": None}
    return {"canceled": canceled, "tx": json.loads(r.data)}
