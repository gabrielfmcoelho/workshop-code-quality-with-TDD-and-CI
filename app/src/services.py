from datetime import datetime as dt

from .models import User
from .schemas import UserRegister, UserLogin, UserPublic, UsersPublic
from .database import DatabaseInterface


class UserService(DatabaseInterface):
    def __init__(self):
        super().__init__()
        
    def create_user(self, user: UserRegister):
        session = self.get_session().__next__()
        user = User(**user.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserService.build_public_info(user)
    
    def get_all(self):
        session = self.get_session().__next__()
        users = session.query(User).all()
        return UsersPublic(users=[self.build_public_info(user) for user in users])
    
    def get_by_id(self, id: int):
        session = self.get_session().__next__()
        return session.query(User).filter(User.id == id).first()
    
    def get_by_username(self, username: str):
        session = self.get_session().__next__()
        return session.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str):
        session = self.get_session().__next__()
        return session.query(User).filter(User.email == email).first()
    
    @staticmethod
    def build_public_info(user: User):
        return UserPublic(username=user.username, email=user.email, full_name=f'{user.first_name} {user.last_name}')
    
    def update_by_id(self, user_id: int, user_info: UserRegister):
        session = self.get_session().__next__()
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        user.first_name = user_info.first_name
        user.last_name = user_info.last_name
        user.username = user_info.username
        user.email = user_info.email
        user.password = user_info.password
        user.updated_at = dt.utcnow()
        session.commit()
        session.refresh(user)
        return UserService.build_public_info(user)
    
    def remove_by_id(self, user_id: int):
        session = self.get_session().__next__()
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        user.is_active = False
        user.updated_at = dt.utcnow()
        session.commit()
        session.refresh(user)

    def delete_by_id(self, user_id: int):
        session = self.get_session().__next__()
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        session.delete(user)
        session.commit()  

    def login(self, user: UserLogin):
        session = self.get_session().__next__()
        user = session.query(User).filter(User.username == user.username, User.password == user.password).first()
        if not user:
            return None
        return UserService.build_public_info(user)
    
def get_user_service():
    return UserService()