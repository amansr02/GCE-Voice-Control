# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import time
import googleapiclient.discovery
from six.moves import input

'''
protocols_ports = [ [tcp,[22]] , [tcp,[43,22]] ]
'''

def list_firewall(compute, project):
    result = compute.firewalls().list(project = project).execute()
    return result['items'] if 'items' in result else None

def create_firewall(compute,project,firewall_name,priority,direction,ip_ranges,protocols_ports,allow):

    allowed = []
    #print(protocols_ports)
    for item in protocols_ports:
        print(item) 
        allowed.append({
                "IPProtocol": item[0],
                "ports": item[1]
        })
    if(allow):
        body = { 
                "priority": priority,    
                "direction": direction, 
                "sourceRanges": ip_ranges,
                "allowed": allowed,
                "kind": "compute#firewall",     
                "logConfig": { 
                    "enable": True, 
                    },
                "disabled": False, 
                "name": firewall_name,
               }
    else:
        body = { 
                "priority": priority,    
                "direction": direction, 
                "sourceRanges": ip_ranges,
                "denied": allowed,
                "kind": "compute#firewall",     
                "logConfig": { 
                    "enable": True, 
                    },
                "disabled": False, 
                "name": firewall_name,
               }

    return compute.firewalls().insert(
        project=project,
        body=body).execute()


def delete_firewall(compute, project, firewall_name):
    return compute.firewalls().delete(
        project=project,
        firewall=firewall_name).execute()

def main(project,firewall_name, priority,direction,ip_ranges,protocols_ports,allow=True):

    compute = googleapiclient.discovery.build('compute', 'v1')

    print('Creating firewall')
    operation = create_firewall(compute,project,firewall_name,priority,direction,ip_ranges,protocols_ports,allow)

    firewalls = list_firewall(compute, project)

    print('Firewall in project %s:' % (project))
    for firewall in firewalls:
        print(' - ' + firewall['name'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument(
        'bucket_name', help='Your Google Cloud Storage bucket name.')
    parser.add_argument(
        '--zone',
        default='us-central1-f',
        help='Compute Engine zone to deploy to.')
    parser.add_argument(
        '--name', default='demo-instance', help='New instance name.')

    args = parser.parse_args()

    main(args.project_id, args.bucket_name, args.zone, args.name)



