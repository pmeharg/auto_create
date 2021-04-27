#!/usr/bin/env python3

from pprint import pprint
import json
import requests
import argparse

username = "admin"  # Nexus IQ username
password = "Nexus!23"  # Nexus IQ password
uri = "localhost"  # Servername where IQ resides
port = str(8070)  # IQ port number
#org_name = "Ryan_Test_Org"
#app_name = "Ryan_Test_App"

parser = argparse.ArgumentParser(
    description='Applies an operation to one or more numbers'
)

parser.add_argument('-o', '--org_name',
                    help="The organization name to contain the new application.")
parser.add_argument("-i", "--app_id",
                    help="The AppId to create if not found.")

args = parser.parse_args()

org_name = args.org_name
app_name = args.app_id

org_list = []
org_count = 0
theurl = "http://%s:%s/api/v2/organizations" % (uri, port)
headers = {"Content-Type": "application/json"}
data = json.dumps({"name": org_name})
res_orgs = requests.get(theurl, data,  auth=(username, password), headers=headers)
json_data_orgs = json.loads(res_orgs.text)

for org_ids in json_data_orgs['organizations']:
    org_id_int = str(org_ids['id'])
    org_id_human = str(org_ids['name'])
    org_list.append(org_id_human)

# sort list and iterate through to find and print duplicate entries
org_list.sort()
print(org_list)
for i in range(0, len(org_list) - 1):
    if org_name == org_list[i]:
        org_count = org_count + 1
print("The org count is: ")
print(org_count)

# Create Org
theurl = "http://%s:%s/api/v2/organizations" % (uri, port)
#print(theurl)
if org_count == 0:
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"name": org_name})
    r = requests.post(theurl, data, auth=(username,password), headers=headers)
    #print(r.status_code)
    if str(r.status_code) == "200":
        print("Your Organisation was successfully added to Nexus IQ.")
    else:
        print("Error, un successful creation of Organisation int Nexus IQ. Check clm-server.log for further information")
        print(r)

if org_count > 0:
    print("The org already exists in Nexus IQ - continuing to application")

res_orgs = requests.get(theurl, data,  auth=(username, password), headers=headers)
json_data_orgs = json.loads(res_orgs.text)
#pprint(json_data_orgs)

for org_ids in json_data_orgs['organizations']:
    org_id_int = str(org_ids['id'])
    org_id_human = str(org_ids['name'])
    if org_id_human == org_name:
        #print(org_id_human, org_id_int)

        #Create the app
        theurl_app = "http://%s:%s/api/v2/applications/" % (uri,port)
        #print(theurl_app)
        # fetch report from uri
        res= requests.get(theurl_app, auth=(username,password))

        # Load result string to json
        json_data = json.loads(res.text)

        app_list =[]
        app_count = 0
        # iterate json
        for applications in json_data['applications']:

            test_line_output = str(applications['publicId'])
            #print test_line_output

            #create a list containing all the applications
            app_list.append(test_line_output)

        #sort list and iterate through to find and print duplicate entries
        app_list.sort()
        for i in range(0,len(app_list)-1):
            if app_name == app_list[i]:
                app_count = app_count+1

        if app_count > 0:
            print(app_name + ' is an exiting application - happy scanning!!! ')
        else:
            print(app_name + ' is not a existing IQ Server application ID....creating this for you now.')

            headers={"Content-Type": "application/json"}
            data = json.dumps({"publicId":app_name,"name":app_name,"organizationId": org_id_int})
            #print(data)
            r = requests.post(theurl_app, data, auth=(username,password), headers=headers)
            #print(r.status_code)
            if str(r.status_code) == "200":
                print("Your application was successfuly added to Nexus IQ under the " + org_id_human + " Organisation")
            else:
                print("Error, un sucessful load of application into Nexus IQ. Check clm-server.log for further information")
                print(r)

print('')
print('End')