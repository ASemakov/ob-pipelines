from mongoengine.connection import disconnect

import pytest
from mongoengine import connect
from pymongo.mongo_client import MongoClient

from ob_pipelines import settings


@pytest.yield_fixture(scope="function", autouse=True)
def another_resource_setup_with_autouse():
    disconnect()
    conn: MongoClient = connect(host="mongomock://localhost/test")
    yield
    # should use database_names because mongomock don't support new method
    for db_name in conn.database_names():
        conn.drop_database(db_name)
    disconnect()
    connect(host=settings.db_connection)

