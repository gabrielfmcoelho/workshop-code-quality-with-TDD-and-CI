from fastapi import APIrouter, HTTPException, status, Depends

from .schemas import UserRegister, UserLogin, UserPublic
from .services import UserService, get_user_service
from .database import DatabaseInterface, get_database_interface


users_router = APIrouter(
    prefix='/users',
    tags=['users']
)

@users_router.post('/register',
             description='Register a new user',
             response_model=UserPublic,
             status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister, user_service: UserService = Depends(get_user_service)):
    """
    Register a new user
    """
    if user_service.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail='Username already exists')
    if user_service.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail='Email already exists')
    return user_service.create_user(user)

@users_router.get('/get/{id}',
            description='Get a user by id',
            response_model=UserPublic,
            status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int, user_service: UserService = Depends(get_user_service)):
    """
    Get a user
    """
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@users_router.put('/update/{id}',
             description='Update a user',
             response_model=UserPublic,
             status_code=status.HTTP_200_OK)
async def update_user(id: int, user: UserRegister, user_service: UserService = Depends(get_user_service)):
    """
    Update a user
    """
    user = user_service.update_user(id, user)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

