#!/bin/bash
../tools/gnmic/gnmic -a 192.168.3.3:6030 -u openconfig -p openconfig --insecure get \
--path \
'/network-instances/network-instance[name=default]/protocols/protocol[name=BGP]/bgp/neighbors/neighbor[neighbor-address=193.178.185.82]/state'
../tools/gnmic/gnmic -a 192.168.3.3:6030 -u openconfig -p openconfig --insecure get \
--path \
'/network-instances/network-instance[name=default]/protocols/protocol[name=BGP]/bgp/neighbors/neighbor[neighbor-address=193.178.185.82]/afi-safis/afi-safi[afi-safi-name=IPV4_UNICAST]'