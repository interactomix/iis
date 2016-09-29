# Process Graph

In order to construct an Interactomix pipeline, the user will be asked to 
answer a series of questions about her data and intentions.  Initially, they
will be asked about the kind of data that they have already.

At each subsequent step, they will be asked what their intentions are, based on
the data available at this step in the pipeline.  This continues until either 
there are no more possible processes to run, or the user decides finish here.

The processes form a graph, with a unique process at each node and a directed 
edge from process A to process B if process A produces output that can be used
by process B as input, with only minor modification.  

## Implementation

The graph will be implemented as a set of instances of a Node or Process class.  
Each instance will contain pointers to the instance to which it is connected by
a leaving edge, along with metadata if it is necessary.

### Base Class

The storage medium is unknown at this point.  Either DB entries or an XML file
seem sensible, but both have disadvantages.  To hide this, there will be an 
abstract base class (AbstractProcess) or similar.  The implementations of this
will read data from the relevant locations on demand.  There will be an instance
method that exposes the set of next processes. Additional metadata will also be
stored.
