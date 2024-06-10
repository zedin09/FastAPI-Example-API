from fastapi import HTTPException
import pandas as pd
from Models.client import Cliente

def leer_clientes():
    df = pd.read_csv("clientes_segmentados.csv")
    return [Cliente(**row) for _, row in df.iterrows()]

def obtener_cliente(cliente_id: str):
    df = pd.read_csv("clientes_segmentados.csv")
    cliente = df[df['id'] == cliente_id]
    if cliente.empty:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return Cliente(**cliente.iloc[0])

def crear_cliente(cliente: Cliente):
    df = pd.read_csv("clientes_segmentados.csv")
    nuevo_registro = pd.DataFrame([cliente.model_dump()])
    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_csv("clientes_segmentados.csv", index=False)

def actualizar_cliente(cliente_id: str, datos_actualizados: Cliente):
    df = pd.read_csv("clientes_segmentados.csv")
    index = df[df['id'] == cliente_id].index
    if len(index) == 0:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    df.loc[index, ['nombre', 'categoria']] = datos_actualizados.nombre, datos_actualizados.categoria
    df.to_csv("clientes_segmentados.csv", index=False)

def eliminar_cliente(cliente_id: str):
    df = pd.read_csv("clientes_segmentados.csv")
    df = df[df['id'] != cliente_id]
    df.to_csv("clientes_segmentados.csv", index=False)