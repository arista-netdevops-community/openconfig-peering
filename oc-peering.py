import requests
import json
from pprint import pprint as pp
from openconfig_bgp import openconfig_bgp
from openconfig_routing_policy import openconfig_routing_policy
from openconfig_interfaces import openconfig_interfaces
import pyangbind.lib.pybindJSON as pybindJSON
import subprocess

#####################
## Peer information from PeeringDB
#####################
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
print(f"ASN: {asn} \nIPv4: {ipaddr4} \nIPv6: {ipaddr6}")

#####################
## Prefix list from IRR
#####################
fullCmd4 = "~/project/persist/bgpq4/bgpq4 -4 -A -j -l temp {}".format(irr_as_set)
fullCmd6 = "~/project/persist/bgpq4/bgpq4 -6 -A -j -l temp {}".format(irr_as_set)
output4 = subprocess.check_output(fullCmd4, shell=True)
bgpq4 = json.loads(output4)
output6 = subprocess.check_output(fullCmd6, shell=True)
bgpq6 = json.loads(output6)

#####################
## Generate OpenConfig interface config
#####################
interface = "Ethernet1"
ipv4 = "193.178.185.250"
ipv4_prefix_length = 24
ipv6 = "2001:7f8:19:1::250:1"
ipv6_prefix_length = 64

oc = openconfig_interfaces()
oc.interfaces.interface.add(interface)
oc.interfaces.interface[interface].config.description = 'IXP Port'
oc.interfaces.interface[interface].config.enabled = True

oc.interfaces.interface[interface].subinterfaces.subinterface.add(0)
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv4.addresses.address.add(ip=ipv4)
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv4.config.enabled = True
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv4.addresses.address[ipv4].config.ip = ipv4
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv4.addresses.address[ipv4].config.prefix_length = ipv4_prefix_length
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv4.addresses.address[ipv4].config.addr_type = 'PRIMARY'
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv6.addresses.address.add(ip=ipv6)
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv6.config.enabled = True
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv6.addresses.address[ipv6].config.ip = ipv6
oc.interfaces.interface[interface].subinterfaces.subinterface[0].ipv6.addresses.address[ipv6].config.prefix_length = ipv6_prefix_length

with open("interfaces.json", "w") as f:
    f.write(pybindJSON.dumps(oc.interfaces, mode="ietf"))

#####################
## Generate OpenConfig prefix-lists
#####################
oc = openconfig_routing_policy()
pfxname = 'AS' + str(asn) + '-v4'
oc.routing_policy.defined_sets.prefix_sets.prefix_set.add(pfxname)
oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].config.name = pfxname
for pfxlist in bgpq4['temp']:
    print(f"prefix: {pfxlist['prefix']}")    
    oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].prefixes.prefix.add(ip_prefix=pfxlist['prefix'], masklength_range='exact')
    #print(oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].prefixes.prefix[(pfxlist['prefix'], 'exact')].keys)
    #print(oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].prefixes.prefix[(pfxlist['prefix'], 'exact')].keys)
    #oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].prefixes.prefix[ip_prefix==pfxlist['prefix'], masklength_range=='exact'].config.ip_prefix=pfxlist['prefix']
    #oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].prefixes.prefix[pfxlist['prefix']].config.masklength_range='exact'

pfxname = 'AS' + str(asn) + '-v6'
oc.routing_policy.defined_sets.prefix_sets.prefix_set.add(pfxname)
oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].config.name = pfxname
for pfxlist in bgpq6['temp']:
    oc.routing_policy.defined_sets.prefix_sets.prefix_set[pfxname].prefixes.prefix.add(ip_prefix=pfxlist['prefix'], masklength_range='exact')

with open("prefixlists.json", "w") as f:
    f.write(pybindJSON.dumps(oc.routing_policy, mode="ietf"))

#####################
## Generate OpenConfig BGP neighbor config
#####################
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

