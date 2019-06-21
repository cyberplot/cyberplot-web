import enum, csv
from .config import BaseConfig

class attributeTypes(enum.Enum):
    NOMINAL = 1
    NUMERICAL = 2
    CATEGORICAL = 3
    VECTOR = 4

def isFlagOnPosition(mask, pos):
    return ((mask >> pos - 1) & 1) != 0

def flipBitOnPosition(mask, pos):
    return mask ^ (1 << pos - 1)

def intToType(_int):
    return attributeTypes(_int).name

def typeToInt(_type):
    return _type.value

def isValidCSV(filename):
    # TODO
    return True

def getDatasetFilepath(filename, uid, did, vid):
    return getDatasetDirectory(uid, did, vid) + "/" + str(filename)

def getDatasetDirectory(uid, did, vid):
    return "datasets/" + str(uid) + "/" + str(did) + "/" + str(vid)

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
                                                        missing_value_setting = 0,
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
        # TODO ignore vectors for now
        data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, typeToInt(attributeTypes.VECTOR))
        
        if np.isnan(median[i]):
            data["attributes"][i].type_mask = flipBitOnPosition(data["attributes"][i].type_mask, typeToInt(attributeTypes.NUMERICAL))
            if len(np.unique(datasetStrings[:,i])) <= BaseConfig.ATTRIBUTE_CLASSIFICATION_CATEGORY_MAX_UNIQUE_COUNT:
                data["attributes"][i].type = typeToInt(attributeTypes.CATEGORICAL)
            else:
                data["attributes"][i].type = typeToInt(attributeTypes.NOMINAL)
            continue
        
        data["statistics"].append(Statistics(aid = i + 1, # SQL increments from 1
                                             minimum = minimum[i],
                                             q1 = q1[i],
                                             median = median[i],
                                             q3 = q3[i],
                                             maximum = maximum[i],
                                             mean = mean[i],
                                             sdev = sdev[i]))

    return data