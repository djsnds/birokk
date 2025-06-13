from contextlib import contextmanager
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker
from settings import DATABASE_URL


engine = create_engine(
    url=DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(engine, expire_on_commit=False)


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise
    finally:
        session.close()
