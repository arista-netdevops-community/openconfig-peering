#!/bin/bash
../tools/gnmic/gnmic -a 192.168.3.3:6030 -u openconfig -p openconfig --insecure capabilities | grep bgp