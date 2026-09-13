from sqlalchemy.orm import Session
from models import User


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, role: str = None):
    query = db.query(User)
    if role is not None:
        query = query.filter(User.role == role)
    return query.all()