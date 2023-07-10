import motor.motor_asyncio
from decouple import config
from models.PostagemModel import PostagemCriarModel
from bson import ObjectId
from utils.ConverterUtils import ConverterUtils


converterUtils = ConverterUtils()

MONGO_DB_URL = config("MONGO_DB_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)

database = client.Devagram
postagem_collection = database.get_collection("postagem")


class Postagem_Repository:
    async def criar_postagem(self, postagem: PostagemCriarModel) -> dict:
        postagem_criada = await postagem_collection.insert_one(postagem.__dict__)

        novo_postagem = await postagem_collection.find_one({"_id": postagem_criada.inserted_id})

        return converterUtils.postagem_converter(novo_postagem)

    async def listar_postagens(self, ):
        return postagem_collection.find()

    async def buscar_postagem(self, id: str) -> dict:
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

        if postagem:
            return converterUtils.postagem_converter(postagem)

    async def atualizar_postagem(self, id: str, dados_postagem: dict):
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

        if postagem:
            postagem_atualizado = await postagem_collection.update_one(
                {"_id": ObjectId(id)}, {"$set": dados_postagem}
            )
            postagem_encoontrado = await postagem_collection.find_one(
                {"_id": ObjectId(id)}
            )

            return converterUtils.postagem_converter(postagem_encoontrado)

    async def deletar_postagem(self, id: str):
        postagem = await postagem_collection.find_one({"_id": ObjectId(id)})

        if postagem:
            await postagem_collection.delete_one({"_id": ObjectId(id)})
