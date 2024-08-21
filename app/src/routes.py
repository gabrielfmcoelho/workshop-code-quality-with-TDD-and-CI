from fastapi import APIRouter, HTTPException, status, Depends

from .schemas import UserRegister, UserLogin, UserPublic, UsersPublic, DatabaseTables, DefaultMessage
from .services import UserService, get_user_service
from .database import DatabaseInterface, get_database_interface


database_router = APIRouter(
    prefix='/database',
    tags=['database']
)


@database_router.get('/test-connection',
                description='Test the database connection',
                status_code=status.HTTP_200_OK)
async def test_connection(database_service: DatabaseInterface = Depends(get_database_interface)):
    """
    Test the database connection
    """
    if database_service.test_connection():
        return
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Connection failed')


@database_router.get('/tables',
                description='Get all existing tables in the database',
                response_model=DatabaseTables,
                status_code=status.HTTP_200_OK,
                response_description='List of tables')
async def get_existing_tables(database_service: DatabaseInterface = Depends(get_database_interface)):
    """
    Get all existing tables in the database
    """
    try:
        return DatabaseTables(tables=database_service.get_existing_tables())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@database_router.post('/tables',
                    description='Create or reset tables in the database',
                    status_code=status.HTTP_201_CREATED)
async def setup_tables(reset: bool = False, database_service: DatabaseInterface = Depends(get_database_interface)):
    """
    Create default tables in the database
    """
    try:
        if reset:
            database_service.reset_tables()
        else:
            database_service.create_tables()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@database_router.delete('/tables',
                    description='Drop all tables from the database',
                    status_code=status.HTTP_204_NO_CONTENT)
async def drop_tables(database_service: DatabaseInterface = Depends(get_database_interface)):
    """
    Drop all tables from the database
    """
    try:
        database_service.drop_tables()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

users_router = APIRouter(
    prefix='/users',
    tags=['users']
)


@users_router.post('/',
             description='Register a new user',
             response_model=UserPublic,
             status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegister, user_service: UserService = Depends(get_user_service)):
    """
    Register a new user
    """
    if user_service.get(username=user.username, validate=False):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username already exists')
    if user_service.get(email=user.email, validate=False):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
    return user_service.create(user, public_output=True)

@users_router.get('/',
            description='Get all users',
            response_model=UsersPublic,
            status_code=status.HTTP_200_OK)
async def get_users(user_service: UserService = Depends(get_user_service)):
    """
    Get all users
    """
    return user_service.get_all(public_output=True)

@users_router.get('/search',
            description='Get a user by one of its unique identifiers; eg. id, username, email',
            response_model=UserPublic,
            status_code=status.HTTP_200_OK)
async def get_user(id: int|None = None, username: str|None = None, email: str|None = None, user_service: UserService = Depends(get_user_service)):
    """
    Get a user
    """
    try:
        return user_service.get(id=id, username=username, email=email, validate=True, public_output=True)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@users_router.patch('/{id}',
             description='Update a user by its id',
             response_model=None,
             status_code=status.HTTP_204_NO_CONTENT)
async def update_user(id: int, user: UserRegister, user_service: UserService = Depends(get_user_service)):
    """
    Update a user
    """
    try:
        user_service.update_by_id(id, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@users_router.delete('/{id}',
                description='Delete or deactivate a user by its id; default methodology is to deactivate',
                response_model=None,
                status_code=status.HTTP_204_NO_CONTENT)
async def delete_or_user(id: int, delete: bool = False, user_service: UserService = Depends(get_user_service)):
    """
    Delete a user
    """
    try:
        user_service.delete_by_id(id) if delete else user_service.remove_by_id(id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@users_router.post('/login',
                description='Login a user with its email and password',
                response_model=UserPublic,
                status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    """
    Login a user
    """
    try:
        return user_service.login(user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    






