# Structure

In order to make code reusable for a future GUI, and to make it easy to change
web interface if necessary, the code should be separated in to a distinct 
View and Controller package.  The view is the web application and the
controller is in effect a separate library.  At the interface the two will 
exchange input data and a 'Pipeline Definition File' in one direction, and the
output data in the other.

## Pipeline Definition File

This is the file that defines the order of processes in the pipeline, the type
of input data, the expected type of the output data and any modifications that
need to be made to the data between processes.  

For instance:  Process-1 produces a set of structures.  Process-2 expects a pair
of structures as input.  There are a number of ways to pass pairwise structures
to Process-2:  Execute Process-2 once for every pair of structures in the set, 
execute Process-2 once with the first two structures in the set, execute 
Process-2 once for every pair of structures such that each structure only 
occurs in one set.....

The syntax of this file or even the file type is not defined at this point.  XML
seems like a good candidate however.

## View

This is a web app written in python using Flask and co.  It will provide at
least two interfaces/ways of creating/selecting the definition files.  The first
will be a form driven interface where the user selects from a list of possible
processes based on the type of data that they have currently available.

The second will allow the user to select from a list of existing pipeline 
definitions or upload their own definition file.

## Controller

This will have to be a separate python package, however probably contained in 
the same repository.
