class GPS:
    parameters = []
    type = ""

    def __init__(self):
        pass

    def addtype(self, type):
        self.parameters.append(type)

    def addnumsat(self, numsat):
        self.parameters.append(numsat)

    def addband(self, band):
        self.parameters.append(band)

    """def appendparameters(self, numsat, band):
        self.parameters.append(numsat)
        self.parameters.append(band)
    """

    def returnparams(self):
        return self.parameters


class GLONASS:
    parameters = []
    type = ""

    def __init__(self):
        pass

    def addtype(self, type):
        self.parameters.append(type)

    def addnumsat(self, numsat):
        self.parameters.append(numsat)

    def addband(self, band):
        self.parameters.append(band)

    """def appendparameters(self, numsat, band):
        self.parameters.append(numsat)
        self.parameters.append(band)
    """

    def returnparams(self):
        return self.parameters


class SBAS:
    parameters = []
    type = ""

    def __init__(self):
        pass

    def addtype(self, type):
        self.parameters.append(type)

    def addnumsat(self, numsat):
        self.parameters.append(numsat)

    def addband(self, band):
        self.parameters.append(band)

    """def appendparameters(self, numsat, band):
        self.parameters.append(numsat)
        self.parameters.append(band)
    """

    def returnparams(self):
        return self.parameters


class GALILEO:
    parameters = []
    type = ""

    def __init__(self):
        pass

    def addtype(self, type):
        self.parameters.append(type)

    def addnumsat(self, numsat):
        self.parameters.append(numsat)

    def addband(self, band):
        self.parameters.append(band)

    """def appendparameters(self, numsat, band):
        self.parameters.append(numsat)
        self.parameters.append(band)
    """

    def returnparams(self):
        return self.parameters


class BEIDOU:
    parameters = []
    type = ""

    def __init__(self):
        pass

    def addtype(self, type):
        self.parameters.append(type)

    def addnumsat(self, numsat):
        self.parameters.append(numsat)

    def addband(self, band):
        self.parameters.append(band)

    """def appendparameters(self, numsat, band):
        self.parameters.append(numsat)
        self.parameters.append(band)
    """

    def returnparams(self):
        return self.parameters


class QZSS:
    parameters = []
    type = ""

    def __init__(self):
        pass

    def addtype(self, type):
        self.parameters.append(type)

    def addnumsat(self, numsat):
        self.parameters.append(numsat)

    def addband(self, band):
        self.parameters.append(band)

    """def appendparameters(self, numsat, band):
        self.parameters.append(numsat)
        self.parameters.append(band)
    """

    def returnparams(self):
        return self.parameters
