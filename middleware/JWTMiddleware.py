from fastapi import Header, HTTPException
from services.AuthService import decode_token_jwt


async def verificar_token_jwt(Authorization: str = Header(default='')):
    if not Authorization.split(' ')[0] == 'Bearer':
        raise HTTPException(status_code=401, detail="Token Invalido!")

    token = Authorization.split(" ")[1]

    payload = decode_token_jwt(token)

    if not payload:
        raise HTTPException(status_code=401, detail="token invalido ou expirado.")

    return payload
