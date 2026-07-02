from fastapi.security import OAuth2PasswordBearer

# Tells FastAPI where clients obtain JWT tokens
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)