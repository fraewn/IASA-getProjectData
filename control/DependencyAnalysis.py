from xml.etree import ElementTree
import csv
import subprocess

from service.util.credentials import Credentials

class DependencyAnalysis:
    def analyseDependencies (self):
        #Call of the Dependency Analysis Function via JAR subprocess
        subprocess.call(['java', '-jar', 'DependencyAnalysis.jar'])

    def formatDependenciesClean (self):
        credentials = Credentials ()
        #Open result csv file
        with open(credentials.getDependencyAnalysisLink() + '/result/dependencymatrix.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #parsing of the DAAccess result file
            tree = ElementTree.parse(credentials.getDependencyAnalysisLink() + '/result/result.odem')
            tree.getroot()
            #select relevant results and write into result csv file
            for child in tree.iter('type'):
                for subchild in child.iter('depends-on'):
                    if ("java." not in subchild.attrib.get('name')):
                        childattrib = child.attrib.get('name')
                        childattrib = childattrib.split('.').pop()
                        childattrib = childattrib + ".java"
                        csvfile.write(childattrib + ";")
                        subchildattrib = subchild.attrib.get('name')
                        subchildattrib = subchildattrib.split('.').pop()
                        subchildattrib = subchildattrib + ".java"
                        csvfile.write(subchildattrib + ";")
                        csvfile.write(subchild.attrib.get('classification') )
                        csvfile.write("\n")



    def formatDependencies (self):
        credentials = Credentials ()
        with open(credentials.getDependencyAnalysisLink() + '/result/dependencymatrix.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            tree = ElementTree.parse(credentials.getDependencyAnalysisLink() + "/result/result.odem")
            tree.getroot()
            for child in tree.iter('type'):
                for subchild in child.iter('depends-on'):
                    if ("java." not in subchild.attrib.get('name')):
                        csvfile.write(""+child.attrib.get('name') + ";")
                        csvfile.write(subchild.attrib.get('name') + ";")
                        csvfile.write(subchild.attrib.get('classification') )
                        csvfile.write("\n")