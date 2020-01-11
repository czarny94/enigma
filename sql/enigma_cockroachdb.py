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

Base = declarative_base()

# Klasa Account jest odzwierciedleniem tabeli accounts w cockroachdb
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_salt = Column(LargeBinary)
    password_key = Column(LargeBinary)
    email = Column(String)


username = "mac4iek"
password = "maselko"
not_password = "dupa"

test_account = Account(
    username=username,
    password_salt=b'dffdsf',
    password_key=b'fdsfdf',
    email="maciek.czarnota@gmail.com"
)

# Create an engine to communicate with the database. The
# "cockroachdb://" prefix for the engine URL indicates that we are
# connecting to CockroachDB using the 'cockroachdb' dialect.
# For more information, see
# https://github.com/cockroachdb/cockroachdb-python.

secure_cluster = False  # Set to False for insecure clusters
connect_args = {}

if secure_cluster:
    connect_args = {
        'sslmode': 'require',
        'sslrootcert': 'certs/ca.crt',
        'sslkey': 'certs/client.enigma.key',
        'sslcert': 'certs/client.enigma.crt'
    }
else:
    connect_args = {'sslmode': 'disable'}

engine = create_engine(
    'cockroachdb://{}@{}/{}'.format(COCKROACH_DB_USER, COCKROACH_DB_URL, COCKROACH_DB_DATABASE),
    connect_args=connect_args,
    echo=True  # Log SQL queries to stdout
)

# Automatically create the "accounts" table based on the Account class.
Base.metadata.create_all(engine)


def create_account(session, account):
    exists = session.query(Account.id).filter_by(username=account.username).first() is not None
    if not exists:
        session.add(account)


# Utworzenie salt i key na podstawie zadanego hasła
def salt_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, 100000)
    return salt, key


# sprawdzenie zadanego hasła za pomocą salt i key z bazy danych
def check_password(salt, key, password):
    if key == hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, 100000):
        return True
    else:
        return False


run_transaction(sessionmaker(bind=engine),
                lambda session: create_account(session, test_account))
