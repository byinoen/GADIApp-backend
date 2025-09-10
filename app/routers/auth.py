from fastapi import APIRouter, HTTPException
from app.models.user import UserLogin, UserPublic
from app.security.deps import set_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# Mock user database
MOCK_USERS = {
    "trabajador@example.com": {"password": "1234", "role": "Trabajador", "id": 1},
    "encargado@example.com": {"password": "1234", "role": "Encargado", "id": 2},
    "admin@example.com": {"password": "1234", "role": "Administrador", "id": 3},
}


@router.post("/login")
def login(user_login: UserLogin):
    """Mock login endpoint with hardcoded credentials"""
    email = user_login.email.lower()
    
    if email not in MOCK_USERS:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    user_data = MOCK_USERS[email]
    if user_login.password != user_data["password"]:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    # Create user object
    user = UserPublic(
        id=user_data["id"],
        email=email,
        role=user_data["role"]
    )
    
    # Store current user for demo token
    set_current_user(user)
    
    return {
        "token": "demo",
        "user": user
    }