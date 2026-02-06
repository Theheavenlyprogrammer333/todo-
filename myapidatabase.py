from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.exc import IntegrityError  # Add this import
 

DATABASE_URL = "sqlite:///./notes.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create the session instance
session = SessionLocal()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

class task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

def user_by_email(email):
    return session.query(User).filter(User.email == email).first()

def confirm_action(prompt: str) -> bool:
    return input(f"{prompt} (y/n): ").lower() == 'yes'

def add_user():
    name = input("Enter user: ")
    email = input("Enter email: ")
    
    if user_by_email(email):
        print("User already exists.")
        return
    
    try:
        session.add(User(name=name, email=email))
        session.commit()
        print(f"User {name} added successfully.")
    except IntegrityError:
        session.rollback()
        print("Error: Could not add user.")

def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    
    try:
        session.add(task(title=title, description=description))
        session.commit()
        print(f"Task '{title}' added successfully.")
    except IntegrityError:
        session.rollback()
        print("Error: Could not add task.")

def main() -> None:
    while True:
        print("\nOptions:")
        print("1. Add User")
        print("2. Add Task")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            add_user()
        elif choice == '2':
            add_task()
        elif choice == '3':
            break
        else:
            print("Invalid option. Please try again.")

# Add this to actually run the program
if __name__ == "__main__":
    main()
