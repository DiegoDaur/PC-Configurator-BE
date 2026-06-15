from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:160306@localhost/pc_configurator", echo=True)

SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()


def init_db():
    print("[LOG] - Inizializzazione Database")

    with engine.connect() as conn:
        conn.execute(text(open("docs/DDL/10_CREATE.sql").read()))
        conn.commit()

    print("[LOG] - Database inizializzato con successo")
