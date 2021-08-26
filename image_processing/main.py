from fastapi import FastAPI
import asyncio
from aio_pika import connect, Message


origins = [
    "http://localhost:8000/",
    "http://localhost/",
]




app = FastAPI(
    openapi_url="/api/v1/upload_images/openapi.json",
    docs_url="/api/v1/upload_images/docs",
    description="Обработка изображений",
)

@app.get('/service_produser')
def hh():
    return 'fast'

async def main(y):
    # Perform connection
    connection = await connect(
        "amqp://user:bitnami@rabbit/"
    )

    # Creating a channel
    channel = await connection.channel()

    # Sending the message
    await channel.default_exchange.publish(
        Message(str(y).encode("utf-8")),
        routing_key="hello",
    )

    print(" [x] Sent 'Hello World!'")

    await connection.close()

@app.get("/service_produser/tt")
async def read_root(id_for_consumer:str):
    await main(id_for_consumer)
    return {"Hello": "World"}




