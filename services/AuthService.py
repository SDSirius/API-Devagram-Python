import time
import jwt
from decouple import config
from models.UsuarioModel import UsuarioLoginModel
from repositories.UsuarioRepository import UsuarioRepository
from utils.AuthUtil import verificar_senha

JWT_SECRET_KEY = config('JWT_SECRET_KEY')
usuarioRepository = UsuarioRepository()

def gerar_token_jwt(usuario_id:str)-> str:
    payload = {
        "usuario_id": usuario_id,
        "expires": time.time() + 1200
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

    return token


def decode_token_jwt(token:str):
    try:
        token_decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])

        if token_decoded["expires"] >= time.time():
            return token_decoded
        else:
            return None

    except Exception as erro:
        print(f'Erro ao decodificar {erro}')
        return None

async def login_service(usuario : UsuarioLoginModel):
    usuario_encontrado = await usuarioRepository.buscar_usuario_por_email(usuario.email)

    if not usuario_encontrado:
        return {
            "mensagem": "Email ou senha incorrentos",
            "dados": "",
            "status": 401
        }
    else:
        if verificar_senha(usuario.senha, usuario_encontrado['senha']):
            return {
                "mensagem":"Login realizado",
                "dados": usuario_encontrado,
                "status": 200
            }
        else:
            return {
                "mensagem": "Email ou senha incorrentos",
                "dados": "",
                "status": 401
            }

