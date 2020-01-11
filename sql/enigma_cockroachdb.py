# sqlalchemy orm:
# https://docs.sqlalchemy.org/en/13/orm/query.html
# użycie sqlalchemy i cockroachdb
# https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html
# generowanie zahashowanych haseł
# https://nitratine.net/blog/post/how-to-hash-passwords-in-python/

import hashlib
import os

from cockroachdb.sqlalchemy import run_transaction
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

COCKROACH_DB_USER = 'enigma'
COCKROACH_DB_URL = 'localhost:26257'
COCKROACH_DB_DATABASE = 'enigma'
SECURE_CLUSTER = False  # Set to False for insecure clusters

Base = declarative_base()

# Klasa Account jest odzwierciedleniem tabeli accounts w cockroachdb
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_salt = Column(LargeBinary)
    password_key = Column(LargeBinary)
    email = Column(String)


class Cockroach:
    def __init__(self, secure_cluster):
        if secure_cluster:
            self.connect_args = {
                'sslmode': 'require',
                'sslrootcert': 'certs/ca.crt',
                'sslkey': 'certs/client.enigma.key',
                'sslcert': 'certs/client.enigma.crt'
            }
        else:
            self.connect_args = {'sslmode': 'disable'}

        self.engine = create_engine(
            'cockroachdb://{}@{}/{}'.format(COCKROACH_DB_USER, COCKROACH_DB_URL, COCKROACH_DB_DATABASE),
            connect_args=self.connect_args,
            echo=True  # Log SQL queries to stdout
        )

        # Automatically create the "accounts" table based on the Account class.
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()

    def create_account(self, account):
        exists = self.session.query(Account.id).filter_by(username=account.username).first() is not None
        if not exists:
            self.session.add(account)
            self.session.commit()

# Utworzenie salt i key na podstawie zadanego hasła
def salt_password(salt, password):
    key = hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, 100000)
    return key

# sprawdzenie zadanego hasła za pomocą salt i key z bazy danych
def check_password(salt, key, password):
    if key == hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, 100000):
        return True
    else:
        return False


cockroach = Cockroach(SECURE_CLUSTER)

salt = os.urandom(32)
password = 'masełko'
test_account = Account(
    username='macfiej',
    password_salt=salt,
    password_key=salt_password(salt, password),
    email="maciek.czarnota@gmail.com"
)

cockroach.create_account(test_account)