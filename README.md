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

1. Download the DependencyAnalysis.jar (request from admin) and copy .jar file into getrepository/control 

2. Start a new neo4j instance as project database and make sure it exists in global database 

3. Create postgreSQLconfig.ini in control package and add global database credentials (request from admin)

4. Run Program: 

Option 1 (REST API) - recommended: 
* In terminal, navigate to `getrepository/control`
* execute projectRestAPI.py with `python3 projectRestAPI.py` or create new run configuration for it
* add a project using POST-method: `curl localhost:5000/projects -d "project_id=1" -X POST`

Option 2 (GUI):
* In terminal, navigate to `getrepository/control`
* execute GUI.py with `python3 GUI.py` or create new run configuration for it 
* enter project_id (see global database for projects)



