from typing import Dict, List, Optional
from fastapi import Depends, HTTPException, status
import jwt
from fastapi.security import OAuth2PasswordBearer
from configure import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/token")

def verify_access_token(token: str = Depends(oauth2_scheme)) -> Dict[str, str | List[str]] | None:
    '''토큰 검증 Dependency'''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #type: ignore
        username: Optional[str] = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        
        if username is None:
            raise credentials_exception
            
        return {"username": username, "roles": roles}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise credentials_exception


def verify_admin_role(token_data: Dict[str, str | List[str]] = Depends(verify_access_token)):
    '''관리자 권한 확인 Dependency'''
    permission_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions",
    )
    
    if 'admin' not in token_data["roles"]:
        raise permission_exception
    
    return token_data["username"]

# 3. 사용자 확인 함수
def verify_user_role(token_data: Dict[str, str | List[str]] = Depends(verify_access_token)) -> str:
    '''사용자 권한 확인 Dependency'''
    permission_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not enough permissions",
    )
    
    if 'user' not in token_data["roles"] and 'admin' not in token_data["roles"]:
        raise permission_exception
    
    return token_data["username"] #type: ignore
