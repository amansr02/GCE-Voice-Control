from create_groups import main as create_groups_main
from create_instance import main as create_instance_main
from create_templates import main as create_templates_main


def main():
    #testing instance
    project = "sodium-gateway-267900"
    bucket = "gs://"+project+".appspot.com"
    zone = "us-central1-a"
    instance_name = "example"
    #create_instance_main(project = project,bucket = bucket,zone = zone,instance_name = instance_name)

    #testing templates

    create_templates_main(project = project,bucket=bucket,instance_name=instance_name,zone=zone)
    
    #testing groups
    #create_groups_main()



if(__name__ == '__main__'):
    main()

