import enum, csv
from .config import BaseConfig

class attributeTypes(enum.Enum):
    NOMINAL = 1
    NUMERICAL = 2
    CATEGORICAL = 3
    VECTOR = 4
    LATITUDE = 5
    LONGITUDE = 6

class attributeMissingValueSettings(enum.Enum):
    IGNORE = 1
    CUSTOM = 2
    MEAN = 3
    MEDIAN = 4
    ZEROVECTOR = 5

def isFlagOnPosition(mask, pos):
    return ((mask >> pos - 1) & 1) != 0

def flipBitOnPosition(mask, pos):
    return mask ^ (1 << pos - 1)

def intToType(_int):
    return attributeTypes(_int).name

def typeToInt(_type):
    return _type.value

def intToMissingValueSetting(_int):
    return attributeMissingValueSettings(_int).name

def missingValueSettingToInt(_missingSetting):
    return _missingSetting.value

def checkAttributeMissingValueValidity(attribute, value):
    if intToType(attribute.type) == attributeTypes.NUMERICAL:
        try:
            assert float(value)
        except ValueError:
            return False
    return True

def missingValueSettingValidForAttribute(attribute, setting):
    if attribute.type != attributeTypes.NUMERICAL.value:
        if setting == attributeMissingValueSettings.MEAN.value or setting == attributeMissingValueSettings.MEDIAN.value:
            return False

    if attribute.type == attributeTypes.VECTOR.value:
        if setting == attributeMissingValueSettings.CUSTOM.value:
            return False
    else:
        if setting == attributeMissingValueSettings.ZEROVECTOR.value:
            return False

    return True

def isValidCSV(filename):
    # TODO
    return True

def getDatasetFilepath(filename, uid, did, vid):
    return getDatasetDirectory(uid, did, vid) + "/" + str(filename)

def getDatasetDirectory(uid, did, vid):
    return "datasets/" + str(uid) + "/" + str(did) + "/" + str(vid) + "/"

def getSpaceFilepath(filename, uid, sid):
    return getSpaceDirectory(uid, sid) + "/" + str(filename)

def getSpaceDirectory(uid, sid):
    return "spaces/" + str(uid) + "/" + str(sid) + "/"

def generateNonconflictingName(datasetName, uid):
    from .models import Dataset

    if Dataset.query.filter_by(name = datasetName, uid = uid, deleted = False).first():
        appendedNumber = 1
        # increment number until we find one that is unused
        while Dataset.query.filter_by(name = datasetName + " (" + str(appendedNumber) + ")", uid = uid, deleted = False).first():
            appendedNumber = appendedNumber + 1
        
        datasetName = datasetName + " (" + str(appendedNumber) + ")"
    return datasetName

def getDatasetData(filename, skipHeader):
    data = {}

    data["attributes"] = []
    from .models import Attribute

    with open(filename) as csvfile:    
        reader = csv.reader(csvfile)

        for i, row in enumerate(reader):
            if i == 0: # first row contains labels
                for y, label in enumerate(row):
                    if not skipHeader:
                        label = "Attribute" + str(y + 1)
                    data["attributes"].append(Attribute(label = label, 
                                                        missing_value_setting = 1,
                                                        type_mask = pow(2, len(attributeTypes)) - 1,
                                                        type = typeToInt(attributeTypes.NUMERICAL)))
                continue
    
    import numpy as np
    dataset = np.genfromtxt(filename, delimiter = ",", skip_header = skipHeader, usemask = True)
    np.warnings.filterwarnings("ignore")
    data["itemCount"] = len(dataset)

    median = np.median(dataset, axis = 0)
    mean = np.mean(dataset, axis = 0)
    sdev = np.std(dataset, axis = 0)
    minimum = np.quantile(dataset, 0, axis = 0)
    q1 = np.quantile(dataset, .25, axis = 0)
    q3 = np.quantile(dataset, .75, axis = 0)
    maximum = np.quantile(dataset, 1, axis = 0)

    datasetStrings = np.genfromtxt(filename, delimiter = ",", skip_header = skipHeader, usemask = True, dtype = str)

    data["statistics"] = []
    from .models import Statistics

    for i in range(len(data["attributes"])):
        generateStatistics = True

        if np.isnan(median[i]):
            generateStatistics = False # only generate statistics for numbers
            data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, typeToInt(attributeTypes.NUMERICAL))
            if len(np.unique(datasetStrings[:,i])) <= BaseConfig.ATTRIBUTE_CLASSIFICATION_CATEGORY_MAX_UNIQUE_COUNT:
                data["attributes"][i].type = typeToInt(attributeTypes.CATEGORICAL)
            else:
                data["attributes"][i].type = typeToInt(attributeTypes.NOMINAL)

        # check if we are within bounds for longitude and latitude
        if np.isnan(median[i]) or minimum[i] < -180 or maximum[i] > 180:
            data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, typeToInt(attributeTypes.LONGITUDE))
        elif data["attributes"][i].label.lower() == "lon" or data["attributes"][i].label.lower() == "longitude":
            data["attributes"][i].type = typeToInt(attributeTypes.LONGITUDE)

        if np.isnan(median[i]) or minimum[i] < -90 or maximum[i] > 90:
            data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, typeToInt(attributeTypes.LATITUDE))
        elif data["attributes"][i].label.lower() == "lat" or data["attributes"][i].label.lower() == "latitude":
            data["attributes"][i].type = typeToInt(attributeTypes.LATITUDE)

        # vector checks
        isVector = True
        for item in datasetStrings[:,i]:
            vectorValues = item.split()
            if len(vectorValues) != 3:
                isVector = False

            for value in vectorValues:
                if not value.replace('.','',1).isdigit():
                    isVector = False

            if not isVector:
                break

        if isVector: # vector takes priority over any other type
            data["attributes"][i].type = typeToInt(attributeTypes.VECTOR)
        else:
            data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, typeToInt(attributeTypes.VECTOR))

        if generateStatistics:
            data["statistics"].append(Statistics(aid = i + 1, # SQL increments from 1
                                                minimum = minimum[i],
                                                q1 = q1[i],
                                                median = median[i],
                                                q3 = q3[i],
                                                maximum = maximum[i],
                                                mean = mean[i],
                                                sdev = sdev[i]))

    return data