import requests
import json
from pprint import pprint as pp
url = "https://www.peeringdb.com/api/net?asn=44194&depth=2&="

payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

data = json.loads(response.text)
name = data['data'][0]['name']
irr_as_set = data['data'][0]['irr_as_set']
for i in data['data'][0]['netixlan_set']:
    if i['ix_id'] == 87:
        asn = i['asn']
        ipaddr4 = i['ipaddr4']
        ipaddr6 = i['ipaddr6']
print (name)
print(f"ASN: {asn} \nIPV4: {ipaddr4} \nIPV6:{ipaddr6}")

