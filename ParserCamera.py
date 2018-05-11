import sqlite3
import os
import plistlib
import datetime
import biplist
import re
import io
import json
import time
import sys

def try_parse_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val

# This is the path of selective backup files.
path = sys.argv[1]
output_path = sys.argv[2]
goose_path = os.path.join(output_path, 'goose.csv')

manifest_path = os.path.join(path, 'Manifest.db')
print (manifest_path)
info_path = os.path.join(path, 'Info.plist')
status_path = os.path.join(path, 'Status.plist')
#print(manifest_path)

sqlite_nest_fullpath = os.path.join(path, 'Nest.sqlite')   #c5
plist_nest_fullpath = os.path.join(path, 'com.nestlabs.jasper.release')  #cfe4cc
goose_fullpath = os.path.join(path, 'GooseEventLogging')

with open(info_path, 'rb') as f:
    info_plist = plistlib.load(f)

device_name = info_plist['Device Name']
phone_number = info_plist['Phone Number']
imei = info_plist['IMEI']
product_version = info_plist['Product Version']

with open(status_path, 'rb') as f:
    status_plist = plistlib.load(f)
status = status_plist['SnapshotState']
date_completion = status_plist['Date']

with open(goose_fullpath, 'rb') as f:
    goose_plist = biplist.readPlist(f)
#print(goose_plist)
num_objects = len(goose_plist['$objects'])
print("Number of objects:" , num_objects)

keys = set()
goose_events = []
for i in range(2, num_objects-1):
    matchObj = re.match(r'(\d\d-\d\d \d\d:\d\d:\d\d\.\d\d\d\d):(.*)', goose_plist['$objects'][i])
    jsonObj = json.loads(matchObj.group(2))

    for key in jsonObj.keys():
        keys.add(key)
    goose_events.append([matchObj.group(1),jsonObj])
with open(goose_path, "w") as f:
    f.write("timestamp|")
    for key in keys:
        f.write(key + "|")
    f.write("\n")
    for ev in goose_events:
        f.write(ev[0] + "|")
        for key in keys:
            if key in ev[1].keys():
                f.write(str(ev[1][key])+ "|")
            else:
                f.write("|")
        f.write("\n")

with sqlite3.connect(sqlite_nest_fullpath, uri=True) as conn:
    c = conn.cursor()
    c.execute("SELECT ZLATITUDE, ZLONGITUDE from ZCDGEOFENCE")
    result = c.fetchall()

    latitude = result[0][0]
    longitude = result[0][1]
    print("latitude: ", latitude,  " longitude: ", longitude)

    c.execute("SELECT ZNAME, ZUSER, ZEMAIL from ZCDUSERSESSION")
    result = c.fetchall()
    name = result[0][0]
    user = result[0][1]
    email = result[0][2]
    print("name: ", name, " user: ", user, " email: " , email)
    c.execute("SELECT ZCREATIONTIME, ZIP_ADDRESS, ZMAC_ADDRESS,"
              "ZIDENTIFIER, ZLAST_CONNECT_TIME, ZLAST_DISCONNECT_TIME from ZCDBASEDEVICE")
    result = c.fetchall()
    creation_time = result[0][0]
    ip_address = result[0][1]
    mac_address = result[0][2]
    identifier = result[0][3]
  
    last_connection_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((result[0][4]/1000)+(result[0][4]%1000)))
    last_disconnect_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((result[0][5]/1000)+(result[0][5]%1000)))
    print("creation_time: " , creation_time, "ip: " , ip_address, "macaddre:" , mac_address,  "identifier: ", identifier, " last_connection_time: ", last_connection_time, " last_disconnect:", last_disconnect_time )
    
    events = []
    c.execute("SELECT ZSTARTDATE, ZENDDATE"
              " from ZCDSCRUBBYCHUNKINFO")
    result = c.fetchall()
    for row in result:

        events.append({'starttime': (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[0]))),
                       'enddate': (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row[1]))), 'diff': (float("{0:.2f}".format((row[1]-row[0])/60)))} )


events = sorted(events, key=lambda k: k['starttime'])
for a in events:
    print(a)
