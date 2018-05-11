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
    def __init__(self, header1, header2, header3, table1_data, table2_data):
        """Constructor"""
        self.width, self.height = letter
        self.styles = getSampleStyleSheet()
        self.header1 = header1
        self.header2 = header2
        self.header3 = header3
        self.table1_data = table1_data
        self.table2_data = table2_data

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
        self.doc = SimpleDocTemplate(pdf_name)
        self.story = [Spacer(1, 0 * inch)]
        #self.createLineItems()
        self.story.append(Paragraph("PART-I", self.styles["Heading1"]))
        self.story.append(Paragraph("Section-1. iOS Device Information", self.styles["Heading2"]))
        self.story.append(Paragraph(header1, self.styles["Normal"]))
        self.story.append(Paragraph("Section-2. IoT Mobile Apps and User Information", self.styles["Heading2"]))
        self.story.append(Paragraph("Nest App:", self.styles["Heading3"]))
        self.story.append(Paragraph(header2, self.styles["Normal"]))
        self.story.append(Paragraph("Google Home App:", self.styles["Heading3"]))
        self.story.append(Paragraph(header3, self.styles["Normal"]))
        self.story.append(Paragraph("PART-II. Fence Report", self.styles["Heading1"]))
        self.createTable1()
        self.story.append(Paragraph("PART-III. Fence Report", self.styles["Heading1"]))
        self.createTable2()
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
        datetime_header = Paragraph('''<b>Logging Date/Time</b>''', styleBH)
        event_header = Paragraph('''<b>Event</b>''', styleBH)
        nettype_header = Paragraph('''<b>iOS Network</b>''', styleBH)
        internetconn_header = Paragraph('''<b>Internet Status</b>''', styleBH)
        inference_header = Paragraph('''<b>Inference</b>''', styleBH)

        report1data = []

        report1data = [[datetime_header, event_header, nettype_header, internetconn_header, inference_header]]

        for element in data:
            report1data.append([Paragraph(element[1], styleN),
                                Paragraph(element[2], styleN),
                                Paragraph(element[3], styleN),
                                Paragraph(element[4], styleN),
                                Paragraph(element[5], styleN)])

        report1table = Table(report1data, colWidths=[4.00 * cm, 2.7 * cm, 2.8 * cm,
                                                     3 * cm, 4 * cm])

        report1table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 1), 0.25, colors.black),
            #('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        self.story.append(report1table)

        # ----------------------------------------------------------------------
    def createTable2(self):
        data = self.table2_data
        styles = getSampleStyleSheet()
        styleN = styles["BodyText"]
        styleN.alignment = TA_LEFT
        styleBH = styles["Normal"]
        styleBH.alignment = TA_CENTER

        # Headers
        datetime_header = Paragraph('''<b>Event Date/Time</b>''', styleBH)
        event_header = Paragraph('''<b>Event</b>''', styleBH)
        triggeredBy_header = Paragraph('''<b>Event Triggered by</b>''', styleBH)
        inference_header = Paragraph('''<b>Inference</b>''', styleBH)

        report1data = []

        report1data = [[datetime_header, event_header, triggeredBy_header, inference_header]]

        for element in data:
            report1data.append([Paragraph(element[0], styleN),
                                Paragraph(element[1], styleN),
                                Paragraph(element[2], styleN),
                                Paragraph(element[3], styleN)])

        report1table = Table(report1data, colWidths=[5 * cm, 4 * cm, 3.5 * cm,
                                                     4 * cm])

        report1table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 1), 0.25, colors.black),
            # ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        self.story.append(report1table)

    # ----------------------------------------------------------------------
    def createDocument(self, canvas, doc):
        print("done!")

    # ----------------------------------------------------------------------



# ----------------------------------------------------------------------

def try_parse_int(s, base=10, val=None):
  try:
    return int(s, base)
  except ValueError:
    return val



