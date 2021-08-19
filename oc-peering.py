import requests
import json
from pprint import pprint as pp
from openconfig_bgp import openconfig_bgp
from openconfig_routing_policy import openconfig_routing_policy
from openconfig_interfaces import openconfig_interfaces
import pyangbind.lib.pybindJSON as pybindJSON
import subprocess

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

fullCmd = "bgpq4 -4 -A -j -l temp {}".format(irr_as_set)
output = subprocess.check_output(fullCmd, shell=True)
bgpq = json.loads(output)

# prefix-list

oc = openconfig_routing_policy()
pfxname = str(asn) + 'v4'
oc.routing_policy.defined_sets.prefix_sets.prefix_set.add(pfxname)
for pfxlist in bgpq['temp']:
    oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].prefixes.prefix.add(ip_prefix=pfxlist['prefix'], masklength_range='exact')

with open("prefixlists.json", "w") as f:
    f.write(pybindJSON.dumps(oc.routing_policy, mode="ietf"))

# BGP section

oc = openconfig_bgp()

oc.bgp.neighbors.neighbor.add(ipaddr4)
oc.bgp.neighbors.neighbor[ipaddr4].config.neighbor_address=ipaddr4
oc.bgp.neighbors.neighbor[ipaddr4].config.enabled=True
oc.bgp.neighbors.neighbor[ipaddr4].config.peer_as=asn
oc.bgp.neighbors.neighbor[ipaddr4].config.description=name

oc.bgp.neighbors.neighbor.add(ipaddr6)
oc.bgp.neighbors.neighbor[ipaddr6].config.neighbor_address=ipaddr6
oc.bgp.neighbors.neighbor[ipaddr6].config.enabled=True
oc.bgp.neighbors.neighbor[ipaddr6].config.peer_as=asn
oc.bgp.neighbors.neighbor[ipaddr6].config.description=name
with open("bgp.json", "w") as f:
    f.write(pybindJSON.dumps(oc.bgp, mode="ietf"))

# interfaces

oc = openconfig_interfaces()
oc.interfaces.interface.add('Ethernet1')
oc.interfaces.interface['Ethernet1'].config.description = 'IXP Port'
oc.interfaces.interface['Ethernet1'].config.enabled = True
ip = "193.178.185.250"
prefix_length= "24"
oc.interfaces.interface['Ethernet1'].subinterfaces.subinterface.add(0)
#oc.interfaces.interface['Ethernet1'].subinterfaces.subinterface[0].ipv4.addresses.add(ip=ip,prefix_length=prefix_length)
oc.interfaces.interface['Ethernet1'].subinterfaces.subinterface[0].ipv4.addresses.config.ip=ip

with open("interfaces.json", "w") as f:
    f.write(pybindJSON.dumps(oc.interfaces, mode="ietf"))

