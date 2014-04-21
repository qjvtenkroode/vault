from nose.tools import *
from vault import crypto
from vault import db

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_cryto():
    passwd = 'test'
    raw = "Super Secret"
    enc = crypto.encrypt(passwd, raw)

    assert_equal(crypto.decrypt(passwd, enc), raw)

def test_db_create():
    database = db.Database();
    database.create()

def test_db_insert():
    passwd = 'test'
    database = db.Database()
    session = database.session()
    a = db.Account(name="Github", user="piebob", password=crypto.encrypt(passwd,"testing"))
    database.create()
    database.add(session, a)
    session.commit()
