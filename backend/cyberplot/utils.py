import enum, csv, os
from .config import BaseConfig

class attributeTypes(enum.Enum):
    NOMINAL = 1
    NUMERICAL = 2
    CATEGORICAL = 3
    VECTOR = 4
    LOCATIONAL = 5
    SPATIAL = 6

class attributeMissingValueSettings(enum.Enum):
    IGNORE = 1
    CUSTOM = 2
    MEAN = 3
    MEDIAN = 4
    ZEROVECTOR = 5

class datasetTypes(enum.Enum):
    MULTIVARIATE = 1
    MATRIX = 2

def isFlagOnPosition(mask, pos):
    return ((mask >> pos - 1) & 1) != 0

def flipBitOnPosition(mask, pos):
    return mask ^ (1 << pos - 1)

def intToAttributeType(_int):
    return attributeTypes(_int).name

def attributeTypeToInt(_type):
    return _type.value

def intToDatasetType(_int):
    return datasetTypes(_int).name

def datasetTypeToInt(_type):
    return _type.value

def intToMissingValueSetting(_int):
    return attributeMissingValueSettings(_int).name

def missingValueSettingToInt(_missingSetting):
    return _missingSetting.value

def checkAttributeMissingValueValidity(attribute, value):
    if intToAttributeType(attribute.type) == attributeTypes.NUMERICAL:
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

def isImage(filename):
    from PIL import Image
    try:
        im = Image.open(filename)
        im.verify()
        im.close()
        return True
    except:
        return False

def createCSVFromHeightmap(filename):
    from PIL import Image
    im = Image.open(filename, "r")
    width, height = im.size

    if width > 256 or height > 256:
        thumbsize = 256, 256
        im.thumbnail(thumbsize)
        width, height = im.size

    pixelValues = list(im.getdata(band = 0))
    im.close()
    os.unlink(filename)

    output = open(filename, "w+")

    for h in range(0, height):
        for w in range(0, width):
            output.write(str(pixelValues[h * width + w]))
            if w != width - 1:
                output.write(",")
        output.write("\n")
    output.close()

    return

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

def getMatrixDatasetData(filename):
    data = {}

    data["attributes"] = []
    from .models import Attribute

    data["attributes"].append(Attribute(label = "Values", 
                                        missing_value_setting = 1,
                                        type_mask = 0,
                                        type = attributeTypeToInt(attributeTypes.SPATIAL)))
    data["attributes"][0].type_mask = flipBitOnPosition(data["attributes"][0].type_mask, attributeTypeToInt(attributeTypes.SPATIAL))

    import numpy as np
    dataset = np.genfromtxt(filename, delimiter = ",", skip_header = False, usemask = True)

    median = np.median(dataset)
    mean = np.mean(dataset)
    sdev = np.std(dataset)
    minimum = np.quantile(dataset, 0)
    q1 = np.quantile(dataset, .25)
    q3 = np.quantile(dataset, .75)
    maximum = np.quantile(dataset, 1)

    data["statistics"] = []
    from .models import Statistics

    if not np.isnan(median):
        data["statistics"].append(Statistics(aid = 1, # SQL increments from 1
                                            minimum = minimum,
                                            q1 = q1,
                                            median = median,
                                            q3 = q3,
                                            maximum = maximum,
                                            mean = mean,
                                            sdev = sdev))

    data["itemCount"] = int(dataset.shape[0]) * int(dataset.shape[1])

    return data

def getMultivariateDatasetData(filename, skipHeader):
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
                                                        type = attributeTypeToInt(attributeTypes.NUMERICAL)))
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
            data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, attributeTypeToInt(attributeTypes.NUMERICAL))
            if len(np.unique(datasetStrings[:,i])) <= BaseConfig.ATTRIBUTE_CLASSIFICATION_CATEGORY_MAX_UNIQUE_COUNT:
                data["attributes"][i].type = attributeTypeToInt(attributeTypes.CATEGORICAL)
            else:
                data["attributes"][i].type = attributeTypeToInt(attributeTypes.NOMINAL)

        # check if we are within bounds for longitude and latitude
        if np.isnan(median[i]) or minimum[i] < -180 or maximum[i] > 180:
            data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, attributeTypeToInt(attributeTypes.LOCATIONAL))
        elif data["attributes"][i].label.lower() == "lon" or data["attributes"][i].label.lower() == "longitude" or data["attributes"][i].label.lower() == "lat" or data["attributes"][i].label.lower() == "latitude":
            data["attributes"][i].type = attributeTypeToInt(attributeTypes.LOCATIONAL)

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
            data["attributes"][i].type = attributeTypeToInt(attributeTypes.VECTOR)
        else:
            data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, attributeTypeToInt(attributeTypes.VECTOR))

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