from pydantic import BaseModel, Field, EmailStr


class UsuarioModel(BaseModel):
    id: str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "Exemplo De Nome",
                "email": "SeuEmail@Aqui.com",
                "senha": "SuaSenha123",
                "foto": "UrlDaSuaFoto.com"
            }
        }

class UsuarioCriarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "nome": "Exemplo De Nome",
                "email": "SeuEmail@Aqui.com",
                "senha": "SuaSenha123",
                "foto": "UrlDaSuaFoto.com"
            }
        }

class UsuarioLoginModel(BaseModel):
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "usuario": {
                "email": "SeuEmail@Aqui.com",
                "senha": "SuaSenha123"
            }
        }
