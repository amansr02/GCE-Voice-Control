from create_groups import main as create_groups_main
from create_instance import main as create_instance_main
from create_firewalls import main as create_firewalls_main


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
    
    #Creating a test firewall

    #frontend
    priority = 1000
    direction = "Ingress"
    firewall_name = "frontend"
    ip_ranges = ["10.48.0.0/14"]
    protocols_ports = [ ["tcp", [80]]]
    create_firewalls_main(
            project = project,
            firewall_name = firewall_name,
            priority = priority,
            direction = direction,
            ip_ranges = ip_ranges,
            protocols_ports = protocols_ports
    )

    #http-hc2
    priority = 1000
    direction = "Ingress"
    firewall_name = "http-hc2"
    ip_ranges = ["209.85.152.0/22","209.85.204.0/22","130.211.0.0/22","35.191.0.0/16"]
    protocols_ports = [ ["tcp",[10256]] ]    
    create_firewalls_main(
            project = project,
            firewall_name = firewall_name,
            priority = priority,
            direction = direction,
            ip_ranges = ip_ranges,
            protocols_ports = protocols_ports
    )

    #vms
    priority = 1000
    direction = "Ingress"
    firewall_name = "vms"
    ip_ranges = ["10.128.0.0/9"]
    protocols_ports = [ ["icmp",[]], ["tcp",["1-65535"]], [ "udp",["1-65535"] ]]
    create_firewalls_main(
            project = project,
            firewall_name = firewall_name,
            priority = priority,
            direction = direction,
            ip_ranges = ip_ranges,
            protocols_ports = protocols_ports
    )
        
    #ssh
    priority = 1000
    direction = "Ingress"
    firewall_name = "ssh"
    ip_ranges = ["34.67.122.10/32","34.67.180.217/32","35.223.12.84/32"]
    protocols_ports  = [["tcp",["22"]]]
    create_firewalls_main(
            project = project,
            firewall_name = firewall_name,
            priority = priority,
            direction = direction,
            ip_ranges = ip_ranges,
            protocols_ports = protocols_ports
    )

if(__name__ == '__main__'):
    main()

