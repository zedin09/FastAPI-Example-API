from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from Controllers.client_controller import leer_clientes, obtener_cliente, crear_cliente, actualizar_cliente, eliminar_cliente, plot_customers_rfm
from Models.client import Cliente
from Models.authentication_models import Token
from Controllers.authentication_controller import oauth2_scheme, fake_users_db, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.get("/clientes/", response_model=list[Cliente])
def obtener_clientes(token: Annotated[str, Depends(oauth2_scheme)]):
    return leer_clientes()

@router.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente_por_id(cliente_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    return obtener_cliente(cliente_id)

@router.post("/clientes/", response_model=Cliente)
def agregar_cliente(cliente: Cliente, token: Annotated[str, Depends(oauth2_scheme)]):
    crear_cliente(cliente)
    return cliente

@router.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente_por_id(cliente_id: str, cliente: Cliente, token: Annotated[str, Depends(oauth2_scheme)]):
    actualizar_cliente(cliente_id, cliente)
    return cliente

@router.delete("/clientes/{cliente_id}")
def eliminar_cliente_por_id(cliente_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    eliminar_cliente(cliente_id)
    return {"mensaje": "Cliente eliminado"}

@router.get("/rfm/plot")
def plot_customers_rfm_route(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Genera y muestra un gráfico de los clientes según el modelo RFM.

    Returns:
        None
    """
    return plot_customers_rfm()

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
