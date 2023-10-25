from dataclasses import dataclass

import structlog
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import settings

logger = structlog.get_logger("plotter-rest")


@dataclass
class DatabaseConfig:
    dialect: str
    user: str
    password: str
    host: str
    port: str
    db: str

    @property
    def connection_str(self) -> str:
        return (
            f"{self.dialect}://"
            f"{self.user}:"
            f"{self.password}@"
            f"{self.host}:"
            f"{self.port}/"
            f"{self.db}"
        )


def get_postgres_conn_str():
    return DatabaseConfig(
        settings.PG_DIALECT,
        settings.PG_USER,
        settings.PG_PWD,
        settings.PG_HOST,
        settings.PG_PORT,
        settings.PG_DB,
    ).connection_str


def get_db_session():
    engine = create_engine(get_postgres_conn_str(), pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_db_connection(db_session: Session, database_name: str = None):
    try:
        return db_session.is_active
    except Exception as e:
        logger.error(
            "validate_db_connection_exception", db_name=database_name, error=str(e)
        )
        return False
