import unittest
import xml.etree.ElementTree as ET

import flask_testing

from app import create_app
from app.util.process import XMLProcess


class TestXMLProcess(flask_testing.TestCase):
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


if __name__ == '__main__':
    unittest.main()
