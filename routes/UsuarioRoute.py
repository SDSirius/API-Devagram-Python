import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from services.AuthService import decode_token_jwt
from services.UsuarioService import UsuarioService
from middleware.JWTMiddleware import verificar_token_jwt

router = APIRouter()
usuarioService = UsuarioService()


@router.post("/", response_description="Rota para criação de usuarios.")
async def rota_criar_usuario(file: UploadFile, usuario: UsuarioCriarModel = Depends(UsuarioCriarModel)):
    try:
        caminho_foto = f"files/foto-{datetime.now().strftime('%H%M%S')}.png"
        with open(caminho_foto, 'wb+')as arquivo:
            arquivo.write(file.file.read())

        resultado = await usuarioService.registrar_usuario(usuario, caminho_foto)
        print(resultado)
        os.remove(caminho_foto)

        if not resultado['status'] == 201:
            raise HTTPException(status_code=resultado['status'], detail=resultado['mensagem'])

        return resultado
    except Exception as erro:
        print(f'Erro do rota_criar_usuario -----> UsuarioRoute : {erro}')
        raise HTTPException(status_code=500, detail="Erro interno no servidor. Rota POST Criar Usuario")


@router.get(
    "/me",
    response_description="Rota para buscar as informações do usuario logado.",
    dependencies=[Depends(verificar_token_jwt)]
    )
async def buscar_infor_usuario_logado(Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        payload = decode_token_jwt(token)
        resultado = await usuarioService.buscar_usuario_logado(payload["usuario_id"])

        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado)

        return resultado

    except Exception as erro:
        print(f'Erro do buscar info do usuario {erro}')
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")


@router.put(
    "/me",
    response_description="Rota PUT para Atualizar as informações do usuario logado.",
    dependencies=[Depends(verificar_token_jwt)]
    )
async def atualizar_usuario_logado(Authorization: str = Header(default=''),
                                   usuario_atualizar: UsuarioAtualizarModel = Depends(UsuarioAtualizarModel)):
    try:
        token = Authorization.split(' ')[1]
        payload = decode_token_jwt(token)
        print(payload)

        resultado = await usuarioService.atualizar_usuario_logado(payload["usuario_id"], usuario_atualizar)
        print(resultado)
        if not resultado["status"] == 200:
            raise HTTPException(status_code=resultado['status'], detail=resultado)

        return resultado

    except Exception as erro:
        print(f'Erro atualizar usuario --> Usuario Route: {erro}')
        raise HTTPException(status_code=500, detail="Erro interno no servidor. Rota PUT Atualizar Usuario")
