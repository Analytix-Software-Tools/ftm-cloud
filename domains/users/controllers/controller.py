from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext
from pydantic.validators import List

from auth.jwt_handler import sign_jwt
from models.response import Response
from models.user import User, UserResponse, UserSignIn
from domains.users.services.user_services import UserService

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"])


@router.post("/login")
async def login_user(credentials: UserSignIn = Body(...)):
    user_exists = await User.find_one(User.email == credentials.email)
    if user_exists:
        password = hash_helper.verify(
            credentials.password, user_exists.password)
        if password:
            return await sign_jwt(user_exists)

        raise HTTPException(
            status_code=403,
            detail="Invalid username or password specified!"
        )

    raise HTTPException(
        status_code=403,
        detail="Invalid username or password specified!"
    )


@router.post("/", response_model=UserResponse, response_description="Successfully registered user.")
async def signup_user(new_user: User = Body(...)):
    """Registers a new user within the space.
    """
    user_exists = await User.find_one(User.email == new_user.email)
    if user_exists:
        raise HTTPException(
            status_code=409,
            detail="A user already exists by that email."
        )

    user_services = UserService()
    new_user.password = hash_helper.encrypt(new_user.password)
    new_user = await user_services.add_document(new_user)
    return new_user


@router.patch("/{pid}", response_model=Response, response_description="Successfully patched user.")
async def patch_user(pid: str, patch_list: List[object] = Body(...)):
    """Patches a user within the space.
    """
    user_service = UserService()
    await user_service.patch(pid=pid, patch_document_list=patch_list)
    return Response(status_code=204, response_type='success', description="User patched successfully.")


@router.get("/", response_description="Users retrieved", response_model=Response[UserResponse])
async def get_users(q: str | None = None, limit: int | None = None, offset: int | None = None, sort: str | None = None):
    """Gets all users using the user defined parameters.
    """
    user_services = UserService()
    users = await user_services.get_all(q=q, limit=limit, offset=offset, sort=sort)
    return Response(status_code=200,
                    response_type='success',
                    description="Users retrieved successfully.",
                    data=users)


@router.get("/{pid}", response_description="User data retrieved", response_model=Response[UserResponse])
async def get_user(pid: str):
    """Retrieves a user by ID.
    """
    user_services = UserService()
    user = await user_services.validate_exists(pid=pid)
    return Response(status_code=200, response_type='success', description='User retrieved.', data=[user])


@router.delete("/{pid}", response_description="User successfully deleted.", response_model=Response)
async def delete_user(pid: str):
    """Deletes a user.
    """
    user_services = UserService()
    await user_services.delete_document(pid=pid)
    return Response(status_code=200, response_type="success", description="User deleted.")
