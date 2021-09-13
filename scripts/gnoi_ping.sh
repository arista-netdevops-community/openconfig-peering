#!/bin/bash
grpcurl -H 'username: openconfig' -H 'password: openconfig' \
    -d '{"destination": "192.168.3.1", "count": 2, "do_not_resolve":true }' \
    -import-path ${GOPATH}/src \
    -proto github.com/openconfig/gnoi/system/system.proto \
    -plaintext \
    192.168.3.3:6030 gnoi.system.System/Ping