#!/bin/bash
rm -Rf yang
mkdir -p yang/consolidated
git clone https://github.com/openconfig/public.git yang/openconfig
git clone https://github.com/aristanetworks/yang.git yang/arista
cp yang/openconfig/release/models/*.yang yang/consolidated/
cp -R yang/openconfig/release/models/*/*.yang yang/consolidated/
cp yang/openconfig/third_party/ietf/*.yang yang/consolidated/
for i in `find yang/arista/EOS-4.26.1F/ -name 'arista*.yang'`; do cp $i yang/consolidated; done

cd yang/consolidated
pyang --plugindir $HOME/project/persist/openconfig/venv/lib/python3.7/site-packages/pyangbind/plugin/ -f pybind -o $HOME/project/persist/openconfig/openconfig_bgp.py openconfig-bgp.yang
pyang --plugindir $HOME/project/persist/openconfig/venv/lib/python3.7/site-packages/pyangbind/plugin/ -f pybind -o $HOME/project/persist/openconfig/openconfig_interfaces.py openconfig-interfaces.yang openconfig-if-ip.yang arista-intf-augments.yang
pyang --plugindir $HOME/project/persist/openconfig/venv/lib/python3.7/site-packages/pyangbind/plugin/ -f pybind -o $HOME/project/persist/openconfig/openconfig_routing_policy.py openconfig-routing-policy.yang
cd ../../
