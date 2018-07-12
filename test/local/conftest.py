from mongoengine.connection import disconnect, register_connection, get_connection

import pytest
from mongoengine import connect
from mongoengine.context_managers import switch_db
from pymongo.mongo_client import MongoClient

from ob_pipelines import Task
from ob_pipelines import settings
from ob_pipelines.entities import Experiment, Job


@pytest.yield_fixture(scope="function", autouse=True)
def another_resource_setup_with_autouse():
    register_connection('testdb', host='mongomock://localhost/test')
    with switch_db(Experiment, "testdb"), switch_db(Job, "testdb"), switch_db(Task, "testdb"):
        yield
        conn = get_connection("testdb")
        # should use database_names because mongomock don't support new method
        for db_name in conn.database_names():
            conn.drop_database(db_name)

