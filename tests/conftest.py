from pathlib import Path

import pytest
from peewee import SqliteDatabase

from potyk_ci_back.db import TABLES


@pytest.fixture()
def test_db():
    return SqliteDatabase(':memory:')


@pytest.fixture(autouse=True)
def mock_db(test_db):
    test_db.bind(TABLES, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(TABLES)
    yield
    test_db.drop_tables(TABLES)
    test_db.close()


@pytest.fixture()
def project_path():
    return Path(r'C:\Users\GANSOR\PycharmProjects\potyk-doc').resolve()
