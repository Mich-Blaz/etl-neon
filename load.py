from extract import get_api_data_from_date
from database.models import Base, Events
from database.utils_db import wait_for_db,sessionmaker,create_engine,insert,func


def init_database_events(db_url : str =None, conf = None):
    engine = create_engine(db_url, echo=True,  pool_pre_ping=True, pool_size=5,    max_overflow=10)
    print(f"📡 Connexion à: '{db_url[:26]}**************{db_url[40:]}')")
    if not wait_for_db(engine):
        print("❌ Impossible de se connecter à PostgreSQL")
        return
    Base.metadata.create_all(engine)
    print("✅ Tables créées")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    if session.query(Events).count() == 0:
        res = get_api_data_from_date(conf = conf)
        stmt = insert(Events).values(res)
        session.execute(stmt)
        session.commit()
        print(f"✅ {len(res)} produits ajoutés à la base de données")
    else:
        print(f"ℹ️ La base contient déjà {session.query(Events).count()} produits")
        latest_updated_at_ = session.query(func.max(Events.updated_at)).scalar()

        print(f'La dernière update date est {latest_updated_at_}')
        res = get_api_data_from_date(date=latest_updated_at_,conf=conf)
        if len(res) > 0:
            stmt = insert(Events).values(res)
            session.execute(stmt)
            session.commit()
            print(f"✅ {len(res)} events mis à jour dans la base de données")
        else:
            print("ℹ️ Aucun nouveau produit à mettre à jour")    
    session.close()
    print("✅ Base de données initialisée avec succès!")