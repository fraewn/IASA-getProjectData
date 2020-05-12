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

    def updateFiles(self, filename):
        queries = self.produceQueries.createFileQueries(filename)
        for i in range(len(queries)):
            # execute query
            self.projectDatabaseAccess.executequery(queries[1])

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

    def checkFileExists(self, filepath):
        checkFileExistQueries = self.produceQueries.createCheckFileExistQueries(filepath)
        for i in range(len(checkFileExistQueries)):
            if checkFileExistQueries[i][1] == "ModificationType.ADD":
                query = checkFileExistQueries[i][2]

                # shit works
                fileExists = False
                for record in self.projectDatabaseAccess.executeQueryWithResult(query):
                    fileExists = True
                if fileExists == False:
                    # persist file
                    file = checkFileExistQueries[i][0]
                    print("persisting new file: " + file)
                    self.persistFile(file)

            if checkFileExistQueries[i][1] == "ModificationType.DELETE":
                query = checkFileExistQueries[i][2]
                fileExists = False
                for record in self.projectDatabaseAccess.executeQueryWithResult(query):
                    fileExists = True
                if fileExists == True:
                    # delete file
                    file = checkFileExistQueries[i][0]
                    print("deleting file: " + file)
                    self.deleteFile(file)

    def persistFile(self, file):
        query = "CREATE (file:File {filename: '" + file + "'})"
        print(query)
        self.projectDatabaseAccess.executequery(query)

    def deleteFile(self, file):
        query = "MATCH (n:File { filename: '" + file + "' }) DETACH DELETE n"
        print(query)
        self.projectDatabaseAccess.executequery(query)

    def checkRelationExists(self, filepath):
        checkRelationExistQueries = self.produceQueries.createCheckRelationExistsQueries(filepath)
        for i in range(len(checkRelationExistQueries)):
            query = checkRelationExistQueries[i][3]
            #print(query)
            dependencyExists = False
            for record in self.projectDatabaseAccess.executeQueryWithResult(query):
                # if record is not empty (a relation exists)
                dependencyExists = True
                # if record is empty
            if dependencyExists == False:
                # create new dependency there
                class1 = checkRelationExistQueries[i][0]
                class2 = checkRelationExistQueries[i][1]
                relation = checkRelationExistQueries[i][2]
                self.persistDependency(class1, class2, relation)

    def persistDependency(self, class1, class2, relation):
        query = "MERGE (file:File {filename:'" + class1 + "'}) " \
                "MERGE (filetwo:File {filename:'" + class2 + "'}) " \
                "CREATE (file)-[:`" + relation + "`]->(filetwo)"
        print("persisted dependency: " + query)
        self.projectDatabaseAccess.executequery(query)









