from fastapi import APIRouter, HTTPException, Depends  # Ferramentas para rotas, erros e dependências
from app.core.database import get_supabase  # Conexão com o Supabase
from app.models.user import User, UserUpdate  # Modelos de usuário
from supabase import Client  # Tipo Client
from fastapi.security import OAuth2PasswordBearer  # Para verificar tokens

router = APIRouter(prefix="/users", tags=["Users"])  # Grupo de rotas com prefixo /users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")  # Diz onde pegar o token

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:  # Verifica o usuário pelo token
    supabase: Client = get_supabase()  # Conecta ao Supabase
    try:  # Tenta verificar o token
        user = supabase.auth.get_user(token)  # Pega o usuário
        if not user:  # Se falhar, mostra erro
            raise HTTPException(status_code=401, detail="Invalid token")
        return user.user.id  # Devolve o ID do usuário
    except Exception:  # Se der erro
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=list[User])  # Rota para listar usuários (GET /users)
async def list_users(current_user: str = Depends(get_current_user)):  # Só usuários logados
    supabase: Client = get_supabase()  # Conecta ao Supabase
    response = supabase.table("profiles").select("*").execute()  # Pega todos os perfis
    return response.data  # Devolve a lista de usuários

@router.get("/{user_id}", response_model=User)  # Rota para obter usuário por ID (GET /users/{id})
async def get_user(user_id: str, current_user: str = Depends(get_current_user)):  # Só usuários logados
    supabase: Client = get_supabase()  # Conecta ao Supabase
    response = supabase.table("profiles").select("*").eq("id", user_id).execute()  # Busca o usuário
    if not response.data:  # Se não encontrar
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]  # Devolve o usuário

@router.put("/{user_id}", response_model=User)  # Rota para atualizar usuário (PUT /users/{id})
async def update_user(user_id: str, user_update: UserUpdate, current_user: str = Depends(get_current_user)):
    supabase: Client = get_supabase()  # Conecta ao Supabase
    # Só o próprio usuário pode atualizar seu perfil (por enquanto)
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Prepara os dados para atualizar (só campos não vazios)
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    if not update_data:  # Se não enviou nada para atualizar
        raise HTTPException(status_code=400, detail="No data to update")
    # Atualiza o perfil
    response = supabase.table("profiles").update(update_data).eq("id", user_id).execute()
    if not response.data:  # Se falhar
        raise HTTPException(status_code=404, detail="User not found")
    return response.data[0]  # Devolve o usuário atualizado