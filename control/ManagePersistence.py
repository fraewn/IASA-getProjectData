# imports
from service.DatabaseAccess import DatabaseAccess
from model.ProduceQueries import ProduceQueries

class ManagePersistence:
    def __init__(self):
        print("ManagePersistence Class initiated")

    def init_connection(self, uri, userName, password):
        databaseaccess = DatabaseAccess(uri, userName, password)

    def process_persisting(self, uri, userName, password, filename):
        # execute producing of queries
        producequeries = ProduceQueries()
        queries = []
        queries = producequeries.create_git_info_queries(filename)

        # execute queries
        dbaccess = DatabaseAccess(uri, userName, password)
        #cleanup Database
        dbaccess.executequery("match(n) detach delete(n)")
        # iterate through query array
        for i in range(len(queries)):
            # execute query at i
            dbaccess.executequery(queries[i])

        print("query execution done")

    def process_dependency_persisting(self, uri, userName, password, filename):
        producequeries = ProduceQueries()
        queries = []
        queries = producequeries.create_dependencies_queries(filename)
        print("array with length of " + str(len(queries)) + " was filled with queries from " + filename)
        # execute queries
        dbaccess = DatabaseAccess(uri, userName, password)
        # iterate through query array
        for i in range(len(queries)):
            # execute query at i
            dbaccess.executequery(queries[i])

        print("Dependency query execution done")

    def process_patterns_persisting (self, uri, userName, password):
        producequeries = ProduceQueries()
        queries = []
        queries = producequeries.create_patterns_queries()
        print("array with length of " + str(len(queries)) + " was filled with Pattern Data")

        # execute queries
        dbaccess = DatabaseAccess(uri, userName, password)
        # iterate through query array
        for i in range(len(queries)):
            # execute query at i
            dbaccess.executequery(queries[i])
        #set Password to "abc"
        dbaccess.executequery("match (n:Developer) set n.password ='abc'")
        print("Patterns query execution done")









