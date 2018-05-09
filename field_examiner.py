import sqlite3
import os
import plistlib
import datetime
import biplist

path = "/home/manuel/Downloads/c5ad63c1c7304bbc53dcd4ac9b7a35060450f8e7"

keywords = ["device_id",
            "software_version",
            "structure_id",
            "where_id",
            "where_name",
            "public_share_url",
            "name_long",
            "is_online",
            "is_streaming",
            "app_url",
            "is_audio_input_enabled",
            "is_public_share_enabled",
            "is_video_history_enabled",
            "name",
            "last_is_online_change",
            "snapshot_url",
            "last_event"]

with sqlite3.connect(path, uri=True) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for tablerow in cursor.fetchall():
        table = tablerow[0]
        cursor.execute("SELECT * FROM {t}".format(t=table))
        for row in cursor:
            for field in row.keys():
                for keyword in keywords:
                    if keyword in str(field).lower():
                        print("Keyword:", keyword)
                        print("Found in fieldname")
                        print(table, field, row[field])
                        print()
                for keyword in keywords:
                    if keyword in str(row[field]).lower():
                        print("Keyword:", keyword)
                        print("Found in value")
                        value = row[field]
                        if "bplist" in str(row[field]):
                            value = biplist.readPlistFromString(row[field])
                        print(table, field, value)
                        print()


    # c = conn.cursor()
    #
    # # c.execute("SELECT ZADDRESS_LINES, ZFABRIC_IDS, ZGEOFENCE_ENHANCED_AUTOAWAY, ZMEMBERS, ZRCS_SENSOR_SWARM, "
    # #           "ZSWARM FROM ZCDSTRUCTURE")
    # # res = c.fetchone()
    # # ZADDRESS_LINES = biplist.readPlistFromString(res[0])
    # # print(ZADDRESS_LINES)
    # # ZFABRIC_IDS = biplist.readPlistFromString(res[1])
    # # print(ZFABRIC_IDS)
    # # ZGEOFENCE_ENHANCED_AUTOAWAY = biplist.readPlistFromString(res[2])
    # # print(ZGEOFENCE_ENHANCED_AUTOAWAY)
    # # ZMEMBERS = biplist.readPlistFromString(res[3])
    # # print(ZMEMBERS)
    # # ZRCS_SENSOR_SWARM = biplist.readPlistFromString(res[4])
    # # print(ZRCS_SENSOR_SWARM)
    # # ZSWARM = biplist.readPlistFromString(res[5])
    # # print(ZSWARM)
    #
    # c.execute("SELECT ZOBJECTVALUE FROM ZNLTRANSPORTOBJECT")
    # res = c.fetchone()[0]
    # ZOBJECTVALUE = biplist.readPlistFromString(res)
    # print(ZOBJECTVALUE)

