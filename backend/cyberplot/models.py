from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from .utils import isFlagOnPosition, intToAttributeType, attributeTypeToInt, intToDatasetType, datasetTypeToInt, attributeTypes, getDatasetFilepath, getDatasetDirectory, getSpaceFilepath, getSpaceDirectory, intToMissingValueSetting
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(60), nullable = False)
    account_type = db.Column(db.SmallInteger, nullable = False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method = "sha256")

    @classmethod
    def authenticate(cls, **kwargs):
        username = kwargs.get("username").lower()
        password = kwargs.get("password")

        if not username or not password:
            return None

        user = cls.query.filter_by(username = username).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(UID = self.uid,
                    username = self.username,
                    email = self.email,
                    accountType = self.account_type)

class Dataset(db.Model):
    __tablename__ = "datasets"
    __table_args__ = (
        db.UniqueConstraint("did", "uid", name = "uc_datasets"),
    )
    did = db.Column(db.Integer, primary_key = True, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    last_edit = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    versioning_on = db.Column(db.Boolean, nullable = False, default = False)
    type = db.Column(db.SmallInteger, nullable = False)

    def to_dict(self):
        return dict(DID = self.did,
                    UID = self.uid,
                    name = self.name,
                    lastEdit = int(datetime.timestamp(self.last_edit)),
                    deleted = self.deleted,
                    versioningOn = self.versioning_on,
                    type = intToDatasetType(self.type).lower())
    
    def copy(self, did, uid):
        return Dataset(did = did,
                       uid = uid,
                       name = self.name,
                       last_edit = self.last_edit,
                       deleted = self.deleted,
                       versioning_on = self.versioning_on)

class Space(db.Model):
    __tablename__ = "spaces"
    __table_args__ = (
        db.UniqueConstraint("sid", "uid", name = "uc_spaces"),
    )
    sid = db.Column(db.Integer, primary_key = True, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    filename = db.Column(db.String(255), nullable = False)
    last_edit = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    deleted = db.Column(db.Boolean, nullable = False, default = False)

    def to_dict(self):
        return dict(SID = self.sid,
                    UID = self.uid,
                    name = self.name,
                    filename = self.filename,
                    lastEdit = self.last_edit,
                    deleted = self.deleted)

    def filepath(self):
        return getSpaceFilepath(self.filename, self.uid, self.sid)
    
    def dirpath(self):
        return getSpaceDirectory(self.uid, self.sid)

class SpaceDependency(db.Model):
    __tablename__ = "space_dependencies"
    __table_args__ = (
        db.UniqueConstraint("sid", "did", "uid", name = "uc_space_dependencies"),
        db.ForeignKeyConstraint(["sid", "uid"],
                                ["spaces.sid", "spaces.uid"]),
        db.ForeignKeyConstraint(["did", "uid"],
                                ["datasets.did", "datasets.uid"]),
    )
    sid = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, primary_key = True)
    did = db.Column(db.Integer, primary_key = True)

    def to_dict(self):
        return dict(SID = self.sid,
                    UID = self.uid,
                    DID = self.did)

class Attribute(db.Model):
    __tablename__ = "attributes"
    __table_args__ = (
        db.UniqueConstraint("aid", "did", "uid", name = "uc_attributes"),
        db.ForeignKeyConstraint(["did", "uid"],
                                ["datasets.did", "datasets.uid"]),
    )
    aid = db.Column(db.Integer, primary_key = True, nullable = False)
    did = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, primary_key = True)
    label = db.Column(db.String(255), nullable = False)
    type = db.Column(db.SmallInteger, nullable = False)
    type_mask = db.Column(db.Integer, nullable = False)
    missing_value_setting = db.Column(db.SmallInteger, nullable = False)
    missing_value_custom = db.Column(db.String(255))

    def to_dict(self):
        return dict(AID = self.aid,
                    DID = self.did,
                    UID = self.uid,
                    label = self.label,
                    type = intToAttributeType(self.type).lower(),
                    possibleTypes = dict(
                        nominal = isFlagOnPosition(self.type_mask, attributeTypeToInt(attributeTypes.NOMINAL)),
                        numerical = isFlagOnPosition(self.type_mask, attributeTypeToInt(attributeTypes.NUMERICAL)),
                        categorical = isFlagOnPosition(self.type_mask, attributeTypeToInt(attributeTypes.CATEGORICAL)),
                        vector = isFlagOnPosition(self.type_mask, attributeTypeToInt(attributeTypes.VECTOR)),
                        latitude = isFlagOnPosition(self.type_mask, attributeTypeToInt(attributeTypes.LATITUDE)),
                        longitude = isFlagOnPosition(self.type_mask, attributeTypeToInt(attributeTypes.LONGITUDE))
                    ),
                    missingValueSetting = intToMissingValueSetting(self.missing_value_setting).lower(),
                    missingValueCustom = self.missing_value_custom)
    
    def copy(self, aid, did, uid):
        return Attribute(aid = aid,
                         did = did,
                         uid = uid,
                         label = self.label,
                         type = self.type,
                         type_mask = self.type_mask,
                         missing_value_setting = self.missing_value_setting,
                         missing_value_custom = self.missing_value_custom)

