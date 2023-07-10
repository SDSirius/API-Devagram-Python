import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile
from middleware.JWTMiddleware import verificar_token_jwt
from models.PostagemModel import PostagemCriarModel

router = APIRouter()


@router.post("/", response_description="Rota para criação de postagem.")
async def rota_criar_postagem(file: UploadFile, postagem: PostagemCriarModel = Depends(PostagemCriarModel)):
    try:
        caminho_foto = f"files/foto-{datetime.now().strftime('%H%M%S')}.png"
        with open(caminho_foto, 'wb+')as arquivo:
            arquivo.write(file.file.read())

        #resultado = await registrar_postagem(postagem, caminho_foto)

        os.remove(caminho_foto)

    except Exception as erro:
        raise erro


@router.get(
    "/",
    response_description="Rota para listar as postagens.",
    dependencies=[Depends(verificar_token_jwt)]
    )

async def listar_postagens(Authorization: str = Header(default='')):
    try:

        return {"teste": "OK"}

    except Exception as erro:
        raise erro


@router.get(
    "/me",
    response_description="Rota para listar as postagens do usuario logado.",
    dependencies=[Depends(verificar_token_jwt)]
)
async def buscar_postagem_usuario_logado(Authorization: str = Header(default='')):
    try:

        return {"teste": "OK"}

    except Exception as erro:
        raise erro
