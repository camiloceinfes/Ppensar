from ast import List
from venv import logger
from fastapi import Depends, HTTPException

class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")
        
    async def get_current_user_role(self, token: str):
        payload = decodeJWT(token)
        if not payload:
            raise HTTPException(status_code=403, detail="Invalid Token!")
        # Assuming the role is stored in the JWT payload under the key 'role'
        user_role = payload.get('role')
        if not user_role:
            raise HTTPException(status_code=403, detail="Role not found in token!")
        return user_role