# sqlalchemy orm:
# https://docs.sqlalchemy.org/en/13/orm/query.html
# użycie sqlalchemy i cockroachdb
# https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html
# generowanie zahashowanych haseł
# https://nitratine.net/blog/post/how-to-hash-passwords-in-python/

import hashlib
import os

from flask_login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

COCKROACH_DB_USER = 'enigma'
COCKROACH_DB_URL = 'localhost:26257'
COCKROACH_DB_DATABASE = 'enigma'
SECURE_CLUSTER = False  # Set to False for insecure clusters

Base = declarative_base()


class Cockroach:
    def __init__(self, secure_cluster=False):
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

        # Automatyczne utworzenie tabel, jeżeli nie ma
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)
        self.session = self.Session()


# Klasa Account jest odzwierciedleniem tabeli accounts w cockroachdb, oraz implementuje metody UserMixin dla Flask-Login
class Account(UserMixin, Base):
    def __init__(self, cockroach_db = Cockroach()):
        self.cockroach_db = cockroach_db

    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_salt = Column(LargeBinary)
    password_key = Column(LargeBinary)
    email = Column(String)

    def create_account(self, username, password, email):
        # TODO: dodać obsługę wyjątków w sytuacjach, kiedy nie ma bazy danych, nie ma użytkownika, oraz użytkownik nie ma uprawnień do bazy
        exists = self.cockroach_db.session.query(Account.id).filter_by(username=username).first() is not None
        if not exists:
            # Utworzenie salt i key na podstawie zadanego hasła
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, 100000)
            # stworzenie obiektu użytkownika
            self.username=username
            self.password_salt=salt
            self.password_key=key
            self.email=email
            # commit użytkownika do bazy
            self.cockroach_db.session.add(self)
            self.cockroach_db.session.commit()
            return True
        return False

    # sprawdzenie zadanego hasła za pomocą salt i key z bazy danych
    def check_password(self, username, password):
        exists = self.cockroach_db.session.query(Account.id).filter_by(username=username).first() is not None
        if exists:
            salt = self.cockroach_db.session.query(Account.password_salt).filter_by(
                username=username).scalar()
            key = self.cockroach_db.session.query(Account.password_key).filter_by(
                username=username).scalar()
            if key == hashlib.pbkdf2_hmac("sha256", password.encode('utf-8'), salt, 100000):
                id = self.cockroach_db.session.query(Account.id).filter_by(
                    username=username).scalar()
                username = self.cockroach_db.session.query(Account.username).filter_by(
                    username=username).scalar()
                email = self.cockroach_db.session.query(Account.email).filter_by(
                    username=username).scalar()
                return id, username, email
        return False
