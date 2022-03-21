from contextlib import contextmanager

from sqlalchemy import String, Integer, Text, Boolean, create_engine, ForeignKey, Column

from sqlalchemy.orm import relationship, declarative_base, scoped_session, sessionmaker


Base = declarative_base()
host = "localhost"

engine = create_engine(f'postgresql://braxton_admin:braxton_pass@{host}:5433/braxton',
                       pool_size=50, max_overflow=0, echo=False, echo_pool=True)


@contextmanager
def session():
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    try:
        yield db_session
    except Exception as e:
        print(e)
    finally:
        db_session.remove()
        connection.close()


class Types(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    model_info = relationship("Models", backref="types", lazy='dynamic',
                              cascade="all, delete, delete-orphan")


class Models(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    types_id = Column(Integer, ForeignKey('types.id'), nullable=False)
    name = Column(String(200), unique=True, nullable=False)
    descriptions = Column(Text, nullable=False)
    season = Column(String(50), nullable=False)
    available = Column(Boolean, default=False)
    price = Column(Integer, nullable=False)
    model_img = relationship("Images", backref="models", lazy='dynamic',
                             cascade="all, delete, delete-orphan")


class Images(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey('models.id'), nullable=False)
    img = Column(String(200), unique=True, nullable=False)
    name = Column(String(200), nullable=False)
    mimetype = Column(String(200), nullable=False)


