# Name: Yasser Hernandez (hernayas)
# Citation for the ode below:
# Date: 04/15/2025
# Adapted from "Connect using Cloud SQL Language Connectors"
# Source URL: https://docs.cloud.google.com/sql/docs/postgres/connect-connectors

import os
from google.cloud.sql.connector import Connector, IPTypes
import pg8000
import sqlalchemy
import sqlalchemy.orm


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.
    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = "decoded-pivot-493200-k7:us-west1:smart-grocery-db"  # e.g. 'project:region:instance'
    db_user = "postgres"  # e.g. 'my-db-user'
    db_pass = "5{6$o=BdiB#6O0Fg"  # e.g. 'my-db-password'
    db_name = "postgres"  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    # initialize Cloud SQL Python Connector object
    connector = Connector(refresh_strategy="LAZY")

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name,
            ip_type=ip_type,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    # Creates database engine
    return engine, connector

# Base class for models
class Base(sqlalchemy.orm.DeclarativeBase):
    pass

engine, connector = connect_with_connector()

with engine.connect() as conn:
    result = conn.execute(sqlalchemy.text("SELECT 1"))
    print(result.fetchone())

connector.close()