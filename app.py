import sys
from flask import Flask, request, abort, jsonify
from create_instance import main
import json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    print("webhook"); sys.stdout.flush()
    if request.method == 'POST':
        dictionary = dict(request.json)
        project = dictionary["queryResult"]["parameters"]["project_id"]
        bucket = "gs://"+project+".appspot.com"
        instance_name = dictionary["queryResult"]["parameters"]["name"]
        zone = dictionary["queryResult"]["parameters"]["zone"]
        main(project,bucket,zone,instance_name)
        json_file = json.load("payload.json")
        return jsonify(json_file)
    else:
        abort(400)

if __name__ == '__main__':
    app.run()
