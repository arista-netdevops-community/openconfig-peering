#!/bin/bash
rm -Rf yang
mkdir -p yang/consolidated
git clone https://github.com/openconfig/public.git yang/openconfig
git clone https://github.com/aristanetworks/yang.git yang/arista
cp yang/openconfig/release/models/*.yang yang/consolidated/
cp -R yang/openconfig/release/models/*/*.yang yang/consolidated/
cp yang/openconfig/third_party/ietf/*.yang yang/consolidated/
for i in `find yang/arista/EOS-4.26.1F/ -name 'arista*.yang'`; do cp $i yang/consolidated; done
source venv/bin/activate
MODULESPATH="`pwd`/venv/lib/python3/site-packages/"
PLUGINPATH="`pwd`/venv/lib/python3/site-packages/pyangbind/plugin/"
cd yang/consolidated
pyang --plugindir ${PLUGINPATH} -f pybind -o ${MODULESPATH}/openconfig_bgp.py openconfig-bgp.yang
pyang --plugindir ${PLUGINPATH} -f pybind -o ${MODULESPATH}/openconfig_interfaces.py openconfig-interfaces.yang openconfig-if-ip.yang arista-intf-augments.yang
pyang --plugindir ${PLUGINPATH} -f pybind -o ${MODULESPATH}/openconfig_routing_policy.py openconfig-routing-policy.yang
cd ../../