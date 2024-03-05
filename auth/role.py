from fastapi import HTTPException, status, Request
from .jwt_handler import decodeJWT

class RoleChecker:
    def __init__(self, allowed_roles: list[str] = None):
        self.allowed_roles = allowed_roles
        
    async def __call__(self, request: Request):
        user = await self.get_current_user(request)
        await self.role_checker(user)

    async def get_current_user(self, request: Request):
        try:
            authorization = request.headers.get("Authorization")
            if authorization is None or not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or missing Authorization header",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            token = authorization.split(" ")[1]  # Extract token from "Bearer <token>"
            payload = decodeJWT(token)
            user = {
                "activerole": payload.get("activerole"),
            }
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            print(user)
            return user
        except Exception as e:
            print(f'{e}')
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error"
            )

    async def role_checker(self, user: dict):
        if self.allowed_roles is not None and user["activerole"] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="You don't have enough permissions"
            )