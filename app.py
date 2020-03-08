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
    characters = ['a','b','c']
    
    if request.method == 'POST':

        dictionary = dict(request.json)
        project_id = dictionary["queryResult"]["parameters"]["project_id"]
        bucket = "gs://"+project_id+".appspot.com"
        region = dictionary["queryResult"]["parameters"]["region"]
        zones = dictionary["queryResult"]["parameters"]["zone"]["number-integer"]
        instance_group_name = dictionary["queryResult"]["parameters"]["instance_group_name"]
        instance_per_group = dictionary["queryResult"]["parameters"]["instance_per_group"]["number-integer"]
        instance_group_count = dictionary["queryResult"]["parameters"]["instance_group_count"]["number-integer"]

        instance_name = (project_id.split('-'))[0]
        characters = characters[0:zones]

        """
        Documentation: Instance Create 
        for example
        regions = [us-central1,us-west1]
        zones = 3
        group-name = example
        instances_per_group = 3
        group_count = 2

        Example0 region:us-central1
            - instance0 zone:a
            - instance1 zone:b
            - instance2 zone:c
        Example1 region:us-west1   
            - instance3 zone:a
            - instance4 zone:b
            - instance5 zone:c

        if another example is created then us-central1 is used again.
        if another instance is present in any group, the modulus operator restarts the zones from the start
        """
        c = 0
        total_instances = int(instance_per_group*instance_group_count)
        for instance_number in range(0,total_instances,instance_per_group):
            for n in range(0,instance_per_group): 
                instance(project_id,bucket,instance_name+str(c)+str(n),region[int(c%len(region))]+"-"+characters[int(n%zones)])
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
