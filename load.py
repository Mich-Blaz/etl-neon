
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Product

engine = create_engine(os.environ['DATABASE_URL'], echo=False)
Session = sessionmaker(bind=engine)


def add_product(name, price, category):
    """Ajoute un nouveau produit"""
    session = Session()
    try:
        new_product = Product(name=name, price=price, category=category)
        session.add(new_product)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Erreur: {e}")
        return False
    finally:
        session.close()


def etl_insert_products(products_data, batch_size=1000):
    """
    Insertion par lots avec gestion d'erreurs
    products_data: liste de dictionnaires
    batch_size: nombre de produits par batch
    """
    session = Session()
    total_inserted = 0
    
    try:
        # Découper en chunks
        for i in range(0, len(products_data), batch_size):
            batch = products_data[i:i + batch_size]
            
            try:
                session.bulk_insert_mappings(Product, batch)
                session.commit()
                total_inserted += len(batch)
                print(f"Batch {i//batch_size + 1}: {len(batch)} produits insérés")
                
            except Exception as e:
                session.rollback()
                print(f"Erreur sur le batch {i//batch_size + 1}: {e}")
                # Continue avec le prochain batch ou raise selon ton besoin
                
        return total_inserted
        
    finally:
        session.close()


from sqlalchemy.dialects.postgresql import insert  # ou mysql, sqlite, etc.

def upsert_products_batch(products_data):
    """Insert ou update si le produit existe déjà"""
    session = Session()
    try:
        # PostgreSQL exemple
        stmt = insert(Product).values(products_data)
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],  # ou autre clé unique
            set_={
                'price': stmt.excluded.price,
                'name': stmt.excluded.name
            }
        )
        session.execute(stmt)
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()