from sqlalchemy.orm import Session
from models import User



def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

def update_user_password(db: Session, user: User, new_password: str):
    user.password = new_password  # type: ignore
    db.commit()

def create_user(db: Session, email: str, password: str):    
    new_user = User(email=email, password=password)
    db.add(new_user)
    db.commit()