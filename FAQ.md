# FAQ 

## Error Messages 
#### Error message in GUI: "No Permission on given Git Repository! Please check again!"
* check if you deleted the dependency_analysis folder in HOME (unix) or LOCALAPPDATA (windows) before reexecuting

#### Execution stops at 60% mark 
* something with your database connection seems wrong
* check if the credentials to your database are correct in service/util/credentials.py
* if you are using neo4j version 4.0 or higher, change 
`self._driver  = GraphDatabase.driver(uri, auth=(user, password))`
in class DatabaseAccess.py to 
`self._driver = GraphDatabase.driver(uri, auth=(user,password), encrypted=false)`
* if you are using a database from school, check if your vpn connection is sufficient

#### Error message in terminal: cannot find dependencyAnalysis.jar
* download .jar file here: https://drive.google.com/file/d/1frkG5Is0tKjcHzf10R49ioDxV6uSCkjn/view?usp=sharing
* copy it into control package
* make sure you are executing from a path where .jar is visible e.g. from `getrepository/control`

#### Error message while installing psycopg2:  Error: pg_config executable not found.
* https://stackoverflow.com/questions/11618898/pg-config-executable-not-found
* ubuntu: `sudo apt-get install libpq-dev`