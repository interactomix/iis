import unittest
import xml.etree.ElementTree as ET

from iis import create_app
from iis.util.process import XMLProcess, DataType, ProcessNotFoundError
from .base import BaseTestCase


class TestXMLProcess(BaseTestCase):
    def create_app(self):
        return create_app(self)

    def setUp(self):
        xml_process_description = """
        <processes>
          <process name="M-VORFFIP" id="mvorffip">
            <description>
              M-VORFFIP calculates things probably...
            </description>
            <outputs>
              <output>
                <type>functional_sites</type>
                <min>0</min>
                <max>-1</max>
              </output>
            </outputs>
            <inputs>
              <input>
                <type>structure</type>
                <min>1</min>
                <max>1</max>
              </input>
            </inputs>
            <post_set>
              <edge target="mvorffip">
              </edge>
            </post_set>
          </process>
        </processes>
        """

        self.process_graph = ET.ElementTree(
            element=ET.XML(xml_process_description)
        )

    def test_XMLProcess_instantiates_without_error(self):
        XMLProcess("mvorffip", self.process_graph)

    def test_XMLProcess_has_expected_properties(self):
        process = XMLProcess("mvorffip", self.process_graph)
        self.assertEqual(process.name, "M-VORFFIP")
        self.assertEqual(process.description.strip(),
                         "M-VORFFIP calculates things probably...")
        self.assertEqual(len(process.outputs), 1)
        self.assertEqual(len(process.inputs), 1)
        self.assertEqual(process.inputs[0][0], DataType.structure)
        self.assertEqual(process.outputs[0][0], DataType.default)
        self.assertEqual(process.inputs[0][1], 1)
        self.assertEqual(process.inputs[0][2], 1)
        self.assertEqual(process.outputs[0][1], 0)
        self.assertEqual(process.outputs[0][2], -1)
        self.assertEqual(len(process.post_set), 1)

    def test_returns_correct_post_set(self):
        process = XMLProcess("mvorffip", self.process_graph)
        self.assertEqual(len(process.list_next_nodes()), 1)
        self.assertEqual(process.list_next_nodes()[0], "mvorffip")

    def test_returns_correct_next_process(self):
        process = XMLProcess("mvorffip", self.process_graph)
        self.assertEqual(process._id, process.next_node("mvorffip")._id)

    def test_raises_exception_when_accessing_invalid_next_node(self):
        process = XMLProcess("mvorffip", self.process_graph)
        with self.assertRaises(ProcessNotFoundError):
            process.next_node("invalid")

if __name__ == '__main__':
    unittest.main()
