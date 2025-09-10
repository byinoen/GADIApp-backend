from sqlmodel import SQLModel, create_engine, Session
from app.config import get_settings

settings = get_settings()
engine = create_engine(
    settings.DATABASE_URL, 
    echo=False,
    connect_args={"check_same_thread": False}
)


def get_session():
    with Session(engine) as session:
        yield session


async def init_db():
    SQLModel.metadata.create_all(engine)