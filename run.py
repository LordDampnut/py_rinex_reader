import json
import sys
from params import *
import datetime as dt

# {"2018-05-21 00:00:00": {"Year": "2018", "Month": "05", "Day": "21", "hour": "00", "minute": "00", "second": "00", "observation count": "27","Observations": {"G02": {"Type": "GPS", "Name": "02","Bands": { "freq1": "number xyz", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd"}}, "G03": {"Type": "GPS", "Name": "03","Bands": { "freq1": "number xyz", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd", "freq2": "number asd"}}
# }}}

rinexfilename = "rinexfiles/ABMF00GLP_R_20181410000_01D_30S_MOasd.rnx"
# rinexfilename = "rinexfiles/ABMF00GLP_R_20181410000_01D_30S_MO_clipped.rnx"
# rinexfilename = "rinexfiles/ABMF00GLP_R_20181410000_01D_30S_MO_Short.rnx"
# rinexfilename = "rinexfiles/ZAMB00ZMB_R_20200320000_01D_30S_MO_short.rnx"
rinexdict = {}  # dictionary to dump as json later
svidentifier = {"G": "GPS", "R": "GLONASS", "S": "SBAS", "E": "GALILEO", "C": "BEIDOU", "J": "QZSS"}
anzahl = 0
satt = ""
timestamp = ""
argc = len(sys.argv)


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
        sattype.addtype(svidentifier[prn])
        l += 1

    if l == 1:
        sattype.addnumsat(str(numsat))
        l += 1

    for i in range(positions):
        sattype.addband(str(line[7 + (i * 4):10 + (i * 4)]))

    return prn, numsat, sattype


def decodeepoch(line):
    """
    Lines starting with ">" are converted to a single string containing the date from year to seconds

    :param line: rinex file line starting with ">"
    :return: timestamp as string, count of observations (string)
    """
    timestamp = str(dt.datetime(int(line[2:6]), int(line[7:9]), int(line[10:12]), int(line[13:15]), int(line[16:18]),
                                int(line[19:21].strip())))
    cobs = str(line[33:35])
    return timestamp, cobs


def writetimeinfo(timestr):
    """
    Takes a timestring from datetime and turns it into a dictionary
    :param timestr: timestring from datetime
    :return: dictionary in (yyyy-mm-dd hh:mm:ss)
    """
    timedict = {"year": timestr[0:4], "month": timestr[5:7], "day": timestr[8:10], "hour": timestr[11:13],
                "minute": timestr[14:16], "second": timestr[17:19]}
    return timedict


def decodeobservation(line):
    """

    :param line: One line containing Rinex observation data. Starting with three chars identifying the SV
    :return: Returns the letter and number identifying the SV e.g. 'G02'
    """
    identifier = line[0:3]  # e.g. "GO2"
    prnidentifier = line[0:1]  # e.g. "G"
    n = 0
    parameterlist = []
    if prnidentifier == "G":
        parameterlist = GPS().returnparams()[1:]
        n = parameterlist[0]
    elif prnidentifier == "R":
        parameterlist = GLONASS().returnparams()[1:]
        n = parameterlist[0]
    elif prnidentifier == "S":
        parameterlist = SBAS().returnparams()[1:]
        n = parameterlist[0]
    elif prnidentifier == "E":
        parameterlist = GALILEO().returnparams()[1:]
        n = parameterlist[0]
    elif prnidentifier == "C":
        parameterlist = BEIDOU().returnparams()[1:]
        n = parameterlist[0]
    elif prnidentifier == "J":
        parameterlist = QZSS().returnparams()[1:]
        n = parameterlist[0]
    else:
        print("Warning! Unknown Sat. identifier")
    codes = {}
    for i in range(len(parameterlist)):
        codes = {parameterlist[i]: line[0]}

    obsdict = {"type": svidentifier[prnidentifier], "prn": line[1:3], "codes": {}}
    return str(identifier), obsdict


def decodeline(line, n):
    """
    decodes one line to combine all observations in one list
    :param line: one observation line
    :return: list containing all observations including blanks space (hopefully)
    """
    templist = []
    for i in n:
        line[5:18].strip()

        templist.append(line)


def codelist(prn):
    """
    Takes a char and returns the observation codes

    :param prn: char describing the SV e.g. 'G' for GPS
    :return: List containing the previously analyzed transponder codes
    """
    if prn == "G":
        return GPS().returnparams()
    elif prn == "R":
        return GLONASS().returnparams()
    elif prn == "S":
        return SBAS().returnparams()
    elif prn == "E":
        return GALILEO().returnparams()
    elif prn == "C":
        return BEIDOU().returnparams()
    elif prn == "J":
        return QZSS().returnparams()
    else:
        pass


if __name__ == "__main__":

    if argc < 2:
        print("No arguments given, using example file.")
        jsonfilename = "example_output.json"
    else:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("\tCrude RINEX to JSON converter\n")
            print("\tThis decoder was tested with two 'mixed' type RINEX files version 3.02 and above!\n")
            print("\tUsage:\n")
            print("\trun.py [RINEX FILE or OPTION]")
            print("\tOption:\n")
            print("\t-h | --help    : print help")
            print("\tNote: Output filename will be input file name as .JSON file.\n")
            print("\tOutput file will be in the same folder as input file!\n")
            print("\tNote: for every row missing a value a print command with more info will be issued!\n")
            exit(0)

        rinexfilename = sys.argv[1]
        jsonfilename = rinexfilename[:-3] + "json"

    # timestamp = ""
    if rinexfilename[-3:] != "rnx":
        print("File format other than .rnx not supported")
        exit()

    try:
        rinexFile = open(rinexfilename, "r")
        line = rinexFile.readline()
    except FileNotFoundError:
        print("File could not be found!")
        exit()

    while line[60:].rstrip() != "END OF HEADER":
        if line[60:].rstrip() == "PGM / RUN BY / DATE":
            if line[56:59].strip() != "UTC":
                print(f"Warning! Timezone is not UTC. Found: {line[56:59]}")
        if line[60:].rstrip() == "SYS / # / OBS TYPES":
            prn2, anzahl, satt = channellog(line)
            # print(prn2, anzahl, satt.returnparams())
        line = rinexFile.readline()

    print("INFO! Header decoded.")

    line = rinexFile.readline()

    counter = 1
    cdict = {}
    while True:
        if line[0:1] == ">":  # Anfang der Eopche, gekennzeichnet mit ">"
            counter = 1
            timestamp, obscount = decodeepoch(line)
            rinexdict[timestamp] = writetimeinfo(timestamp)
            rinexdict[timestamp]["observation count"] = obscount
            rinexdict[timestamp]["observations"] = {}

        elif line[0:1] != "":  # eine Zeile der observation
            key, odict = decodeobservation(line)
            values = line[3:].rstrip().split(" ")
            values = [_ for _ in values if _ != '']
            codes = codelist(key[0])[2:]
            if len(values) == int(codelist(key[0])[1]):
                odict["codes"] = dict(zip(codes, values))
            else:
                print(f"Missing Values in epoch {timestamp} row {counter - 1}")

            rinexdict[timestamp]["observations"][key] = odict

        else:
            print("Writing output file, please wait...")
            with open(jsonfilename, "w+") as jsonfile:
                json.dump(rinexdict, jsonfile)
            print("Process finished.")
            exit(10)

        line = rinexFile.readline()
        counter += 1
