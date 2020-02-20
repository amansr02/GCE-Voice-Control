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
        instance_template_name = dictionary["queryResult"]["parameters"]["Instance_Template_name"]
        instance_template_size =  dictionary["queryResult"]["parameters"]["Instance_Template_Size"]["number-integer"]
        region = dictionary["queryResult"]["parameters"]["Master-Region"]
        zones = dictionary["queryResult"]["parameters"]["Zone"]
        instance_group_name = dictionary["queryResult"]["parameters"]["Instance_Group_name"]
        group_size=  dictionary["queryResult"]["parameters"]["Master-Instance_Group_Count"]["number-integer"]
        instance_size = dictionary["queryResult"]["parameters"]["Master-Instance_Count"]["number-integer"]
        instance_name = instance_template_name

        #Create Template
        #create for loop and change instance_name
        for number in range(0,(instance_template_size)):
            template(project,bucket,"asdkbad",instance_template_name+str(number))

        #Create Instance
        #create for loop and change instance_name
        c = 0
        x = (instance_size*group_size)//len(zones)
        for number in range(0,int(instance_size*group_size),int(x)):
            for n in range(0,int(x)): 
                instance(project,bucket,instance_name+str(number+n),region+"-"+zones[c])
        c=c+1

        #Create group
        for number in range(0,group_size):
            group(project,bucket,region+"-"+zones[number],instance_name,instance_size,instance_size)

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
            instance_templates_size=1,
            group_name = instance_name+"-group",group_size=group_size)

#Create instance templates. dont pass size. do create a while loop
#naming convention = example1,example2,example3


if __name__ == '__main__':
    app.run(host="127.0.0.1",port="80")
