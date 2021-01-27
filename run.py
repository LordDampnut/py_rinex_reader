import os
import numpy as np
import json
import params
from params import *

# rinexline = np.loadtxt("rinexfiles/ABMF00GLP_R_20181410000_01D_30S_MO_Short.rnx", dtype=str)
rinexfilename = "rinexfiles/ABMF00GLP_R_20181410000_01D_30S_MO_Short.rnx"

parameters = []
identifier = {"G": "GPS", "R": "GLONASS", "S": "SBAS", "E": "Galileo", "C": "BeiDou", "J": "QZSS"}
global prn
anzahl = 0
satt = ""


def channellog(line):
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


if __name__ == "__main__":

    rinexFile = open(rinexfilename, "r")
    line = rinexFile.readline()
    while line[60:].rstrip() != "END OF HEADER":
        if line[60:].rstrip() == "SYS / # / OBS TYPES":
            prn2, anzahl, satt = channellog(line)
        line = rinexFile.readline()
