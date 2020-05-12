from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from updateProjectControl import UpdateProjectControl

app = Flask(__name__)
api = Api(app)

# DOCUMENTATION https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api

# add some test data
PROJECT = {
    # 'request_id': {'project_data_attribute': 'project_data'}
    '0': {'project_id': 0}
}

# working
# test if a request with a specific request_id exists, if not: send error message
def abort_if_project_doesnt_exist(request_id):
    if request_id not in PROJECT:
        abort(404, message="Request failed, {} doesn't exist".format(request_id))


# working
# create automatic validation of input values
# initialise parser
parser = reqparse.RequestParser()

# add arguments to parser: project_id (int) and dev_id (int)
parser.add_argument('project_id', type=int)


# defines the endpoint for a specific projectPullRequest by offering REST operations to get, delete and update it
# GET, DELETE, PUT
class project(Resource):
    # working
    # REST GET method, needs request_id
    # test with: curl localhost:5000/projects/1
    def get(self, request_id):
        # check if there is a request that matches the request_id
        abort_if_project_doesnt_exist(request_id)
        # look in array for request and return it
        return PROJECT[request_id]

    # working
    # REST DELETE, needs request_id
    # deletes an existing projectPullRequest: url is http://localhost:5000/projects/<request_id>
    # test with: curl localhost:5000/projects/1 -X DELETE
    def delete(self, request_id):
        abort_if_project_doesnt_exist(request_id)
        # uses already existing function del
        del PROJECT[request_id]
        # return nothing (shows that it was deleted) and code 204 that it worked
        return '', 204

    # working
    # REST PUT, needs request_id
    # updates an existing project: url is http://localhost:5000/projects/<request_id>
    # test with: curl localhost:5000/projects/1 -d "project_id=12" -X PUT
    def put(self, request_id):
        # parse the arguments and save it in python dictionary args
        args = parser.parse_args()

        # read python dict args using e.g. args['key']
        # save value from project_id in variable that is a json_dict, e.g.: project_id_dict = {'project_id': 1}
        project_id_dict = {'project_id': args['project_id']}

        # update project
        # save project in variable source
        source = PROJECT[request_id]
        # update project_id
        source['project_id'] = project_id_dict['project_id']

        # return the updated request
        return PROJECT[request_id], 201


# defines a general endpoint for projects by offering REST operations to create a new one and get all
class projectList(Resource):
    # working
    # get all projects
    # test with: curl localhost:5000/projects/
    def get(self):
        return PROJECT

    # working
    # create a new project
    # test with: curl localhost:5000/update/projects -d "project_id=4" -X POST
    def post(self):
        # parse the arguments and save it in python dictionary args
        args = parser.parse_args()

        # find out highest exisiting request_id_number, increment it by 1 and
        # save the number in variable 'request_id_number'
        request_id_number = int(max(PROJECT.keys())) + 1
        # print(request_id_number)
        # create a new request_id like 'request_<request_id_number>'
        request_id = str(request_id_number)

        # read python dict args using e.g. args['key']
        # save value from project_id in variable that is a json_dict, e.g.: project_id = {'project_id': 1}
        project_id_dict = {'project_id': args['project_id']}

        # create an empty project with newly created request_id
        # save it in variable 'source'
        source = PROJECT[request_id] = {'project_id': ''}
        # update project_id and developer_id
        source['project_id'] = project_id_dict['project_id']

        # trigger create project process
        updateProjectControl = UpdateProjectControl(source['project_id'])
        updateProjectControl.updateProject()

        # return newly added todo_ and status code
        return PROJECT[request_id], 201

# add url endpoints
# all requests
api.add_resource(projectList, '/update_projects')
# a specific request
api.add_resource(project, '/update_projects/<request_id>')

# run
if __name__ == '__main__':
    # set debug mode to false
    app.run(debug=False)