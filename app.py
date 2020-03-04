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
        project_id = dictionary["queryResult"]["parameters"]["project_id"]
        bucket = "gs://"+project_id+".appspot.com"
        region = dictionary["queryResult"]["parameters"]["region"]
        zones = dictionary["queryResult"]["parameters"]["zone"]
        instance_group_name = dictionary["queryResult"]["parameters"]["instance_group_name"]
        instance_per_group = dictionary["queryResult"]["parameters"]["instance_per_group"]["number-integer"]
        instance_group_count = dictionary["queryResult"]["parameters"]["instance_group_count"]
        instance_name = (project_id.split('-'))[0]

        #Create Instance
        #create for loop and change instance_name
        c = 0
        x = (instance_per_group*instance_group_count)//len(zones)
        for number in range(0,int(instance_per_group*instance_group_count),int(x)):
            for n in range(0,int(x)): 
                instance(project_id,bucket,instance_name+str(number+n),region+"-"+zones[c])
            c=c+1

        #Create group
        for number in range(0,instance_group_count):
            group(project_id,bucket,region+"-"+zones[number],instance_name,instance_per_group,instance_per_group)

        json_file="" 
        with open("payload.json") as j:
            json_file = json.load(j)
        return jsonify(json_file)

    else:
        print("hello")
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
            instance_templates_size=instance_size,
            group_name = instance_name+"-group",group_size=group_size)

#Create instance templates. dont pass size. do create a while loop
#naming convention = example1,example2,example3
if __name__ == '__main__':
    app.run(host="127.0.0.1",port="80")