class DatasetConnector(db.Model):
    __tablename__ = "dataset_connectors"
    __table_args__ = (
        db.UniqueConstraint("did", "uid", name = "uc_connectors"),
        db.ForeignKeyConstraint(["did", "uid"],
                                ["datasets.did", "datasets.uid"]),
    )
    did = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, primary_key = True)
    key = db.Column(db.String(255), nullable = False, unique = True)

    def to_dict(self):
        return dict(DID = self.did,
                    UID = self.uid,
                    key = self.key)

class UserConnector(db.Model):
    __tablename__ = "user_connectors"
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key = True)
    key = db.Column(db.String(255), nullable = False, unique = True)

    def to_dict(self):
        return dict(UID = self.uid,
                    key = self.key)

class DatasetVersion(db.Model):
    __tablename__ = "dataset_versions"
    __table_args__ = (
        db.UniqueConstraint("vid", "did", "uid", name = "uc_dataset_versions"),
        db.ForeignKeyConstraint(["did", "uid"],
                                ["datasets.did", "datasets.uid"]),
    )
    vid = db.Column(db.Integer, primary_key = True, nullable = False)
    did = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(255), nullable = False)
    upload_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    item_count = db.Column(db.Integer, nullable = False)
    contains_header = db.Column(db.Boolean, nullable = False, default = True)
    deleted = db.Column(db.Boolean, nullable = False, default = False)

    def to_dict(self):
        return dict(VID = self.vid,
                    DID = self.did,
                    UID = self.uid,
                    filename = self.filename,
                    uploadDate = int(datetime.timestamp(self.upload_date)),
                    itemCount = self.item_count,
                    containsHeader = self.contains_header,
                    deleted = self.deleted)
    
    def copy(self, vid, did, uid):
        return DatasetVersion(vid = vid,
                              did = did,
                              uid = uid,
                              filename = self.filename,
                              upload_date = self.upload_date,
                              item_count = self.item_count,
                              contains_header = self.contains_header)
    
    def filepath(self):
        return getDatasetFilepath(self.filename, self.uid, self.did, self.vid)
    
    def dirpath(self):
        return getDatasetDirectory(self.uid, self.did, self.vid)

class Statistics(db.Model):
    __tablename__ = "statistics"
    __table_args__ = (
        db.UniqueConstraint("aid", "did", "uid", name = "uc_statistics"),
        db.ForeignKeyConstraint(["aid", "did", "uid"],
                                ["attributes.aid", "attributes.did", "attributes.uid"]),
    )
    aid = db.Column(db.Integer, primary_key = True)
    did = db.Column(db.Integer, primary_key = True)
    uid = db.Column(db.Integer, primary_key = True)
    minimum = db.Column(db.Numeric)
    q1 = db.Column(db.Numeric)
    median = db.Column(db.Numeric)
    q3 = db.Column(db.Numeric)
    maximum = db.Column(db.Numeric)
    mean = db.Column(db.Numeric)
    sdev = db.Column(db.Numeric)

    def to_dict(self):
        return dict(AID = self.aid,
                    DID = self.did,
                    UID = self.uid,
                    minimum = self.minimum,
                    Q1 = self.q1,
                    median = self.median,
                    Q3 = self.q3,
                    maximum = self.maximum,
                    mean = self.mean,
                    sdev = self.sdev)

    def copy(self, aid, did, uid):
        return Statistics(aid = aid,
                          did = did,
                          uid = uid,
                          minimum = self.minimum,
                          q1 = self.q1,
                          median = self.median,
                          q3 = self.q3,
                          maximum = self.maximum,
                          mean = self.mean,
                          sdev = self.sdev)

class ShareRequest(db.Model):
    __tablename__ = "share_requests"
    __table_args__ = (
        db.UniqueConstraint("did", "uid_sender", "uid_receiver", name = "uc_sharerequests"),
        db.ForeignKeyConstraint(["did", "uid_sender"],
                                ["datasets.did", "datasets.uid"]),
    )
    did = db.Column(db.Integer, primary_key = True)
    uid_sender = db.Column(db.Integer, primary_key = True)
    uid_receiver = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key = True)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def to_dict(self):
        return dict(DID = self.did,
                    UIDsender = self.uid_sender,
                    UIDreceiver = self.uid_receiver,
                    timestamp = self.timestamp)

class HeadsetConnector(db.Model):
    __tablename__ = "headset_connectors"
    hid = db.Column(db.Integer, primary_key = True, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"))
    key = db.Column(db.String(255), nullable = False, unique = True)
    setup_code = db.Column(db.String(10), nullable = False)
    device_name = db.Column(db.String(100), nullable = False)
    last_used = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def to_dict(self):
        return dict(HID = self.hid,
                    UID = self.uid,
                    key = self.key,
                    setupCode = self.setup_code,
                    deviceName = self.device_name,
                    lastUsed = int(datetime.timestamp(self.last_used)))