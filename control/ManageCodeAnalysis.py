import os
import platform
import shutil
import stat
from subprocess import call

from git import Repo
from DependencyAnalysis import DependencyAnalysis
from GetRepositoryData import GetRepositoryData
from ManagePersistence import ManagePersistence
from service.util.credentials import Credentials


class ManageCodeAnalysis:
    link="1"

    def getGitInfo(self, path):
        print (self.link)
        os.makedirs(self.link+"/result")
        with open(self.link +"/result/rawrepdatacsv.csv" , 'w'):
            pass
        getRepsoitoryData = GetRepositoryData()
        getRepsoitoryData.getRepInfo(self.link + "/result/rawrepdatacsv.csv", path)

    def getSourceCode (self, path):
        credentials = Credentials()
        self.link=credentials.getDependencyAnalysisLink()
        self.cleanUpFolder(self.link)


        #Download of the Source Code
        Repo.clone_from(path, self.link)
        #Check if compiled files exist
        if (self.compiledFilesExist(self.link)) is not True:
           raise Exception ('No compiled files found! Please provide a project with compiled java code.')

    def persData (self):
        managePers = ManagePersistence()
        managePers.init_connection(Credentials.uri, Credentials.userName, Credentials.password)
        managePers.process_persisting(Credentials.uri,Credentials.userName, Credentials.password,self.link +'/result/rawrepdatacsv.csv')
        managePers.process_dependency_persisting(Credentials.uri, Credentials.userName, Credentials.password, self.link +'/result/dependencymatrix.csv')


    def persPatternData (self):
        managePers = ManagePersistence()
        managePers.init_connection(Credentials.uri, Credentials.userName, Credentials.password)
        managePers.process_patterns_persisting(Credentials.uri, Credentials.userName, Credentials.password)


    def analyseDependencies(self):
        depana = DependencyAnalysis()
        depana.analyseDependencies()
        depana.formatDependenciesClean()

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

