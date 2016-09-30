"""
Define classes and methods for manipulating the process graph.

Classes
=======
AbstractProcess - Abstract base class for the processes (nodes).
XMLProcess - Represent a node stored in an XML file

Enums
=====
DataType - The type of input or output data.

Exceptions
==========
ProcessNotFoundError - This is raised when an attempt is made to access
                       a process that doesn't exist or isn't in the
                       postset of another process.
"""
from typing import List, Tuple
import abc
from xml.etree.ElementTree import ElementTree
from enum import Enum


class AbstractProcess():
    """Encapsulates the behaviour of the Process Graph Nodes."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def next_node(self: "AbstractProcess", ident: str) -> "AbstractProcess":
        """Return the connected node belonging to the identifier"""
        pass

    @abc.abstractmethod
    def list_next_nodes(self: "AbstractProcess") -> List[str]:
        """Returns a list containing information about next nodes"""
        pass


class XMLProcess(AbstractProcess):
    """XML implementation of AbstractProcess."""
    def __init__(self: "XMLProcess", process: str,
                 tree: ElementTree) -> None:
        """Initilizes a process from an XML element."""
        element = tree.find(".//process[@id='" + process + "']")
        self._tree = tree
        self._id = element.attrib["id"]
        self.name = element.attrib["name"]
        self.description = element.find("description").text

        InOutputType = List[Tuple[DataType, int, int]]  # noqa: F841
        outputs = element.findall(".//output")
        self.outputs = []  # type: InOutputType
        for output in outputs:
            try:
                output_type = DataType(output.find("type").text)
            except ValueError:
                output_type = DataType.default

            n_output_min = int(output.find("min").text)
            n_output_max = int(output.find("max").text)
            self.outputs.append((output_type, n_output_min, n_output_max))

        inputs = element.findall(".//input")
        self.inputs = []  # type: InOutputType
        for in_put in inputs:
            try:
                input_type = DataType(in_put.find("type").text)
            except ValueError:
                input_type = DataType.default

            n_input_min = int(in_put.find("min").text)
            n_input_max = int(in_put.find("max").text)
            self.inputs.append((input_type, n_input_min, n_input_max))

        self.post_set = []  # type: List[Dict[str, str]]
        for edge in element.find("post_set"):
            post_node = {
                "target": (edge.attrib["target"]
                           if not isinstance(edge.attrib["target"], bytes) else
                           edge.attrib["target"].decode('utf-8')),
            }

            self.post_set.append(post_node)

    def next_node(self: "XMLProcess", ident: str) -> "AbstractProcess":
        """Return the process in the postset with id == ident

        Throw an ProcessNotFoundError if there is no process with
        id == ident in the postset.
        """
        found = False
        for node in self.post_set:
            if node["target"] == ident:
                found = True
                break

        if not found:
            raise ProcessNotFoundError("This process does not have the "
                                       "process with id:'" + ident +
                                       "' in its postset.")

        return XMLProcess(ident, self._tree)

    def list_next_nodes(self) -> List[str]:
        """List the ids of all nodes in the postset"""
        ret = []
        for node in self.post_set:
            ret.append(node["target"])

        return ret


class DataType(Enum):
    structure = "structure"
    sequence = "sequence"
    default = "default"


class ProcessNotFoundError(ValueError):
    """An error associated with accessing a non existent process."""
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(self, msg)

    def __repr__(self) -> str:
        return self.msg
