from datetime import datetime  
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(60), unique = True, nullable = False)
    account_type = db.Column(db.SmallInteger, nullable = False)

    def to_dict(self):
        return dict(UID = self.uid,
                    username = self.username,
                    password = self.password,
                    email = self.email,
                    accountType = self.account_type)

class Dataset(db.Model):
    __tablename__ = "datasets"
    did = db.Column(db.Integer, primary_key = True, nullable = False)
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    last_edit = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    space_dependencies = db.Column(db.Integer, nullable = False)
    deleted = db.Column(db.Boolean, nullable = False)

    def to_dict(self):
        return dict(DID = self.did,
                    UID = self.uid,
                    name = self.name,
                    lastEdit = self.last_edit,
                    spaceDependencies = self.space_dependencies,
                    deleted = self.deleted)

class Space(db.Model):
    __tablename__ = "spaces"
    sid = db.Column(db.Integer, primary_key = True, nullable = False)
    did = db.Column(db.Integer, db.ForeignKey("datasets.did"), primary_key = True)
    dataset_uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key = True)
    owner_uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    filename = db.Column(db.String(255), nullable = False)

    def to_dict(self):
        return dict(SID = self.sid,
                    DID = self.did,
                    datasetUID = self.dataset_uid,
                    ownerUID = self.owner_uid,
                    name = self.name,
                    filename = self.filename)

class Attribute(db.Model):
    __tablename__ = "attributes"
    aid = db.Column(db.Integer, primary_key = True, nullable = False)
    did = db.Column(db.Integer, db.ForeignKey("datasets.did"), primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey("datasets.uid"), primary_key = True)
    type = db.Column(db.SmallInteger, nullable = False)
    type_mask = db.Column(db.Binary, nullable = False)
    missing_value_setting = db.Column(db.SmallInteger, nullable = False)

    def to_dict(self):
        return dict(AID = self.aid,
                    DID = self.did,
                    UID = self.uid,
                    type = self.type,
                    typeMask = self.type_mask,
                    missingValueSetting = self.missing_value_setting)

class Connector(db.Model):
    __tablename__ = "connectors"
    did = db.Column(db.Integer, db.ForeignKey("datasets.did"), primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey("datasets.uid"), primary_key = True)
    type = db.Column(db.SmallInteger, nullable = False)
    key = db.Column(db.String(255))

    def to_dict(self):
        return dict(DID = self.did,
                    UID = self.uid,
                    type = self.type,
                    key = self.key)

class DatasetVersion(db.Model):
    __tablename__ = "dataset_versions"
    vid = db.Column(db.Integer, primary_key = True, nullable = False)
    did = db.Column(db.Integer, db.ForeignKey("datasets.did"), primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey("datasets.uid"), primary_key = True)
    filename = db.Column(db.String(255), nullable = False)
    upload_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    item_count = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return dict(VID = self.vid,
                    DID = self.did,
                    UID = self.uid,
                    filename = self.filename,
                    uploadDate = self.upload_date,
                    itemCount = self.item_count)

class Statistics(db.Model):
    __tablename__ = "statistics"
    aid = db.Column(db.Integer, db.ForeignKey("attributes.aid"), primary_key = True)
    did = db.Column(db.Integer, db.ForeignKey("attributes.did"), primary_key = True)
    uid = db.Column(db.Integer, db.ForeignKey("attributes.uid"), primary_key = True)
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