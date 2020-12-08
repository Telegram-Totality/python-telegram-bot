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
    if canceled:
        return {"totality": True, "status": "CANCELED"}

    hash = data[8:]
    endpoint = os.environ.get("CUSTODIAL_ENDPOINT")
    http = urllib3.PoolManager()
    r = http.request("POST", "%s/tx/%s" % (endpoint, hash),
        headers={
            'Content-Type': 'application/json',
            'Authorization': os.environ.get("TOTALITY_SECRET"),
            'userid': update.effective_user.id
        },
        body=json.dumps(str(update.callback_query.from_user))
        )
    print(r.data)

    return {"totality": True, "status": "OK", "data": json.loads(r.data)}