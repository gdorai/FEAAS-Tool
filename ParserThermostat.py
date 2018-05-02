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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER
from reportlab.lib.units import  inch, mm
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, SimpleDocTemplate
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors

class Report(object):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, header1, header2, table1_data):
        """Constructor"""
        self.width, self.height = letter
        self.styles = getSampleStyleSheet()
        self.header1 = header1
        self.header2 = header2
        self.table1_data = table1_data

    # ----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        """
        http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        """
        x, y = x * unit, self.height - y * unit
        return x, y

    # ----------------------------------------------------------------------
    def run(self):
        """
        Run the report
        """
        self.doc = SimpleDocTemplate("test.pdf")
        self.story = [Spacer(1, 0 * inch)]
        #self.createLineItems()
        self.story.append(Paragraph(header1, self.styles["Normal"]))
        self.story.append(Paragraph(header2, self.styles["Normal"]))
        self.createTable1()
        #self.story.append(report1table)
        self.doc.build(self.story, onFirstPage=self.createDocument)
        print("finished!")

    # ----------------------------------------------------------------------
    def createTable1(self):
        data = self.table1_data
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER

        # Headers
        index_header = Paragraph('''<b>S.No.</b>''', styleBH)
        datetime_header = Paragraph('''<b>LOGGING DATE/TIME </b>''', styleBH)
        event_header = Paragraph('''<b>EVENT</b>''', styleBH)
        nettype_header = Paragraph('''<b>NETWORK TYPE</b>''', styleBH)
        inference_header = Paragraph('''<b>INFERENCE</b>''', styleBH)

        report1data = []

        report1data = [[index_header, datetime_header, event_header, nettype_header, inference_header]]

        for element in data:
            report1data.append([Paragraph(element[0], styleN),
                                Paragraph(element[1], styleN),
                                Paragraph(element[2], styleN),
                                Paragraph(element[3], styleN),
                                Paragraph(element[4], styleN)])

        report1table = Table(report1data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,
                                                     3 * cm, 3 * cm])

        report1table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        self.story.append(report1table)

    # ----------------------------------------------------------------------
    def createDocument(self, canvas, doc):
        print("done!")
        #"""
        #Create the document
        #"""
        # self.c = canvas
        # normal = self.styles["Normal"]
        #
        # header_text = "<b>This is a test header</b>"
        # p = Paragraph(header_text, normal)
        # p.wrapOn(self.c, self.width, self.height)
        # p.drawOn(self.c, *self.coord(100, 12, mm))
        #
        # ptext = """text"""
        #
        # p = Paragraph(ptext, style=normal)
        # p.wrapOn(self.c, self.width - 50, self.height)
        # p.drawOn(self.c, 30, 700)
        #
        # story.append(self.table)

        # ptext = """
        # At vero eos et accusamus et iusto odio dignissimos ducimus qui
        # blanditiis praesentium voluptatum deleniti atque corrupti quos dolores
        # et quas molestias excepturi sint occaecati cupiditate non provident,
        # similique sunt in culpa qui officia deserunt mollitia animi, id est laborum
        # et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio.
        # Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit
        # quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est,
        # omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut
        # rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et
        # molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus,
        # ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis
        # doloribus asperiores repellat.
        # """
        # p = Paragraph(ptext, style=normal)
        # p.wrapOn(self.c, self.width - 50, self.height)
        # p.drawOn(self.c, 30, 600)

    # ----------------------------------------------------------------------



# ----------------------------------------------------------------------

def try_parse_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val


#/home/manuel/Documents/forensics/17f7a8e8b387625472b32d4361250568b164c504/
#path = os.path.join('sandbox', '17f7a8e8b387625472b32d4361250568b164c504')
#path = '/sandbox/17f7a8e8b387625472b32d4361250568b164c504/'

path = sys.argv[1] #'/home/manuel/Documents/forensics/iotfolder/8c75768ed100ac467a83e7a8684a392e3b3b671a'
print(path)
manifest_path = os.path.join(path, 'Manifest.db')
info_path = os.path.join(path, 'Info.plist')
status_path = os.path.join(path, 'Status.plist')
#print(manifest_path)

