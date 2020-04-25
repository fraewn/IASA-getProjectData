# READ ME

## Watch showcase here
https://drive.google.com/file/d/1AOkofseiU2wcuxEFpzoA6HyAOxmpcwXv/view?usp=sharing

## Installation 

### Requirements
* python 3.7+ 64bit
* neo4j local instance (docker is sufficient)
* pip 

Install the following libs using pip3: 
* pydriller 
* PyQt5 
* setuptools 
* requests
* GitPython
* neo4j 
* psycopg2

### Build

1. Download the DependencyAnalysis.jar from here: 
https://drive.google.com/file/d/1frkG5Is0tKjcHzf10R49ioDxV6uSCkjn/view?usp=sharing
and copy .jar file into getrepository/control 

2. Start new neo4j instance as project database

3. Add project database credentials in getrepository/service/util/credentials.py 

4. Add global database credentials in getrepository/service/globalDatabaseAccess.py

5. Run Program: 

Option 1:
* In terminal, navigate to getrepository/control
* execute GUI.py with `python3 GUI.py` 

Option 2: 
* create new python run configuration
* path: getrepository/control
* execute 

!!! IMPORTANT: After each execution, delete folder 'dependency_analysis' in:
* LOCALAPPDATA (if your_os=windows)
* HOME (if your_os=unix based)

