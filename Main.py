from fastapi import FastAPI
from routes.UsuarioRoute import router as UsuarioRoute
from routes.AuthRoute import router as AuthRoute


app = FastAPI()

app.include_router(UsuarioRoute, tags=["Usuario"], prefix="/api/usuario")
app.include_router(AuthRoute, tags=["Auth"], prefix="/api/auth")


@app.get("/api/health", tags=["health"])
async def health():
    return {
        "status": "OK!"
    }
