import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
c=module('snmp_variants',ROOT/'worker/collector.py')
class Variations(unittest.TestCase):
 def device(self,**tables):
  return c.build_device('192.0.2.1',{},dict(description={'1':'port'},type={'1':'6'},**tables),'now')
 def test_empty_discovery_preserves_previous_inventory(self):
  with self.assertRaisesRegex(ValueError,'Previous inventory'):c.collect(lambda _:None,lambda *_:{},{'targets':['192.0.2.1']},'test')
 def test_failed_interface_query_aborts_discovery(self):
  with self.assertRaisesRegex(ValueError,'interface inventory failed'):c.collect(lambda _:{'name':'switch'},lambda *_:None,{'targets':['192.0.2.1']},'test')
 def test_saturated_speed_unknown_and_high_speed_preferred(self):
  self.assertNotIn('speedMbps',self.device(speed={'1':'4294967295'})['interfaces'][0])
  self.assertEqual(self.device(speed={'1':'4294967295'},highSpeed={'1':'25000'})['interfaces'][0]['speedMbps'],25000)
 def test_virtual_interfaces_not_physical_capacity(self):
  d=self.device(name={'1':'veth42'},connectorPresent={'1':'2'})
  self.assertEqual(d['ports'],0);self.assertEqual(d['interfaces'][0]['type'],'Virtual')
 def test_name_collision_unique(self):
  d=c.build_device('192.0.2.1',{},dict(description={'1':'a','2':'b','3':'c'},type={'1':'6','2':'6','3':'6'},name={'1':'Gi1-3','2':'Gi1','3':'Gi1'}),'now')
  self.assertEqual(len({i['name'] for i in d['interfaces']}),3)
 def test_unavailable_and_empty_tables_distinct(self):
  d=self.device(neighborName={})
  self.assertIn('neighborName',d['discovery']['emptyTables']);self.assertNotIn('neighborName',d['discovery']['unsupportedTables'])
  self.assertIn('neighborPort',d['discovery']['unsupportedTables'])
 def test_invalid_vlan_bitmap_does_not_invent_tagging(self):
  d=self.device(bridge={'1':'1'},egress={'0.10':'invalid'},untagged={'0.10':'00'})
  self.assertNotIn('taggedVlans',d['interfaces'][0])
 def test_duplicate_mac_observations_deduplicated(self):
  d=self.device(bridge={'1':'1'},qfdb={'10.0.1.2.3.4.5':'1','20.0.1.2.3.4.5':'1'})
  self.assertEqual(d['interfaces'][0]['observation']['learnedMacs'],['00:01:02:03:04:05'])
 def test_scope_overlap_and_point_to_point(self):
  self.assertEqual(c.targets({'targets':['192.0.2.0/31','192.0.2.1/32']}),['192.0.2.0','192.0.2.1'])

 def test_lldp_explicit_slot_port_description_maps_identity(self):
  d=self.device(name={'1':'0/28'},localPort={'9':'Port 28'},localPortDescription={'9':'Slot: 0 Port: 28 10G - Level'},neighborName={'0.9.1':'switch-b'},neighborPort={'0.9.1':'Port 31'})
  self.assertEqual(d['interfaces'][0]['observation']['neighbors'][0]['name'],'switch-b');self.assertEqual(d['discovery']['unmatchedNeighbors'],[])
 def test_unmapped_lldp_retained_without_guessing_ifindex(self):
  d=self.device(name={'1':'eth0'},localPort={'1':'Port 99'},neighborName={'0.1.1':'peer'})
  self.assertEqual(d['interfaces'][0]['observation']['neighbors'],[]);self.assertEqual(d['discovery']['unmatchedNeighbors'][0]['name'],'peer')
 def test_ambiguous_lldp_identity_not_assigned(self):
  d=c.build_device('192.0.2.1',{},dict(description={'1':'same','2':'same'},type={'1':'6','2':'6'},name={'1':'a','2':'b'},localPort={'9':'same'},neighborName={'0.9.1':'peer'}),'now')
  self.assertEqual(d['discovery']['unmatchedNeighbors'][0]['reason'],'ambiguous');self.assertTrue(all(not i['observation']['neighbors'] for i in d['interfaces']))
