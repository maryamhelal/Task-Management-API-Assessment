from sqlmodel import SQLModel, create_engine

# Connect to the database using sqlite
sqlite_file_name = "Buguard_task.db"
sqlite_url = f'sqlite:///{sqlite_file_name}'

connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, echo = True, connect_args = connect_args)

def create_db():
    SQLModel.metadata.create_all(engine)