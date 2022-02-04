import urllib.request
import json

API_url = "http://api.exchangeratesapi.io/v1/latest?access_key=b8332a67e8775b84556eb418874799cf&base=EUR&symbols=CNY,GBP,JPY,USD"

result = urllib.request.urlopen(API_url).read()

json_result = json.loads(result)
print(json_result)


