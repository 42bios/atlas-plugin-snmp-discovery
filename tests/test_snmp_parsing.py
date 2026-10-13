import importlib.util,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'worker'))
s=importlib.util.spec_from_file_location('snmp_parser_checks',ROOT/'worker/runtime.py');r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
class Parsing(unittest.TestCase):
 def test_unsupported_object_differs_from_empty_table(self):
  self.assertIsNone(r.parse('.1.2.3 = No Such Object available on this agent','1.2'))
  self.assertEqual(r.parse('.1.2.3 = No more variables left in this MIB View','1.2'),{})
 def test_numeric_enum_quoted_and_hex_values(self):
  self.assertEqual(r.parse('.1.2.1 = INTEGER: up(1)\n.1.2.2 = STRING: "Gi1"\n.1.2.3 = Hex-STRING: 00 01 02\n.1.3.1 = STRING: unrelated','1.2'),{'1':'1','2':'Gi1','3':'00 01 02'})
