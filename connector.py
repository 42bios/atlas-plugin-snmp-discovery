import json
import os
from pathlib import Path
import runpy
import sys
config_path=Path(os.environ['ADDIN_CONFIG_FILE'])
config=json.loads(config_path.read_text())
credential=os.environ['ADDIN_CREDENTIAL_FILE']
os.environ['RUN_ONCE']='true'
sys.path.insert(0,str(Path(__file__).parent/'worker'))
targets=config['targets'].replace(',',' ').split()
import ipaddress
if not 1<=len(targets)<=16 or any(ipaddress.ip_network(t,strict=False).version!=4 for t in targets) or sum(ipaddress.ip_network(t,strict=False).num_addresses for t in targets)>1024:raise ValueError('Use up to 1024 IPv4 discovery addresses.')
path=config_path.parent/'discovery_config'
path.write_text(json.dumps({'targets':targets,'version':config.get('snmpVersion','2c')}));path.chmod(0o600)
os.environ.update(DISCOVERY_CONFIG_FILE=str(path),SNMP_COMMUNITY_FILE=credential,SNMP_CREDENTIALS_FILE=credential)
runpy.run_path(str(Path(__file__).parent/'worker/runtime.py'),run_name='__main__')
