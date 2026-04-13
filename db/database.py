from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# O "Engine" é o motor de conexão (similar ao DataSource no Spring)
engine = create_async_engine(DATABASE_URL, echo=True)

# A Session é o que você usa para fazer queries (similar ao EntityManager)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# A Base é a "mãe" de todas as suas classes/entidades
Base = declarative_base()