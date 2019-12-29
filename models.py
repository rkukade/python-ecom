
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rkukade25@localhost/pydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Vendor(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    name = db.Column('vname', db.String(100))
    email = db.Column('vemail', db.String(100), unique=True)
    product = db.relationship('Product', backref='vendor',
                               lazy=False, uselist=False)
    accno = db.Column('accno', db.Integer(),
                      db.ForeignKey('account.id'),
                      unique=True,nullable=True)

class Product(db.Model):
    id = db.Column('pid', db.Integer(), primary_key=True)
    name = db.Column('pname', db.String(100))
    price = db.Column('pprice', db.Float())
    qty = db.Column('pqty', db.Integer())
    vid = db.Column('v_id', db.Integer,db.ForeignKey('vendor.id'),nullable=False)


class Customer(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    name = db.Column('cname', db.String(100))
    accno = db.Column('caccno', db.Integer, db.ForeignKey('account.id'),unique=True, nullable=True)


class Account(db.Model):
    id = db.Column('id', db.Integer(), primary_key=True)
    type = db.Column('type', db.String(100))
    balance = db.Column('balance', db.Float())
    vendor = db.relationship('Vendor', backref='venacc',
                              lazy=False, uselist=False)
    #customer = db.relationship('Customer', backref='custacc',
    #                          lazy=False, uselist=False)

if __name__ == '__main__':
    db.create_all()