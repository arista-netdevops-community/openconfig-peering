#!/bin/bash
gnmic -a 192.168.3.3:6030 -u openconfig -p openconfig set \
--update-path '/interfaces/' \
--update-file ../json/interface.json