from config import get_config
import os
from database.models import Events
from database.init_or_check_db import wait_for_db,get_database_url,get_tables_database

if __name__ == '__main__':
    conf = get_config()
    if os.getenv('DATABASE_URL'):
        print('DATABASE URL exist')
        tables = get_tables_database()
        print(tables)
    else:
        print('No URL of Database detected')
