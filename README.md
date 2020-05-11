#Abstract and Mock Class Helping Creator

##Requirement
* Python >=3.6
* PySide2/Qt >=5.14


## Purpose
From a .hpp or .h file, will create:
* The Interface of this Class, with the prefix desired
* The Mock of this Class, based on Google Mock
You can chose the desired prefix of the new class.
New class is saved in the folder selected as: ***Prefix**FileSelected.hpp*

**For Mock Class, you have to add th path to the Interface Class file.**

## Improvement
* Template return type are not supported yet
* If forward declaration of class in Interface Class File, it will appear in MockClass File

## How to use this tool
The tool is provided with a Graphical Interface. Two tabs are present:
* One to create Interface File
* One to create Mock File

For each tab there are two panels:
* Left panel : select your file and chose the Prefix and the destination folder
* Right panel : display the newly created file (Interface or Mock)