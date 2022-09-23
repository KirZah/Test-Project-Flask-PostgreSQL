from test_project.db.models import Base
from test_project.db.database import engine

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
