import csv

class ProduceQueries:
    def create_git_info_queries(self, filename):
        with open(filename, 'r') as f:
            csvreader = csv.reader(f, delimiter=';')
            # store queries in array
            queries = []
            # iterate through rows in csv file
            next(csvreader, None) # skip headers
            for row in csvreader:
                # assign variables to cells in columns
                filename = row[0]
                developer = row[1]
                changetype = row[4]
                if changetype == "ModificationType.ADD":
                    if filename.__contains__('.java'):
                        # create query to add two nodes and their edge
                        query = "MERGE (file:File {filename:'" \
                        + filename + "'}) MERGE (developer:Developer " \
                        "{devname:'" + developer + "'}) " \
                        "CREATE (file)<-[:GITADD]-(developer)"
                        # add newly created query to array
                        queries.append(query)
                # create query to delete file- and developer
                if changetype == "ModificationType.DELETE":
                    if filename.__contains__('.java'):
                        querydelete = "MATCH(file:File {filename:'" \
                        + filename + "'})-[r]-(developer:Developer) " \
                        "DETACH DELETE file"
                        print("deletequery: " + querydelete)
                        queries.append(querydelete)
            # return array with all queries
            return queries

    def create_dependencies_queries(self, filename):
        with open(filename, 'r') as f:
            csvreader = csv.reader(f, delimiter=';')
            # store queries in array
            dependencyqueries = []
            # iterate through rows in csv file
            for row in csvreader:
                class1 = row[0]
                class2 = row[1]
                relation = row[2]
                relationup = relation.upper()
                query = "MERGE (file:File {filename:'" + class1 + "'}) " \
                        "MERGE (filetwo:File {filename:'" + class2 +"'}) " \
                        "CREATE (file)-[:`" + relationup + "`]->(filetwo)"
                dependencyqueries.append(query)
            #return array with all queries
            return dependencyqueries

    def create_patterns_queries (self):
        patternsqueries = []
        #Singleton Pattern
        singleton_pattern = "CREATE (singleton:Pattern {patternname:'Singleton'})" \
                            +" MERGE (usingclass:Patterncomponent {componentname:'usingClass'})" \
                            + " MERGE (singletonclass:Patterncomponent {componentname:'SingletonClass'})" \
                            + " CREATE (singleton)-[:HASCOMPONENT]->(usingclass)" \
                            + " CREATE (singleton)-[:HASCOMPONENT]->(singletonclass)" \
                            + " CREATE (usingclass)-[:USES]->(singletonclass)"
        patternsqueries.append(singleton_pattern)
            #Strategy Pattern
        strategy_pattern = "CREATE (strategy:Pattern {patternname:'Strategy'})" \
                           + " MERGE (strategyclient:Patterncomponent {componentname:'StrategyClient'})" \
                           + " MERGE (abstractstrategy:Patterncomponent {componentname:'AbstractStrategy'})" \
                           + " MERGE (concretestrategy:Patterncomponent {componentname:'ConcreteStrategy'})" \
                           + " CREATE (strategy)-[:HASCOMPONENT]->(strategyclient)" \
                           + " CREATE (strategy)-[:HASCOMPONENT]->(concretestrategy)" \
                           + " CREATE (strategy)-[:HASCOMPONENT]->(abstractstrategy)" \
                           + " CREATE (concretestrategy)-[:EXTENDS]->(abstractstrategy)" \
                           + " CREATE (strategyclient)-[:USES]->(abstractstrategy)"
        patternsqueries.append(strategy_pattern)

        #Command Pattern
        command_pattern = "CREATE (command:Pattern {patternname:'Command'})" \
                          + " MERGE (commandcaller:Patterncomponent {componentname:'CommandCaller'})" \
                          + " MERGE (commandclient:Patterncomponent {componentname:'CommandClient'})" \
                          + " MERGE (abstractcommand:Patterncomponent {componentname:'AbstractCommand'})" \
                          + " MERGE (concretecommand:Patterncomponent {componentname:'ConcreteCommand'})" \
                          + " MERGE (commandreceiver:Patterncomponent {componentname:'CommandReceiver'})" \
                          + " CREATE (command)-[:HASCOMPONENT]->(commandclient)" \
                          + " CREATE (command)-[:HASCOMPONENT]->(commandcaller)" \
                          + " CREATE (command)-[:HASCOMPONENT]->(abstractcommand)" \
                          + " CREATE (command)-[:HASCOMPONENT]->(concretecommand)" \
                          + " CREATE (command)-[:HASCOMPONENT]->(commandreceiver)" \
                          + " CREATE (concretecommand)-[:EXTENDS]->(abstractcommand)" \
                          + " CREATE (commandclient)-[:USES]->(concretecommand)" \
                          + " CREATE (concretecommand)-[:USES]->(commandreceiver)" \
                          + " CREATE (commandclient)-[:USES]->(commandreceiver)" \
                          + " CREATE (commandcaller)-[:USES]->(abstractcommand)"
        patternsqueries.append(command_pattern)

        #Observer Pattern
        observer_pattern = "CREATE (observer:Pattern {patternname:'Observer'})" \
                           + " MERGE (publisher:Patterncomponent {componentname:'Publisher'})" \
                           + " MERGE (concretepublisher:Patterncomponent {componentname:'ConcretePublisher'})" \
                           + " MERGE (subscriber:Patterncomponent {componentname:'Subscriber'})" \
                           + " MERGE (concretesubscriber:Patterncomponent {componentname:'ConcreteSubscriber'})" \
                           + " CREATE (observer)-[:HASCOMPONENT]->(publisher)" \
                           + " CREATE (observer)-[:HASCOMPONENT]->(concretepublisher)" \
                           + " CREATE (observer)-[:HASCOMPONENT]->(subscriber)" \
                           + " CREATE (observer)-[:HASCOMPONENT]->(concretesubscriber)" \
                           + " CREATE (concretepublisher)-[:IMPLEMENTS]->(publisher)" \
                           + " CREATE (concretesubscriber)-[:IMPLEMENTS]->(subscriber)" \
                           + " CREATE (publisher)-[:USES]->(subscriber)" \
                           + " CREATE (concretesubscriber)-[:USES]->(concretepublisher)"
        patternsqueries.append(observer_pattern)

        #Proxy Pattern
        proxy_pattern = "CREATE (proxy:Pattern {patternname:'Proxy'})" \
                        + " MERGE (client:Patterncomponent {componentname:'Client'})" \
                        + " MERGE (proxy_class:Patterncomponent {componentname: 'Proxy Class'})" \
                        + " MERGE (realsubject:Patterncomponent {componentname: 'RealSubject'})" \
                        + " MERGE (subject:Patterncomponent {componentname:'Subject'})" \
                        + " CREATE (proxy)-[:HASCOMPONENT]->(client)" \
                        + " CREATE (proxy)-[:HASCOMPONENT]->(proxy_class)" \
                        + " CREATE (proxy)-[:HASCOMPONENT]->(realsubject)" \
                        + " CREATE (proxy)-[:HASCOMPONENT]->(subject)" \
                        + " CREATE (realsubject)-[:IMPLEMENTS]->(subject)" \
                        + " CREATE (proxy_class)-[:IMPLEMENTS]->(subject)" \
                        + " CREATE (client)-[:USES]->(proxy_class)" \
                        + " CREATE (client)-[:USES]->(subject)" \
                        + " CREATE (proxy_class)-[:USES]->(realsubject)"
        patternsqueries.append(proxy_pattern)

        #Round Tripping Persistent Object Pattern
        round_tripping_pattern = "CREATE (roundtrippingpersistentobject:Pattern {patternname:'Round Tripping Persistent Object'})" \
                                 + " MERGE (testclass:Patterncomponent {componentname:'TestClass'})" \
                                 + " MERGE (dao:Patterncomponent {componentname:'DAO'})" \
                                 + " MERGE (compareclass:Patterncomponent {componentname:'CompareClass'})" \
                                 + " CREATE (roundtrippingpersistentobject)-[:HASCOMPONENT]->(testclass)" \
                                 + " CREATE (roundtrippingpersistentobject)-[:HASCOMPONENT]->(dao)" \
                                 + " CREATE (roundtrippingpersistentobject)-[:HASCOMPONENT]->(compareclass)" \
                                 + " CREATE (testclass)-[:USES]->(dao)" \
                                 + " CREATE (testclass)-[:USES]->(compareclass)"
        patternsqueries.append(round_tripping_pattern)


        return patternsqueries

