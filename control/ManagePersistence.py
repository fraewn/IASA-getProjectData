from service.DatabaseAccess import DatabaseAccess
from model.ProduceQueries import ProduceQueries

class ManagePersistence:
    def __init__(self):
        self.produceQueries = ProduceQueries()

    def init_connection(self, uri, userName, password):
        self.projectDatabaseAccess = DatabaseAccess(uri, userName, password)



    def process_persisting(self, filename):
        # produce a project database query for each file and save in array "queries"
        queries = self.produceQueries.create_git_info_queries(filename)
        # iterate through query array
        for i in range(len(queries)):
            # execute query at i
            self.projectDatabaseAccess.executequery(queries[i])

    def process_dependency_persisting(self, filename):
        # produce a project database query for each dependency and save in array "queries"
        queries = self.produceQueries.create_dependencies_queries(filename)
        # iterate through query array
        for i in range(len(queries)):
            # execute query at i
            self.projectDatabaseAccess.executequery(queries[i])

    def process_patterns_persisting (self):
        # produce a project database query for each pattern and save in array "queries"
        queries = self.produceQueries.create_patterns_queries()
        # iterate through query array
        for i in range(len(queries)):
            # execute query at i
            self.projectDatabaseAccess.executequery(queries[i])

    def deleteProject(self):
        # cleanup Database
        self.projectDatabaseAccess.executequery("match(n) detach delete(n)")

    def setDeveloperDefaultPassword(self):
        # set developer default password to "abc"
        self.projectDatabaseAccess.executequery("match (n:Developer) set n.password ='abc'")









