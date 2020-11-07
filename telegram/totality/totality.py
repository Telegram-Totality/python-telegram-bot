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

    if not update.effective_user.address:
        return {"totality": True, "status": "NO_ADDRESS"}

    data = update.callback_query["data"]
    if not (data.startswith("tgtotdo-") or data.startswith("tgtotca-")):
        return
    canceled = data.startswith("tgtotca-")
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
    # handle response
    status = "OK"
    if canceled:
        status = "CANCELED"
    return {"totality": True, "status": canceled, "data": json.loads(r.data)}