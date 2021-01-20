#------------------------------------------------------------------------------
# To run your web server, open up your terminal / command prompt
# and type:
#    cd <path to this file>
#    python practical-03c-deployment.py
#
#------------------------------------------------------------------------------

from flask import Flask, flash, request, redirect, url_for, Response
import requests
import os
import json

# Configure our application 
#
tensorflow_server_url = "http://172.17.0.3:8501/"

# Initialize our Flask app.
# NOTE: Flask is used to host our app on a web server, so that
# we can call its functions over HTTP/HTTPS.
#
app = Flask(__name__)

#------------------------------------------------------------------------------
# This is our predict URL.
#
# This is just a pass-through (in other words a reverse proxy) that routes
# the entire JSON body to our tensorflow/serving container, retrieves the
# predictions and sends the predictions as-is to the caller.
#------------------------------------------------------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    
    # In this deployment, we are not using file uploads.
    # Instead we will extract JSON directly from the body,
    # which makes things a little easier.
    #
    x = request.get_json()
  
    # TODO:
    # Set the IP address of the Docker container with the tensorflow/serving
    # image to connect to.
    #
    url = tensorflow_server_url + 'v1/models/model/versions/1:predict'

    # Set the headers
    #
    headers = {'Content-Type': 'application/json'}

    # POST our JSON coming from the client application
    # to the tensorflow/serving container.
    #
    response = requests.post(url = url, headers = headers, json = x);
    
    # If successful
    if response.status_code == 200:

        # Retrieve the response and send it back as-is to
        # the calling application.
        #
        y = response.json()
        return Response(json.dumps(y), mimetype='application/json') 

    return Response("{}", mimetype='application/json')                           



#------------------------------------------------------------------------------
# This starts our web server.
# Although we are running this on our local machine,
# this can technically be hosted on any VM server in the cloud!
#------------------------------------------------------------------------------
if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)


