from service.globalDatabaseAccess import GlobalDatabaseAccess
from executeProjectCreationControl import ExecuteProjectCreationControl

class UpdateProjectControl:
    def __init__(self, project_id):
        self.project_id = project_id
        self.globalDatabaseAccess = GlobalDatabaseAccess()

    def updateProject(self):
        try:
            # get project database environment
            projectDatabaseURL = self.getProjectDatabaseURL()
            projectDatabaseUsername = self.getProjectDatabaseUsername()
            projectDatabasePassword = self.getProjectDatabasePassword()

            # get project git environment
            projectGitURL = self.getProjectGitURL()

            print("Step 1: connected to global database to get credentials and link to git repository")

            # manage all operations to create project in one object
            executeProjectCreation = ExecuteProjectCreationControl(projectDatabaseURL, projectDatabaseUsername, projectDatabasePassword)

            # download source and save locally
            executeProjectCreation.getSourceCode(projectGitURL)
            print("Step 2: cloned git repository to temporary local folder")
            # check if source is usable (.class files need to be there)
            executeProjectCreation.getGitInfo(projectGitURL)
            print("Step 3: checked if class dependencies in given git repository can be analysed")
            # execute dependency analysis
            executeProjectCreation.analyseDependencies()
            print("Step 4: analysed dependencies")
            # persist projectdata in projectdatabase
            # working
            executeProjectCreation.updateProjectFiles()
            print("Step 5: updated file data in project database")
            # persist new dependencies
            executeProjectCreation.updateProjectDependencies()
            print("Step 6: updated dependencies in project database")
        except(Exception) as error:
            print(error)
        finally:
            # clean up local project data
            executeProjectCreation.deleteLocalProjectFolder()
            print("Step 7: cleaned up temporary local project data")
            # close global database connection
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