with sqlite3.connect(manifest_path, uri=True) as conn:
    c = conn.cursor()

    sqlite_nest_relative_path = 'Documents/Nest.sqlite'
    sqlite_nest_domain = 'AppDomain-com.nestlabs.jasper.release'
    sqlite_nest_filename = ''
    c.execute("SELECT fileID FROM Files WHERE relativePath='{0}' AND domain='{1}'".format(sqlite_nest_relative_path, sqlite_nest_domain))
    sqlite_nest_filename = c.fetchone()[0]
    sqlite_nest_fullpath = os.path.join(path, sqlite_nest_filename[:2], sqlite_nest_filename)
    #print(sqlite_nest_fullpath)

    plist_nest_relative_path = 'Library/Preferences/com.nestlabs.jasper.release.plist'
    plist_nest_domain = 'AppDomain-com.nestlabs.jasper.release'
    plist_nest_filename = ''
    c.execute("SELECT fileID FROM Files WHERE relativePath='{0}' AND domain='{1}'".format(plist_nest_relative_path, plist_nest_domain))
    plist_nest_filename = c.fetchone()[0]
    plist_nest_fullpath = os.path.join(path, plist_nest_filename[:2], plist_nest_filename)
    #print(plist_nest_fullpath)

    goose_relative_path = 'Documents/GooseEventLogging'
    goose_domain = 'AppDomain-com.nestlabs.jasper.release'
    goose_filename = ''
    c.execute("SELECT fileID FROM Files WHERE relativePath='{0}' AND domain='{1}'".format(goose_relative_path,
                                                                                          goose_domain))
    goose_filename = c.fetchone()[0]
    goose_fullpath = os.path.join(path, goose_filename[:2], goose_filename)

with open(info_path, 'rb') as f:
    info_plist = plistlib.load(f)

device_name = info_plist['Device Name']
phone_number = info_plist['Phone Number']
imei = info_plist['IMEI']
product_version = info_plist['Product Version']

with open(status_path, 'rb') as f:
    status_plist = plistlib.load(f)
status_backup = status_plist['SnapshotState']
date_completion = status_plist['Date']

with open(goose_fullpath, 'rb') as f:
    goose_plist = biplist.readPlist(f)
#print(goose_plist)
num_objects = len(goose_plist['$objects'])
print("Number of objects:" , num_objects)

#jsonObjs = list()
keys = set()
goose_events = []
for i in range(2, num_objects-1):
    matchObj = re.match(r'(\d\d-\d\d \d\d:\d\d:\d\d\.\d\d\d\d):(.*)', goose_plist['$objects'][i])
    jsonObj = json.loads(matchObj.group(2))

    for key in jsonObj.keys():
        keys.add(key)
    goose_events.append([matchObj.group(1),jsonObj])
with open("goose.csv", "w") as f:
    f.write("timestamp|")
    for key in keys:
        f.write(key + "|")
    f.write("\n")
    for ev in goose_events:
        f.write(ev[0] + "|")
        for key in keys:
            if key in ev[1].keys():
                #print(ev[1][key])
                f.write(str(ev[1][key])+ "|")
            else:
                f.write("|")
        f.write("\n")

relevantEvents = []
for ev in goose_events:
    if ev[1]["event"] == "FenceEvent":
        event = {}
        event["timestamp"] = ev[0]
        event["event"] = ev[1]["event"]
        event["type"] = ev[1]["type"]
        if "network_type" in ev[1]:
            event["network_type"] = ev[1]["network_type"]
        else:
            event["network_type"] = "-"
        relevantEvents.append(event)

report1_rawdata = []

with open("report1.csv", "w") as f:
    f.write("S.No.|")
    f.write("LOGGING DATE/TIME|")
    f.write("EVENT|")
    f.write("NETWORK TYPE|")
    f.write("INFERENCE\n")
    rowNo = 1
    for event in relevantEvents:
        f.write(str(rowNo) + "|")
        f.write(event["timestamp"] + "|")
        status = "Unknown"
        if(event["type"] == "ENTER"):
            status = "User is at home"
        elif(event["type"] == "EXIT"):
            status = "User left home"
        f.write(event["type"] + "|")
        f.write(event["network_type"] + "|")
        f.write(status + "\n")
        #f.write(event["event"] + "\n")
        report1_rawdata.append([str(rowNo),
                            event["timestamp"],
                            event["type"],
                            event["network_type"],
                            str(status)])
        # report1data.append([Paragraph(str(rowNo), styleN),
        #                     Paragraph(event["timestamp"], styleN),
        #                     Paragraph(event["type"], styleN),
        #                     Paragraph(event["network_type"], styleN),
        #                     Paragraph(str(status), styleN)])
        rowNo += 1

# report1table = Table(report1data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,
#                                              3 * cm, 3 * cm])
#
# report1table.setStyle(TableStyle([
#     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
#     ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
# ]))


