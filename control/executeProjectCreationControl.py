import os
import shutil
import stat
from subprocess import call
from git import Repo

from DependencyAnalysis import DependencyAnalysis
from GetRepositoryData import GetRepositoryData
from ManagePersistence import ManagePersistence
from service.util.util import Util

class ExecuteProjectCreationControl:
    link_to_home_directory = "1"

    def __init__(self, projectdatabase_url, projectdatabase_username, projectdatabase_password):
        # set class variables
        self.util = Util()
        self.managePersistence = ManagePersistence()
        self.dependencyAnalysis = DependencyAnalysis()

        # get environment
        self.link_to_home_directory = self.util.getDependencyAnalysisLink()

        # set paths to local project data
        self.class_csv = self.link_to_home_directory + '/result/rawrepdatacsv.csv'
        self.dependency_csv = self.link_to_home_directory + '/result/dependencymatrix.csv'

        # init project database connection
        self.managePersistence.init_connection(projectdatabase_url, projectdatabase_username, projectdatabase_password)

    # used
    def getSourceCode (self, projectGitURL):
        # prepare working directory for cloning a git project into it
        self.cleanUpFolder(self.link_to_home_directory)
        # clone repository from git
        # save repo temporarily in home directory
        Repo.clone_from(projectGitURL, self.link_to_home_directory)
        # check if compiled files exist in clones git repository (otherwise the dependency analysis does not work)
        if (self.compiledFilesExist(self.link_to_home_directory)) is not True:
           raise Exception ('No compiled files found! Please provide a project with compiled java code.')

    # benutzt die pydriller Klasse
    def getGitInfo(self, path):
        os.makedirs(self.link_to_home_directory + "/result")
        with open(self.link_to_home_directory + "/result/rawrepdatacsv.csv" , 'w'):
            pass
        getRepositoryData = GetRepositoryData()
        getRepositoryData.getRepInfo(self.link_to_home_directory + "/result/rawrepdatacsv.csv", path)

    def persistProjectData (self):
        # persist project files in project database
        self.managePersistence.process_persisting(self.link_to_home_directory + '/result/rawrepdatacsv.csv')
        # persist class dependencies in project database
        self.managePersistence.process_dependency_persisting(self.link_to_home_directory + '/result/dependencymatrix.csv')
        # set a default password for the developer
        self.managePersistence.setDeveloperDefaultPassword()

    def updateProjectFiles(self):
        # check if file already exists and if not, persist it
        self.managePersistence.checkFileExists(self.class_csv)

    def updateProjectDependencies(self):
        # check if relation already exists and if not, persist it
        self.managePersistence.checkRelationExists(self.dependency_csv)

    def persistPatternData (self):
        self.managePersistence.process_patterns_persisting()

    def analyseDependencies(self):
        self.dependencyAnalysis.analyseDependencies()
        self.dependencyAnalysis.formatDependenciesClean()

    def compiledFilesExist(self, link):
        for root, dirs, files in os.walk(link):
            for name in files:
                if ".class" in name:
                    print (name)
                    return True
        return False

    def cleanUpFolder (self, link):
        linkgit = link + ('/.git')
        linkgitobjpack = link + ('/.git/objects')

        #Cleanup of the Workdirectory
        if os.path.isdir(linkgit):
            call(['attrib', '-H', linkgit])
            for root, dirs, files in os.walk(linkgitobjpack):
                for f in files:
                    os.chmod(root +"/" + f,stat.S_IWRITE)
                    os.unlink(root +"/"+ f)
            os.chmod(linkgitobjpack,stat.S_IWRITE)
            shutil.rmtree(linkgitobjpack)
            shutil.rmtree(linkgit)
            for entry in os.scandir(link):
                if entry.is_file():
                    os.unlink(entry)
                else:
                    shutil.rmtree(entry)
        elif (os.path.isdir(link+'/result')):
            shutil.rmtree(link+'/result')

    def deleteLocalProjectFolder(self):
        if(os.path.exists(self.link_to_home_directory)):
            shutil.rmtree(self.link_to_home_directory)

    # used
    def deleteDataFromProjectDatabase(self):
        # clean up database
        self.managePersistence.deleteProject()


