from datetime import datetime as dt

from .models import User
from .schemas import UserRegister, UserLogin, UserPublic, UsersPublic
from .database import DatabaseInterface


class UserService:
    def __init__(self):
        self.db_interface = DatabaseInterface()

    def get_session(self):
        return self.db_interface.get_session().__next__()
        
    def create(self, user: UserRegister, session=None, public_output=False):
        if not session:
            session = self.get_session()
        user = User(**user.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return self.build_public_info(user) if public_output else user
    
    def get_all(self, session=None, public_output=False):
        if not session:
            session = self.get_session()
        users = session.query(User).filter(User.is_active == True).all()
        return UsersPublic(users=[self.build_public_info(user) for user in users]) if public_output else users
    
    def get_by_id(self, id: int, session=None):
        if not session:
            session = self.get_session()
        return session.query(User).filter(User.id == id, User.is_active == True).first()
    
    def get_by_username(self, username: str, session=None):
        if not session:
            session = self.get_session()
        return session.query(User).filter(User.username == username, User.is_active == True).first()
    
    def get_by_email(self, email: str, session=None):
        if not session:
            session = self.get_session()
        return session.query(User).filter(User.email == email, User.is_active == True).first()
    
    def get(self, id: int = None, username: str = None, email: str = None, session=None, validate=True, public_output=False):
        if not any([id, username, email]):
            raise ValueError('Provide at least one unique identifier')
        if id:
            user = self.get_by_id(id, session)
        elif username:
            user = self.get_by_username(username, session)
        elif email:
            user = self.get_by_email(email, session)
        output = self._validate_existence(user) if validate else user
        return self.build_public_info(output) if public_output else output
    
    def _validate_existence(self, user: User|None):
        if user:
            return user
        raise ValueError('User not found')

    @staticmethod
    def build_public_info(user: User):
        return UserPublic(id=user.id, username=user.username, email=user.email, full_name=f'{user.first_name} {user.last_name}')
    
    def update_by_id(self, id: int, data: UserRegister):
        session = self.get_session()
        user = self.get(id=id, session=session, validate=True)
        user.username = data.username
        user.email = data.email
        user.first_name = data.first_name
        user.last_name = data.last_name
        user.password = data.password
        session.commit()
        session.refresh(user)
    
    def remove_by_id(self, id: int):
        session = self.get_session()
        user = self.get(id=id, session=session, validate=True)
        user.is_active = False
        session.commit()
        session.refresh(user)

    def delete_by_id(self, id: int):
        session = self.get_session()
        user = self.get(id=id, session=session, validate=True)
        session.delete(user)
        session.commit()  

    def login(self, user: UserLogin):
        session = self.get_session()
        user = self.get(username=user.username, session=session, validate=True)
        if user.password == user.password:
            return UserService.build_public_info(user)
        raise ValueError('Invalid credentials')
    
def get_user_service():
    return UserService()