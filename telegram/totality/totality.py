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
    if not data.startswith("tgtotal-"):
        return

    hash = data[8:]
    endpoint = os.environ.get("TOTALITY_ENDPOINT")
    if not endpoint:
        print("Please use TOTALITY_ENDPOINT environment variable")
        return

    http = urllib3.PoolManager()
    r = http.request("GET", "%s/result/%s" % (endpoint, hash))
    if r.status != 200:
        print("Something went wrong: %s" % r.data)
        return
    
    data = json.loads(r.data)
    # validate data
    return data
    