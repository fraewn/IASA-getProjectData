from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

# DOCUMENTATION https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api

# create some projectPullRequests for testing
# test with: curl localhost:5000/requests
PROJECTPULLREQUESTS = {
    'projectPullRequest1': {'project_id': 'project_1', 'developer_id': 'dev_1'},
    'projectPullRequest2': {'project_id:': 'project_2', 'developer_id': 'dev_2'},
}

# working
# test if a request with a specific request_id exists, if not: send error message
def abort_if_projectPullRequest_doesnt_exist(request_id):
    if request_id not in PROJECTPULLREQUESTS:
        abort(404, message="Request {} doesn't exist".format(request_id))


# working
# create automatic validation of input values
# initialise parser
parser = reqparse.RequestParser()

# add arguments to parser: project_id (int) and dev_id (int)
parser.add_argument('project_id', type=int)
parser.add_argument('developer_id', type=int)


# defines the endpoint for a specific projectPullRequest by offering REST operations to get, delete and update it
# GET, DELETE, PUT
class projectPullRequest(Resource):
    # working
    # REST GET method, needs request_id
    # test with: curl localhost:5000/requests/projectPullRequest1
    def get(self, request_id):
        # check if there is a request that matches the request_id
        abort_if_projectPullRequest_doesnt_exist(request_id)
        # look in array for request and return it
        return PROJECTPULLREQUESTS[request_id]

    # working
    # REST DELETE, needs request_id
    # deletes an existing projectPullRequest: url is http://localhost:5000/requests/<request_id>
    # test with: curl localhost:5000/requests/projectPullRequest1 -X DELETE
    def delete(self, request_id):
        abort_if_projectPullRequest_doesnt_exist(request_id)
        # uses already existing function del
        del PROJECTPULLREQUESTS[request_id]
        # return nothing (shows that it was deleted) and code 204 that it worked
        return '', 204

    # working
    # REST PUT, needs request_id
    # updates an existing projectpullrequest: url is http://localhost:5000/requests/<request_id>
    # test with: curl localhost:5000/requests/projectPullRequest1 -d "project_id=12" -d "developer_id=900" -X PUT
    def put(self, request_id):
        # parse the arguments and save it in python dictionary args
        args = parser.parse_args()

        # read python dict args using e.g. args['key']
        # save value for developer id in variable
        developer_id = {'developer_id': args['developer_id']}
        # save value from project_id in variable that is a json_dict, e.g.: project_id = {'project_id': 1}
        project_id = {'project_id': args['project_id']}

        # update projectpullrequest
        # save projectpullrequest in variable source
        source = PROJECTPULLREQUESTS[request_id]
        # update project_id and developer_id
        source['project_id'] = project_id
        source['developer_id'] = developer_id

        # return the updated request
        return PROJECTPULLREQUESTS[request_id], 201


# defines a general endpoint for projectPullRequests by offering REST operations to create a new one and get all
class projectPullRequestList(Resource):
    # working
    # get all projectPullRequests
    # test with: curl localhost:5000/requests/
    def get(self):
        return PROJECTPULLREQUESTS

    # working
    # create a new projectPullRequest
    # test with: curl localhost:5000/requests -d "project_id=4" -d "developer_id=4" -X POST
    def post(self):
        # parse the arguments and save it in python dictionary args
        args = parser.parse_args()

        # find out highest exisiting request_id_number, increment it by 1 and
        # save the number in variable 'request_id_number'
        request_id_number = int(max(PROJECTPULLREQUESTS.keys()).lstrip('projectPullRequest')) + 1
        print(request_id_number)
        # create a new request_id like 'projectPullRequest<request_id_number>'
        request_id = 'projectPullRequest%i' % request_id_number

        # read python dict args using e.g. args['key']
        # save value from project_id in variable that is a json_dict, e.g.: project_id = {'project_id': 1}
        project_id = {'project_id': args['project_id']}
        # save value for developer id in variable
        developer_id = {'developer_id': args['developer_id']}

        # create an empty projectPullRequest with newly created request_id
        # save it in variable 'source'
        source = PROJECTPULLREQUESTS[request_id] = {'project_id': '', 'developer_id': ''}
        # update project_id and developer_id
        source['project_id'] = project_id
        source['developer_id'] = developer_id

        # return newly added todo_ and status code
        return PROJECTPULLREQUESTS[request_id], 201

# add url endpoints
# all requests
api.add_resource(projectPullRequestList, '/requests')
# a specific request
api.add_resource(projectPullRequest, '/requests/<request_id>')

# run
if __name__ == '__main__':
    # set debug mode to false
    app.run(debug=False)
