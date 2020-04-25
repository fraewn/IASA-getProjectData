from ManageCodeAnalysis import ManageCodeAnalysis
from service.globalDatabaseAccess import GlobalDatabaseAccess

class CreateProjectControl:
    def __init__(self, project_id):
        self.project_id = project_id
        self.globalDatabaseAccess = GlobalDatabaseAccess()

    def createProject(self):
        print("creating project...")

        projectDatabaseURL = self.getProjectDatabaseCredentials()
        #print(projectDatabaseURL)
        projectGitURL = self.getProjectGitURL()
        #print(projectGitURL)

        managerepdata = ManageCodeAnalysis()
        # managerepdata.getSourceCode(projectGitURL)
        print("Downloaded project data...")
        # managerepdata.getGitInfo(projectGitURL)
        print("Cloned repository for dependency analysis")

        # managerepdata.analyseDependencies()
        print("Analysing Dependencies...")
        # managerepdata.persData()
        print("imported project data into neo4j")
        # managerepdata.persPatternData()
        print("imported pattern data into neo4j")
        self.globalDatabaseAccess.close()

    def getProjectGitURL(self):
        query = "SELECT PROJECT_GITURL FROM PROJECT WHERE PROJECT_ID = {}".format(self.project_id)
        print(query)
        self.projectGitURL = self.globalDatabaseAccess.executeQuery(query)
        print(self.projectGitURL)


    def getProjectDatabaseCredentials(self):
        query = "SELECT PROJECTDATABASE_URL FROM PROJECTDATABASE WHERE PROJECT_ID = {};".format(self.project_id)
        print(query)
        projectDatabaseURL = self.globalDatabaseAccess.executeQuery(query)
        print(projectDatabaseURL)
        query = "SELECT PROJECTDATABASE_USER FROM PROJECTDATABASE WHERE PROJECT_ID = {};".format(self.project_id)
        print(query)
        projectDatabaseUser = self.globalDatabaseAccess.executeQuery(query)
        print(projectDatabaseUser)
        query = "SELECT PROJECTDATABASE_PASSWORD FROM PROJECTDATABASE WHERE PROJECT_ID = {};".format(self.project_id)
        projectDatabasePassword = self.globalDatabaseAccess.executeQuery(query)
        print(query)
        print(projectDatabasePassword)
