import os
import numpy as np
import json
import params
from params import *
import datetime as dt

# {"2018-05-21 00:00:00": {"Year": "2018", "Month": "05", "Day": "21", "hour": "00", "minute": "00", "second": "00", "observation count": "27","Observations": {"G02": {"Type": "GPS", "Name": "02","Bands": { "freq1": "number xyz", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd"}}, "G03": {"Type": "GPS", "Name": "03","Bands": { "freq1": "number xyz", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd"}}
# }}}


# rinexline = np.loadtxt("rinexfiles/ABMF00GLP_R_20181410000_01D_30S_MO_Short.rnx", dtype=str)

rinexfilename = "rinexfiles/ABMF00GLP_R_20181410000_01D_30S_MO_Short.rnx"
# rinexfilename = "rinexfiles/ZAMB00ZMB_R_20200320000_01D_30S_MO_short.rnx"
rinexdict = {}  # dictionary to dump as json later
parameters = []
identifier = {"G": "GPS", "R": "GLONASS", "S": "SBAS", "E": "Galileo", "C": "BeiDou", "J": "QZSS"}
# global prn
anzahl = 0
satt = ""


def createtsdict(line):
    """
    creates dictionariy containing the timestamp data
    :param line: Rinex file line
    :return: None
    """


def channellog(line):
    """
    Decodes "SYS # Type" line
    :param line: One line starting with a capital letter of the sat type or a line containing channel information
    :return: PRN, number of different observed channels, type of satellite
    """
    prn = str(line[0])
    if prn != " ":
        numsat = int(line[1:6])
    else:
        numsat = anzahl % 13

    if prn == "G":
        sattype = GPS()
    elif prn == "R":
        sattype = GLONASS()
    elif prn == "S":
        sattype = SBAS()
    elif prn == "E":
        sattype = GALILEO()
    elif prn == "C":
        sattype = BEIDOU()
    elif prn == "J":
        sattype = QZSS()
    else:
        sattype = satt
        # print(prn)

    positions = numsat if numsat <= 13 else (abs((numsat % 13) - numsat))

    # erstelle eine lokale parameterliste, dann den buchstaben hinzufügen, dann werte anhängen.
    # anschließend in das objekt schreiben
    # repeat
    l = len(sattype.returnparams())

    if l == 0:
        # print(identifier[prn])
        sattype.addtype(identifier[prn])
        l += 1

    if l == 1:
        sattype.addnumsat(str(numsat))
        l += 1

    for i in range(positions):
        sattype.addband(str(line[7 + (i * 4):10 + (i * 4)]))

    print(sattype.returnparams())
    print(positions)
    return prn, numsat, sattype


def decodeepoch(line):
    """
    Lines starting with ">" are converted to a single string containing the date from year to seconds

    :param line: rinex file line starting with ">"
    :return: timestamp as string, number of observations (string)
    """
    timestamp = str(dt.datetime(int(line[2:6]), int(line[7:9]), int(line[10:12]), int(line[13:15]), int(line[16:18]),
                                int(line[19:21].strip())))
    cobs = str(line[33:35])
    return timestamp, cobs

def writetimeinfo(timestr):
    timedict = {}
    timedict["year"] = timestr[0:4]
    timedict["month"] = timestr[5:7]
    timedict["day"] = timestr[8:10]
    timedict["hour"] = timestr[11:13]
    timedict["minute"] = timestr[14:16]
    timedict["second"] = timestr[17:19]
    return timedict

def decodeobservation(line):
    pass


if __name__ == "__main__":
    timestamp = ""
    rinexFile = open(rinexfilename, "r")
    line = rinexFile.readline()
    while line[60:].rstrip() != "END OF HEADER":
        if line[60:].rstrip() == "PGM / RUN BY / DATE":
            if line[56:59].strip() != "UTC":
                print(f"Warning! Timezone is not UTC. Found: {line[56:59]}")
        if line[60:].rstrip() == "SYS / # / OBS TYPES":
            prn2, anzahl, satt = channellog(line)
        line = rinexFile.readline()

    line = rinexFile.readline()

    while True:
        if line[0:1] == ">":
            print("Found on Epoch")
            timestamp, obscount = decodeepoch(line)
            rinexdict[timestamp] = writetimeinfo(timestamp)
            rinexdict[timestamp]["observation count"] = obscount
            with open("results/output1.json", "w+") as jsonfile:
                json.dump(rinexdict, jsonfile)
        else:
            decodeobservation(line)
            rinexdict[timestamp] = {}
            pass
        line = rinexFile.readline()
