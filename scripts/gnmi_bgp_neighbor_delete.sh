#!/bin/bash
gnmic -a 192.168.3.3:6030 -u openconfig -p openconfig set \
--delete \
'/network-instances/network-instance[name=default]/protocols/protocol[name=BGP]/bgp/neighbors/neighbor[neighbor-address=193.178.185.82]'
