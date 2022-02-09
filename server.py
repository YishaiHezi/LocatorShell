import time

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__)


# this is the 'connection' to the database.
# we will create 1 database with 2 tables/models:
application.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///location_database.db?check_same_thread=False'
db = SQLAlchemy(application)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.mac} -> {self.address}"


class Names(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    mac = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} -> {self.mac}"


@application.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello! This is the locator app.'


@application.route('/macs', methods=['POST'])
def write_mac():
    input_json = request.get_json()
    client_mac = input_json['mac']
    client_name = input_json['name']
    print(client_mac)

    result = write_name_and_mac_in_db(client_mac, client_name)

    if result:
        return 'got it!'

    return 'I need your location'


@application.route('/locations', methods=['POST'])
def write_location_of_mac():
    input_json = request.get_json()
    client_mac = input_json['mac']
    client_location = input_json['location']
    write_mac_and_location_in_db(client_mac, client_location)
    return 'the location inserted to the db'


@application.route('/names')
def get_location_of_name():
    input_json = request.get_json()
    name_to_find = input_json['name']
    location = get_location_from_name_db(name_to_find)

    if location:
        return location

    else:
        return 'Not found'


##########################################################################


def write_name_and_mac_in_db(mac, name):
    name_to_mac_list = Names.query.filter_by(name=name).all()

    if len(name_to_mac_list) == 0:
        db.session.add(Names(name=name, mac=mac))

    else:
        name_to_mac_list[0].mac = mac

    db.session.commit()

    mac_to_address_list = Address.query.filter_by(mac=mac).all()

    if len(mac_to_address_list) == 0:
        return False

    return True


def write_mac_and_location_in_db(client_mac, client_location):
    db.session.add(Address(mac=client_mac, address=client_location))
    db.session.commit()

##########################################################################


def get_location_from_name_db(name):
    name_to_mac_list = Names.query.filter_by(name=name).all()

    if name_to_mac_list:
        desired_mac = name_to_mac_list[0].mac

        mac_to_address_list = Address.query.filter_by(mac=desired_mac).all()

        if mac_to_address_list:
            return mac_to_address_list[0].address


if __name__ == '__main__':
    application.run()
