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

"""Example of using the Compute Engine API to create and delete instances.
Creates a new compute engine instance and uses it to apply a caption to
an image.
    https://cloud.google.com/compute/docs/tutorials/python-guide
For more information, see the README.md under /compute.
"""

import argparse
import os
import time
import googleapiclient.discovery
import json
from six.moves import input


# [START create_instance]
def create_group(compute, project,group_size,zone, name, bucket):
    # Get the latest Debian Jessie image.
    zone_resource = compute.zones().get(project = project, zone=zone).execute()
    zone_url = zone_resource['selfLink']
    region = compute.regions().get(project = project , region = zone[:len(zone)-2]).execute()
    region_url = region['selfLink']
    # Configure the machine
    machine_type = "zones/%s/machineTypes/n1-standard-1" % zone
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"

    config = { # Represents an Instance Group resource.
                # 
                # Instance Groups can be used to configure a target for load balancing.
                # 
                # Instance groups can either be managed or unmanaged.
                # 
                # To create  managed instance groups, use the instanceGroupManager or regionInstanceGroupManager resource instead.
                # 
                # Use zonal unmanaged instance groups if you need to apply load balancing to groups of heterogeneous instances or if you need to manage the instances yourself. You cannot create regional unmanaged instance groups.
                # 
                # For more information, read Instance groups.
                # 
                # (== resource_for {$api_version}.instanceGroups ==) (== resource_for {$api_version}.regionInstanceGroups ==)
                "size": group_size, # [Output Only] The total number of instances in the instance group.
                "kind": "compute#instanceGroup", # [Output Only] The resource type, which is always compute#instanceGroup for instance groups.
                "zone": zone_url, # [Output Only] The URL of the zone where the instance group is located (for zonal resources).
                "region": region_url, # [Output Only] The URL of the region where the instance group is located (for regional resources).
                "name": name, # The name of the instance group. The name must be 1-63 characters long, and comply with RFC1035.
            }

    return compute.instanceGroups().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]


# [START delete_instance]
def delete_group(compute, project, zone, name):
    return compute.instanceGroups().delete(
        project=project,
        zone=zone,
        instanceGroup=name).execute()
# [END delete_instance]


# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)

# [END wait_for_operation]
def add_instances(compute,project, zone, name,size,instance_name):
    l = []
    for number in range(0,size):
        if(number == 0):
            url = compute.instances().get(project = project,zone = zone,instance= instance_name+str(number)).execute()
            url = url["selfLink"]
            l.append({"instance":url})
        else:
            url = compute.instances().get(project = project,zone=zone,instance= instance_name+str(number)).execute()
            url = url["selfLink"]
            l.append({"instance": url})
    config ={
        "instances":l
    }
    config1 = {


    }
    return compute.instanceGroups().addInstances(project=project, zone = zone, instanceGroup=name , body = config).execute()

# [START run]
def main(project, bucket, zone, instance_templates, instance_templates_size , group_name, group_size,wait=True):
    compute = googleapiclient.discovery.build('compute', 'v1')

    print('Creating instance groups.')

    operation = create_group(compute, project,group_size,zone, group_name, bucket)
    wait_for_operation(compute, project, zone, operation['name'])

    print("adding templates")
    operation = add_instances(compute,project,zone,group_name,instance_templates_size,instance_templates)

    print("""
Group created.
It will take a minute or two for the instance to complete work.
Check this URL: http://storage.googleapis.com/{}/output.png
Once the image is uploaded press enter to delete the instance.
""".format(bucket))

    #if wait:
    #    input()

    #print('Deleting instance.')

    #operation = delete_group(compute, project, zone, group_name)
    #wait_for_operation(compute, project, zone, operation['name'])


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
# [END run]