#print(relevantEvents)
with sqlite3.connect(sqlite_nest_fullpath, uri=True) as conn:
    c = conn.cursor()
    c.execute("SELECT ZLATITUDE, ZLONGITUDE from ZCDGEOFENCE")
    result = c.fetchall()

    latitude = result[0][0]
    longitude = result[0][1]

    c.execute("SELECT ZNAME, ZUSER, ZEMAIL from ZCDUSERSESSION")
    result = c.fetchall()
    user_name = result[0][0]
    user_nest = result[0][1]
    email = result[0][2]

    c.execute("SELECT ZCREATIONTIME, ZLASTIPADDRESS, ZMAC_ADDRESS, ZLOCALIPADDRESS,"
              "ZIDENTIFIER, ZLASTCONNECTIONTIME, ZIDENTIFIER, ZDIAMONDBACKPLATESERIALNUMBER from ZCDBASEDEVICE")
    result = c.fetchall()
    creation_time = result[0][0]
    last_ip = result[0][1]
    mac_address = result[0][2]
    local_ip = result[0][3]
    identifier = result[0][4]
    last_connection_time = result[0][5]
    serialNumberDisplay = result[0][6]
    serialNumberBase = result[0][7]

    # events = []
    # c.execute("SELECT ZTOUCHEDAT, ZTEMPERATURE, ZTOUCHEDUSERID, ZSETPOINTTYPE, ZTIME"
    #           " from ZCDSCHEDULESETPOINT")
    # result = c.fetchall()
    # for row in result:
    #     events.append({'timestamp': datetime.datetime.fromtimestamp(int(row[0])).strftime("%c"),
    #                    'datetime': datetime.datetime.fromtimestamp(int(row[0])),
    #                    'temperature': row[1],
    #                    'user' : row[2],
    #                    'type': row[3],
    #                    'time': str(datetime.timedelta(seconds=int(row[4])))})

    events = []
    c.execute("SELECT ZTOUCHEDWHEN, ZCOOLTEMP, ZHEATTEMP, ZTOUCHEDID"
              " from ZCDENERGYEVENT")
    result = c.fetchall()
    for row in result:
        events.append({'timestamp': (datetime.datetime.fromtimestamp(int(row[0]))).strftime("%c"),
                       'datetime': datetime.datetime.fromtimestamp(int(row[0])),
                       'cool_temperature': row[1],
                       'heat_temperature': row[2],
                       'user': row[3]})

events = sorted(events, key=lambda k: k['datetime'])
#print(events)
with open("report2.csv", "w") as f:
    f.write("S.No.|")
    f.write("EVENT DATE/TIME|")
    # f.write("BY (‘user’)|")
    f.write("TYPE OF EVENT|")
    f.write("INFERENCE|")
    f.write("EVENT PERFORMED USING\n")
    rowNo = 1
    for event in events:
        f.write(str(rowNo) + "|")
        f.write(event["timestamp"] + "|")
        f.write("Set cool to " + str(event["cool_temperature"]) + " or heat to " + str(event["heat_temperature"]) + "|")
        f.write("|")
        user = "-"
        if event["user"] != None:
            user = event["user"]
        f.write(user + "\n")
        rowNo += 1



header1 = "Device Name: " + str(device_name) + "<br></br>"
header1 += "Phone Number:" + str(phone_number) + "<br></br>"
header1 += "IMEI Number:" + str(imei) + "<br></br>"
header1 += "iOS Version:" + str(product_version) + "<br></br>"
header1 += "App groups: (1) com.nestlabs.jasper.release (2) com.google.Chromecast" + "<br></br>"
header1 += "App analyzed: (1) Nest (2) com.google.Chromecast" + "<br></br>"
header1 += "Status of Backup: " + str(status_backup) + "<br></br>"
header1 += "Date of Backup: " + str(date_completion) + "<br></br>"

header2 = "<br></br>User: " + str(user_name) + "<br></br>"
header2 += "User-ID: " + str(user_nest) + "<br></br>"
header2 += "User Address: " + str(email) + "<br></br>"
header2 += "IoT Device Activation Time: " + str(creation_time) + "<br></br>"
header2 += "IoT Device MAC Address: " + str(mac_address) + "<br></br>"
header2 += "IoT Device Identifier:: " + str(identifier) + "<br></br>"
header2 += "IoT Device Last Connection Time: " + str(last_connection_time) + "<br></br>"


r = Report(header1, header2, report1_rawdata)
r.run()