path = sys.argv[1]
output_path = sys.argv[2]
old_goose_name = os.path.join(output_path, 'oldGoose.csv')
report1_name = os.path.join(output_path, 'report1.csv')
report2_name = os.path.join(output_path, 'report2.csv')
pdf_name = os.path.join(output_path, 'report.pdf')

print(path)
manifest_path = os.path.join(path, 'Manifest.db')
info_path = os.path.join(path, 'Info.plist')
status_path = os.path.join(path, 'Status.plist')


sqlite_nest_fullpath = os.path.join(path, 'Nest.sqlite')
plist_nest_fullpath = os.path.join(path, 'com.nestlabs.jasper.release.plist')
goose_fullpath = os.path.join(path, 'GooseEventLogging')
google_fullpath = os.path.join(path, 'com.google.Chromecast.plist')

if(len(sys.argv) > 3):
    if sys.argv[3] == "-b":
        with sqlite3.connect(manifest_path, uri=True) as conn:
            c = conn.cursor()
            sqlite_nest_relative_path = 'Documents/Nest.sqlite'
            sqlite_nest_domain = 'AppDomain-com.nestlabs.jasper.release'
            sqlite_nest_filename = ''
            c.execute("SELECT fileID FROM Files WHERE relativePath='{0}' AND domain='{1}'".format(sqlite_nest_relative_path, sqlite_nest_domain))
            sqlite_nest_filename = c.fetchone()[0]
            sqlite_nest_fullpath = os.path.join(path, sqlite_nest_filename[:2], sqlite_nest_filename)

            plist_nest_relative_path = 'Library/Preferences/com.nestlabs.jasper.release.plist'
            plist_nest_domain = 'AppDomain-com.nestlabs.jasper.release'
            plist_nest_filename = ''
            c.execute("SELECT fileID FROM Files WHERE relativePath='{0}' AND domain='{1}'".format(plist_nest_relative_path, plist_nest_domain))
            plist_nest_filename = c.fetchone()[0]
            plist_nest_fullpath = os.path.join(path, plist_nest_filename[:2], plist_nest_filename)

            goose_relative_path = 'Documents/GooseEventLogging'
            goose_domain = 'AppDomain-com.nestlabs.jasper.release'
            goose_filename = ''
            c.execute("SELECT fileID FROM Files WHERE relativePath='{0}' AND domain='{1}'".format(goose_relative_path,
                                                                                                  goose_domain))
            goose_filename = c.fetchone()[0]
            goose_fullpath = os.path.join(path, goose_filename[:2], goose_filename)

            google_relative_path = 'Library/Preferences/com.google.Chromecast.plist'
            google_domain = 'AppDomain-com.google.Chromecast'
            google_filename = ''
            c.execute("SELECT fileID FROM Files WHERE relativePath='{0}' AND domain='{1}'".format(google_relative_path,
                                                                                                  google_domain))
            google_filename = c.fetchone()[0]
            google_fullpath = os.path.join(path, google_filename[:2], google_filename)

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

num_objects = len(goose_plist['$objects'])
print("Number of objects:" , num_objects)

with open(google_fullpath, 'rb') as f:
    google_plist = biplist.readPlist(f)
    google_userID = google_plist["kGoogleAuthDefaultKeySSOIdentityUserID"]
    google_user_address = google_plist["AddressEntryDefault"]
    google_device_activation = google_plist["GRWUniversalMetricsFirstLaunchDateKey"]
    google_device_identifier = google_plist["com.google.sso.GeneratedDeviceIdentifier"]
    google_last_sync = google_plist["GRWMessagingCacheUserDefaultsKey"]["GRWCacheLastSyncDate"]
    google_last_logging = google_plist["com.google.cast.analytics_logging_last_api_usage_report_time"]

keys = set()
all_events = []
for i in range(2, num_objects-1):
    matchObj = re.match(r'(\d\d-\d\d \d\d:\d\d:\d\d\.\d\d\d\d):(.*)', goose_plist['$objects'][i])
    jsonObj = json.loads(matchObj.group(2))

    for key in jsonObj.keys():
        keys.add(key)
    all_events.append([matchObj.group(1), jsonObj])

