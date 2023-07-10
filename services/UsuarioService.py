from datetime import datetime
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AWSProvider import AWSProvider
from repositories.UsuarioRepository import UsuarioRepository

awsProvider = AWSProvider()
usuarioRepository = UsuarioRepository()

class UsuarioService:
    async def registrar_usuario(self, usuario: UsuarioCriarModel, caminho_foto):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_email(usuario.email)

            if usuario_encontrado:
                return {
                    "mensagem": f"Email {usuario.email} Já Cadastrado!",
                    "dados": "",
                    "status": 400
                }
            else:
                novo_usuario = await usuarioRepository.criar_usuario(usuario)

                try:
                    url_foto = awsProvider.upload_arquivo_s3(
                        f"fotos-perfil/{novo_usuario['id']}.png",
                        caminho_foto
                    )
                except Exception as erro:
                    print(f'Erro do registrar usuario --> UserService Registrar Usuario: {erro}')


                novo_usuario = await usuarioRepository.atualizar_usuario(novo_usuario['id'], {"foto": url_foto})

                return {
                    "mensagem": "Usuario cadastrado com sucesso!",
                    "dados": novo_usuario,
                    "status": 201
                }
        except Exception as error:
            return {
                "mensagem": "Erro interno no serviodr",
                "dados": str(error),
                "status": 500
            }


    async def buscar_usuario_logado(self, id: str):

        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario(id)

            if usuario_encontrado:
                return {
                    "mensagem": f"Usuario encontrado!",
                    "dados": usuario_encontrado,
                    "status": 200
                }

            else:
                return {
                    "mensagem": f"Usuario com o id {id} não encontrado!",
                    "dados": "",
                    "status": 404
                }

        except Exception as erro:
            print(f'Erro do buscar usuario logado -> {erro}')
            return {
                "mensagem": f"Usuario com o id {id} não encontrado!",
                "dados": "",
                "status": 404
            }
    async def atualizar_usuario_logado(self, id, usuario_atualizar: UsuarioAtualizarModel):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario(id)
            print(usuario_encontrado)
            if usuario_encontrado:
                usuario_dict = usuario_atualizar.__dict__
                print(usuario_dict)
                try:
                    caminho_foto = f"files/foto-{datetime.now().strftime('%H%M%S')}.png"

                    with open(caminho_foto, 'wb+') as arquivo:
                        arquivo.write(usuario_atualizar.foto.file.read())

                    url_foto = awsProvider.upload_arquivo_s3(
                        f"fotos-perfil/{id}.png",
                        caminho_foto
                    )
                except Exception as erro:
                    print(f'Erro do atualizar_usuario_logado --> Upload Imagem ---->UserService: {erro}')

                usuario_dict["foto"] = url_foto if url_foto is not None else usuario_dict["foto"]


                usuario_atualizado = await usuarioRepository.atualizar_usuario(id, usuario_dict)
                print(usuario_atualizado)
                return {
                    "mensagem": f"Usuario Atualizado!",
                    "dados": usuario_atualizado,
                    "status": 200
                }

            else:
                return {
                    "mensagem": f"Usuario com o id {id} não encontrado!",
                    "dados": "",
                    "status": 404
                }

        except Exception as erro:
            print(f'Erro do buscar usuario logado -> {erro}')
            return {
                "mensagem": f"Usuario com o id {id} não encontrado!",
                "dados": "",
                "status": 404
            }
