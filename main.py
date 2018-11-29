from flask import Flask, request, abort, Response
import json
import os

app = Flask(__name__)
postPath = '/'+os.environ['POST_PATH'] if 'POST_PATH' in os.environ else '/webhook'
versionFile = '/GIT_SHA'

# Read in version file provided by automated pipeline
if os.path.exists(versionFile):
    shaFile = open(versionFile, 'r')
    gitSHA = shaFile.read()
    gitSHA = gitSHA.replace('\n', '')
    shaFile.close()
else:
    gitSHA = 'non-pipeline build'

@app.route('/')
def route_root():
    # check for custom header
    key,value = 'number','4'
    if key in request.headers and value == request.headers[key]:
        return 'Yadi, Yadi, Yadi...\n'
    else:
        abort(404)

# Provide git SHA and configured POST method path on http request
@app.route('/status')
def route_status():
    currentStatus = {
        'sha': gitSHA,
        'path': postPath
    }
    return Response(json.dumps(currentStatus), mimetype='application/json')

# Print received POST headers and json payload
@app.route(postPath, methods=['POST'])
def route_post():
   data = json.loads(request.data)
   print('** Headers **')
   print(request.headers)
   print('** Payload **')
   print(json.dumps(data, indent=4, sort_keys=True))
   return "OK"

if __name__ == '__main__':
   app.run()