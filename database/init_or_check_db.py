import sys
import os
import time

from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from .models import Base, Events



def get_database_url():   
    return os.getenv('DATABASE_URL',None)

def wait_for_db(engine, max_retries=30):
    for i in range(max_retries):
        try:
            engine.connect()
            print("✅ Connexion à PostgreSQL réussie!")
            return True
        except OperationalError:
            print(f"⏳ Attente de PostgreSQL... ({i+1}/{max_retries})")
            time.sleep(1)
    return False


def get_tables_database():
    url_database = get_database_url()
    engine = create_engine(url_database)
    try:
        inspector = Inspector.from_engine(engine)
        table_names = inspector.get_table_names()
        tables = engine.table_names()
        return tables
    except Exception as e:
        print(f'Execption Occurs : {e}')
        return ['PAS DE TABLE']
