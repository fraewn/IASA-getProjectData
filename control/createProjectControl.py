from service.globalDatabaseAccess import GlobalDatabaseAccess
from executeProjectCreationControl import ExecuteProjectCreationControl

class CreateProjectControl:
    def __init__(self, project_id):
        self.project_id = project_id
        self.globalDatabaseAccess = GlobalDatabaseAccess()

    def createProject(self):
        try:
            projectDatabaseURL = self.getProjectDatabaseURL()
            projectDatabaseUsername = self.getProjectDatabaseUsername()
            projectDatabasePassword = self.getProjectDatabasePassword()

            projectGitURL = self.getProjectGitURL()
            print("Step 0: connected to global database to get credentials and link to git repository")

            # manage all operations to create project
            executeProjectCreation = ExecuteProjectCreationControl(projectDatabaseURL, projectDatabaseUsername, projectDatabasePassword)

            # clean project database
            executeProjectCreation.deleteDataFromProjectDatabase()
            print("Step 1: cleaned project database")
            # download source and save locally
            executeProjectCreation.getSourceCode(projectGitURL)
            print("Step 2: cloned git repository to temporary local folder")
            # check if source is usable
            executeProjectCreation.getGitInfo(projectGitURL)
            print("Step 3: checked if class dependencies in given git repository can be analysed")
            # execute dependency analysis
            executeProjectCreation.analyseDependencies()
            print("Step 4: analysed dependencies")
            # persist projectdata in projectdatabase
            executeProjectCreation.persistProjectData()
            print("Step 5: persisted project data in project database")
            # persist pattern data in projectdatabase
            executeProjectCreation.persistPatternData()
            print("Step 6: persisted pattern data in project database")
            executeProjectCreation.deleteLocalProjectFolder()
            print("Step 7: cleaned up temporary local project data")
        except(Exception) as error:
            print(error)
        finally:
            self.globalDatabaseAccess.close()

    def getProjectGitURL(self):
        query = "SELECT PROJECT_GITURL FROM PROJECT WHERE PROJECT_ID = {}".format(self.project_id)
        return self.globalDatabaseAccess.executeQuery(query)

    def getProjectDatabaseURL(self):
        query = "SELECT PROJECTDATABASE_URL FROM PROJECTDATABASE WHERE PROJECT_ID = {};".format(self.project_id)
        return self.globalDatabaseAccess.executeQuery(query)

    def getProjectDatabaseUsername(self):
        query = "SELECT PROJECTDATABASE_USER FROM PROJECTDATABASE WHERE PROJECT_ID = {};".format(self.project_id)
        return self.globalDatabaseAccess.executeQuery(query)

    def getProjectDatabasePassword(self):
        query = "SELECT PROJECTDATABASE_PASSWORD FROM PROJECTDATABASE WHERE PROJECT_ID = {};".format(self.project_id)
        return self.globalDatabaseAccess.executeQuery(query)



