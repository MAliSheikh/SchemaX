from db.sessions import SessionLocal

# Provides DB session per request
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()