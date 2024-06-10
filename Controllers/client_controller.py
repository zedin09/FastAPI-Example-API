from io import BytesIO
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
from Models.client import Cliente
import matplotlib.pyplot as plt

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

db = pd.read_csv("clientes_segmentados.csv")
oro_customers: list = db[db['categoria'] == 'Oro']['nombre'].tolist()
plata_customers: list = db[db['categoria'] == 'Plata']['nombre'].tolist()
bronce_customers: list = db[db['categoria'] == 'Bronce']['nombre'].tolist()
print(oro_customers)

def plot_customers_rfm() -> StreamingResponse:
    """
    Genera un gráfico de barras mostrando la distribución de clientes según su clase RFM.

    Returns:
        StreamingResponse: Imagen del gráfico en formato PNG.
    """

    classes = ["oro", "plata", "bronce"]
    counts = [len(oro_customers), len(plata_customers), len(bronce_customers)]

    fig, ax = plt.subplots()
    ax.bar(classes, counts, color=['gold', 'silver', 'brown'])
    ax.set_xlabel('RFM Class')
    ax.set_ylabel('Number of Customers')
    ax.set_title('RFM Segmentation of Customers')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return StreamingResponse(buf, media_type="image/png")