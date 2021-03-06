from create_groups import main as create_groups_main
from create_instance import main as create_instance_main
from create_firewalls import main as create_firewalls_main
from firewalls import Firewall

def main():
    #testing instance
    project = "sodium-gateway-267900"
    bucket = "gs://"+project+".appspot.com"
    zone = "us-central1-a"
    instance_name = "example"
    #create_instance_main(project = project,bucket = bucket,zone = zone,instance_name = instance_name)

    #testing templates
    #create_templates_main(project = project,bucket=bucket,instance_name=instance_name,zone=zone)
    
    #testing groups
    #create_groups_main(
    #        project=project,
    #        bucket=bucket,
    #        zone=zone,
    #        instance_templates = instance_name,
    #        instance_templates_size=1,
    #        group_name = instance_name+"-group",group_size=1)
    firewall = Firewall(project=project)
    firewall.firewall_all_execute()
    
if(__name__ == '__main__'):
    main()

