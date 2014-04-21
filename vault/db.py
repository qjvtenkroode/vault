from sqlalchemy import Column, Integer, String, Binary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import crypto

Base = declarative_base()
Session = sessionmaker()

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user = Column(String(250), nullable=False)
    password = Column(Binary, nullable=False)

    def __repr__(self, passwd):
        return '<Name %r> <User %r> <Encrypted %r> <Decrypted %r>' % (self.name, self.user, self.password, crypto.decrypt(passwd, self.password))

class Database:
    engine = create_engine('sqlite:///vault.db', echo=True)
    Session.configure(bind=engine)

    def create(self):
        Base.metadata.create_all(self.engine)

    def session(self):
        return Session()
    
    def add(self, session, account):
        session.add(account)


if __name__ == "__main__":
    passwd = "test"
    db = Database()
    session = db.session()
    a = Account(name="Github", user="piebob", password=crypto.encrypt(passwd,"testing"))
    db.create()
    db.add(session, a)
    print(a)
    session.commit()
