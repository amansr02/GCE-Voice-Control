import sys
from flask import Flask, request, abort, jsonify
from create_instance import main
from create_instance import delete_instance
from create_groups import main as create_groups_main
from create_firewalls import main as create_firewalls_main
import json

app = Flask(__name__)

"""
    Documentation: Instance Create 
    for example
    region = [us-central1]
    zones = 2
    group-name = example
    instances_per_group = 3
    group_count = len(region)*zones

    Example0 region:us-central1
        - instance0 zone:a
        - instance1 zone:a
        - instance2 zone:a
    Example1 region:us-central1  
        - instance3 zone:b
        - instance4 zone:b
        - instance5 zone:b

    if another example is created then us-central1 is used again. [modulus operator]
    if another instance is present in any group, the modulus operator restarts the zones from the start [modulus operator]

"""

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
        instance_per_group = dictionary["queryResult"]["parameters"]["instance_per_group"]["number-integer"]

        instance_name = (project_id.split('-'))[0]
        characters = characters[0:zones]
        instance_group_count =  int(len(region)*zones)
        instance_group_name = instance_name

        #create instances
        zone_counter = 0
        region_counter = 0
        total_instances = int(instance_per_group*instance_group_count)
        for instance_number in range(0,total_instances,instance_per_group):
            for n in range(0,instance_per_group): 
                instance(project_id,bucket,instance_name+str(zone_counter)+str(n),region[int(region_counter%len(region))]+"-"+characters[int(zone_counter%zones)])
            zone_counter=zone_counter+1
            if zone_counter%zones==0:
               region_counter=region_counter+1 

        #Create group
        zone_counter = 0
        region_counter = 0
        for number in range(0,instance_group_count):
            group(project_id,bucket, region[int(region_counter%len(region))]+"-"+characters[int(zone_counter%zones)],
                    instance_name+str(number),instance_per_group,instance_group_count,instance_group_name+str(number))
            zone_counter=zone_counter+1
            if zone_counter%zones==0:
               region_counter=region_counter+1 

        #Create Firewall
        firewall = Firewall(project)
        firewall.firewall_all_execute()

        json_file="" 
        with open("payload.json") as j:
            json_file = json.load(j)
        return jsonify(json_file)

    else:
        print("hello")
        abort(400)

def instance(project,bucket,instance_name,zone):
    main(project,bucket,zone,instance_name)

def firewall(project,firewall_name,priority,direction,ip_ranges,protocols_ports):
    create_firewalls_main(project,firewall_name,priority,direction,ip_ranges,protocols_ports)

def group(project,bucket,zone,instance_name,instance_size,group_size,instance_group_name):
    create_groups_main(
            project=project,
            bucket=bucket,
            zone=zone,
            instance_templates = instance_name,
            instance_templates_size=instance_size,
            group_name = instance_group_name,group_size=group_size)

#Create instance templates. dont pass size. do create a while loop
#naming convention = example1,example2,example3
if __name__ == '__main__':
    app.run(host="127.0.0.1",port="80")
