import sys
from flask import Flask, request, abort, jsonify
from create_instance import main
from create_instance import delete_instance
from create_groups import main as create_groups_main
from create_templates import main as create_templates_main
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
        instance_size=  dictionary["queryResult"]["parameters"]["instance-size"]
        group_size=  dictionary["queryResult"]["parameters"]["group-size"]

        #Create Template
        template(project,bucket,zone,instance_name)

        #Create Instance
        instance(project,bucket,instance_name,zone)

        #Create group
        group(project,bucket,zone,instance_name,instance_size,group_size)

        json_file="" 
        with open("payload.json") as j:
            json_file = json.load(j)
        return jsonify(json_file)

    else:
        abort(400)

def instance(project,bucket,instance_name,zone):
    main(project,bucket,zone,instance_name)

def template(project,bucket,zone,instance_name):
    create_templates_main(project = project,bucket = bucket,zone = zone,instance_name = instance_name)

def group(project,bucket,zone,instance_name,instance_size,group_size):
    create_groups_main(
            project=project,
            bucket=bucket,
            zone=zone,
            instance_templates = instance_name,
            instance_templates_size=1,
            group_name = instance_name+"-group",group_size=1)

#Create instance templates. dont pass size. do create a while loop
#naming convention = example1,example2,example3


if __name__ == '__main__':
    app.run(host="127.0.0.1",port="80")
