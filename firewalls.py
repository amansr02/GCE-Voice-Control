#https://www.digitalocean.com/community/tutorials/iptables-essentials-common-firewall-rules-and-commands

from create_firewalls import main as create_firewalls_main

class Firewall:

    def __init__(self,project,
                 firewall_name=None,
                 priority=None,
                 direction=None,
                 ip_ranges=None,
                 protocols_ports=None,
                 allow=None):
        self.project = project
        self.firewall_name = firewall_name
        self.priority = priority
        self.direction = direction
        self.ip_ranges = ip_ranges
        self.protocols_ports = protocols_ports
        self.allow = allow

    def firewall_all_outgoing(self):
        priority = 1000
        direction = "Egress"
        firewall_name = "firewall-all-outgoing"
        ip_ranges = []
        protocols_ports = [ ["all", ""] ]
        create_firewalls_main(
                project = self.project,
                firewall_name = firewall_name,
                priority = priority,
                direction = direction,
                ip_ranges = ip_ranges,
                protocols_ports = protocols_ports
        )

    def firewall_ssh_incoming(self):
        priority = 1000
        direction = "Ingress"
        firewall_name = "firewall-ssh-incoming"
        ip_ranges = []
        protocols_ports  = [["tcp",["22"]]]
        create_firewalls_main(
                project = self.project,
                firewall_name = firewall_name,
                priority = priority,
                direction = direction,
                ip_ranges = ip_ranges,
                protocols_ports = protocols_ports
        )

    def firewall_https_incoming(self):
        priority = 1000
        direction = "Ingress"
        firewall_name = "firewall-https-incoming"
        ip_ranges = []
        protocols_ports = [ ["tcp", [80]], ["tcp",[10256]], ["tcp",[443]] ]
        create_firewalls_main(
                project = self.project,
                firewall_name = firewall_name,
                priority = priority,
                direction = direction,
                ip_ranges = ip_ranges,
                protocols_ports = protocols_ports
        )
    
    def firewall_imaps_incoming(self):
        priority = 1000
        direction = "Ingress"
        firewall_name = "firewall-imap-incoming"
        ip_ranges = []
        protocols_ports = [ ["tcp", [143]],["tcp",[993]] ]
        create_firewalls_main(
                project = self.project,
                firewall_name = firewall_name,
                priority = priority,
                direction = direction,
                ip_ranges = ip_ranges,
                protocols_ports = protocols_ports
        )
    def firewall_pop3s_incoming(self):
        priority = 1000
        direction = "Ingress"
        firewall_name = "firewall-pop3s-incoming"
        ip_ranges = []
        protocols_ports = [ ["tcp", [110]],["tcp",[995]] ]
        create_firewalls_main(
                project = self.project,
                firewall_name = firewall_name,
                priority = priority,
                direction = direction,
                ip_ranges = ip_ranges,
                protocols_ports = protocols_ports
        )

    def firewall_all_deny(self):
        priority = 999
        direction = "Ingress"
        firewall_name = "firewall-alldeny-incoming"
        ip_ranges = []
        protocols_ports = [ ["all",""] ]
        create_firewalls_main(
                project = self.project,
                firewall_name = firewall_name,
                priority = priority,
                direction = direction,
                ip_ranges = ip_ranges,
                protocols_ports = protocols_ports,
                allow = False
        )

    def firewall_all_execute(self):
        self.firewall_https_incoming()
        self.firewall_imaps_incoming()
        self.firewall_pop3s_incoming()
        self.firewall_all_deny()

    def custom_firewall(self):
        create_firewalls_main(
                project = self.project,
                firewall_name = self.firewall_name,
                priority = self.priority,
                direction = self.direction,
                ip_ranges = self.ip_ranges,
                protocols_ports = self.protocols_ports,
                allow = self.allow
        )
        
