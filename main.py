from fastapi import FastAPI  # Ferramenta para criar a API
from app.api.v1.auth import router as auth_router  # Importa as rotas de autenticação
from app.api.v1.users import router as users_router  # Importa as rotas de usuários

app = FastAPI(title="Library API", version="1.0.0")  # Cria a API com nome e versão

app.include_router(auth_router, prefix="/api/v1")  # Adiciona as rotas de autenticação
app.include_router(users_router, prefix="/api/v1")  # Adiciona