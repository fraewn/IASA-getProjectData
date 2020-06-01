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
* setuptools 
* requests
* GitPython
* neo4j 
* psycopg2

### Build

1. Download the DependencyAnalysis.jar (request from admin) and copy .jar file into getrepository/control 

2. Start a new neo4j instance as project database and make sure it exists in global IASA project database 

3. Create postgreSQLconfig.ini in control package and add global database credentials (request from admin)

4. Run component: 
* In terminal, navigate to `getrepository/control`
* execute projectRestAPI.py with `python3 projectRestAPI.py` or create new run configuration for it
* create a project: `curl localhost:5000/createproject -d "project_id=1" -X POST`
* update a project: `curl localhost:5000/updateproject -d "project_id=1" -X POST`
* see project_id for a specific request `curl localhost:5000/request/<request_id>`



