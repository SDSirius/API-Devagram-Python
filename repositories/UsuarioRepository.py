import motor.motor_asyncio
from decouple import config
from models.UsuarioModel import UsuarioCriarModel
from utils.AuthUtil import gerar_senha_criptografada
from bson import ObjectId
from utils.ConverterUtils import ConverterUtils


converterUtils = ConverterUtils()


MONGO_DB_URL = config("MONGO_DB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)

database = client.Devagram
usuario_collection = database.get_collection("usuario")


class UsuarioRepository:
    async def criar_usuario(self, usuario: UsuarioCriarModel) -> dict:
        usuario.senha = gerar_senha_criptografada(usuario.senha)

        usuario_criado = await usuario_collection.insert_one(usuario.__dict__)

        novo_usuario = await usuario_collection.find_one({"_id": usuario_criado.inserted_id})

        return converterUtils.usuario_converter(novo_usuario)

    async def listar_usuarios(self):
        return usuario_collection.find()

    async def buscar_usuario(self, id: str) -> dict:
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            return converterUtils.usuario_converter(usuario)

    async def buscar_usuario_por_email(self, email: str):
        usuario = await usuario_collection.find_one({"email": email})

        if usuario:
            return converterUtils.usuario_converter(usuario)

    async def atualizar_usuario(self, id: str, dados_usuario: dict):
        if "senha" in dados_usuario:
            dados_usuario["senha"] = gerar_senha_criptografada(dados_usuario["senha"])
            print(dados_usuario)

        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            usuario_atualizado = await usuario_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": dados_usuario}
            )
            usuario_encoontrado = await usuario_collection.find_one(
                {"_id": ObjectId(id)}
            )

            return converterUtils.usuario_converter(usuario_encoontrado)

    async def deletar_usuario(self, id: str):
        usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

        if usuario:
            await usuario_collection.delete_one({"_id": ObjectId(id)})
