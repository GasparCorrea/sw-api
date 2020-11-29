import flask
import json
from flask import jsonify, make_response, request
from flask_swagger_ui import get_swaggerui_blueprint

# Reads json file with data in its original state
with open('./data/characters.json') as json_file:
    data = json.load(json_file)

# Flask config
app = flask.Flask(__name__, static_url_path='/static')
app.config["DEBUG"] = True

# Swagger config
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger'  # Our API url (can of course be a local resource)
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Star Wars Characters Wiki"
    },
)

app.register_blueprint(swaggerui_blueprint)

# Swagger config static file
@app.route('/static/swagger')
def send_static():
    return app.send_static_file('swagger.json')

# Returns all characters
@app.route('/',methods=['GET','POST'])
def home():
    if flask.request.method == 'GET':
        return jsonify(data)
    elif flask.request.method == 'POST':
        new_id = str( int(max(data.keys())) + 1)
        data[new_id] = request.json
        return jsonify(data[new_id])
    else:
        msg = "Sorry, we dont know what you wanted"
        return make_response(jsonify(msg),400)

# Returns character by given id
@app.route('/<character_id>',methods=['GET','PUT','DELETE'])
def character(character_id):
    if character_id in data:
        if flask.request.method == 'GET':
            return jsonify(data[character_id])
        elif flask.request.method == 'PUT':
            data[character_id] = request.json
            return jsonify(data[character_id])
        elif flask.request.method == 'DELETE':
            data.pop(character_id)
            msg = "Succesful delete"
            return make_response(jsonify(msg), 204)
        else:
            msg = "Sorry, we dont know what you wanted"
            return make_response(jsonify(msg),400)

    else:
        msg = "Given character id doesn't exists. Try another!"
        return make_response(jsonify(msg), 404)

app.run()