relevantEvents = []
eventid  = 0
eventIndexList = []
for ev in all_events:
    if ev[1]["event"] == "FenceEvent":
        event = {}
        event["internet_status"] = "-"
        event["timestamp"] = ev[0]
        event["event"] = ev[1]["event"]
        event["type"] = ev[1]["type"]
        if "network_type" in ev[1]:
            event["network_type"] = ev[1]["network_type"]
        else:
            event["network_type"] = "-"
        relevantEvents.append(event)

        eventIndexList.append(eventid)
        eventid += 1

    elif ev[1]["event"] == "FenceReport":
        for i in eventIndexList:
            if ev[1]["network_type"] == "No Connection":
                relevantEvents[i]["internet_status"] = "Offline"
            else:
                relevantEvents[i]["internet_status"] = "Online"
        eventIndexList = []
        #flush


report1_rawdata = []

atHome = False
rowNo = 1
for event in relevantEvents:
    status = "Unknown"
    if(event["type"] == "ENTER"):
        if(atHome):
            status = "User is at home"
        else:
            status = "User arrived home"
            atHome = True
    elif(event["type"] == "EXIT"):
        if(atHome):
            status = "User left home"
            atHome = False
        else:
            status = "User is outside"
    report1_rawdata.append([str(rowNo),
                        event["timestamp"],
                        event["type"],
                        event["network_type"],
                        event["internet_status"],
                        str(status)])
    rowNo += 1


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

report2_rawdata = []
for event in events:
    thermo_inference = "None"
    thermo_user = "None"
    happened = "Set cool to " + str(event["cool_temperature"])
    if event["cool_temperature"] == 0.0:
        happened = "Set heat to " + str(event["heat_temperature"])
    if event["user"] is None:
        thermo_user = "Unknown"
        thermo_inference = "Manual Calibration"
    elif event["user"] == "Google Assistant":
        thermo_user = "Google Assistant"
        thermo_inference = "Voice command to Google Home"
    else:
        thermo_user = event["user"]
        thermo_inference = "A companion client was used"
    report2_rawdata.append([event["timestamp"],
                            happened,
                            thermo_user,
                            thermo_inference])


header1 = "Device Name: " + str(device_name) + "<br></br>"
header1 += "Phone Number:" + str(phone_number) + "<br></br>"
header1 += "IMEI Number:" + str(imei) + "<br></br>"
header1 += "iOS Version:" + str(product_version) + "<br></br>"
header1 += "App groups: (1) com.nestlabs.jasper.release (2) com.google.Chromecast" + "<br></br>"
header1 += "App analyzed: (1) Nest (2) com.google.Chromecast" + "<br></br>"
header1 += "Status of Backup: " + str(status_backup) + "<br></br>"
header1 += "Date of Backup: " + str(date_completion) + "<br></br>"

header2 = "User: " + str(user_name) + "<br></br>"
header2 += "User-ID: " + str(user_nest) + "<br></br>"
header2 += "User Address: " + str(email) + "<br></br>"
header2 += "IoT Device Activation Time: " + str(creation_time) + "<br></br>"
header2 += "IoT Device MAC Address: " + str(mac_address) + "<br></br>"
header2 += "IoT Device Identifier:: " + str(identifier) + "<br></br>"
header2 += "IoT Device Last Connection Time: " + str(last_connection_time) + "<br></br>"

header3 = "User-ID: " + str(google_userID) + "<br></br>"
header3 += "User Address: " + str(google_user_address) + "<br></br>"
header3 += "Device Activation Time: " + str(google_device_activation) + "<br></br>"
header3 += "Device Identifier: " + str(google_device_identifier) + "<br></br>"
header3 += "Last Sync Date/Time: " + str(google_last_sync) + "<br></br>"
header3 += "Last-known Logging API Usage: " + str(google_last_logging) + "<br></br><br></br>"

r = Report(header1, header2, header3, report1_rawdata, report2_rawdata)
r.run()