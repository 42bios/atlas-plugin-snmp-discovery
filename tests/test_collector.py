import importlib.util,json,os,tempfile,unittest,sys
from pathlib import Path
from unittest.mock import patch,MagicMock
PLUGIN=Path(__file__).resolve().parents[1]/'worker/collector.py'
def load(name):
 spec=importlib.util.spec_from_file_location(name,PLUGIN)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
class CollectorTests(unittest.TestCase):

    def test_snmp_scope_and_index_mapping(self):
        m = load('snmp')
        self.assertEqual(len(m.targets({'targets': ['192.0.2.0/30']})), 2)
        with self.assertRaises(ValueError):
            m.targets({'targets': ['192.0.0.0/16']})
        tables = {'description': {'101': 'uplink', '102': 'access'}, 'type': {'101': '6', '102': '6'}, 'name': {'101': 'Gi1', '102': 'Gi2'}, 'highSpeed': {'101': '10000'}, 'oper': {'101': '1', '102': '2'}, 'bridge': {'1': '101', '2': '102'}, 'pvid': {'2': '20'}, 'localPort': {'9': 'Gi1'}, 'neighborName': {'0.9.1': 'switch-b'}, 'neighborPort': {'0.9.1': 'Gi7'}, 'egress': {'0.30': 'C0'}, 'untagged': {'0.30': '40'}, 'fdb': {'0.1.2.3.4.5': '2'}}
        device = m.build_device('192.0.2.1', {'name': 'switch-a'}, tables, 'now')
        self.assertEqual(device['interfaces'][0]['speedMbps'], 10000)
        self.assertEqual(device['interfaces'][0]['observation']['neighbors'][0]['port'], 'Gi7')
        self.assertEqual(device['interfaces'][0]['taggedVlans'], [30])
        self.assertEqual(device['interfaces'][1]['nativeVlan'], 20)
        self.assertEqual(device['interfaces'][1]['observation']['learnedMacs'], ['00:01:02:03:04:05'])
        snap = m.collect(lambda a: {'name': 'test'}, lambda a, oid: tables.get(next((k for (k, v) in m.OIDS.items() if v == oid), '')), {'targets': ['192.0.2.1']}, 'test-snmp')
        self.assertEqual(snap['links'], [])
