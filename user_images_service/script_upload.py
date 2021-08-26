from asyncio.tasks import sleep
from fastapi import FastAPI
import asyncio
import threading




# asyncio.run(main())

app = FastAPI()
import time
queue = asyncio.Queue()

async def upload_images():

    
    tt = queue.qsize()
    while tt:
        client = await queue.get()
        print(f'добавлено изображение в очередь от клиента с id {client}')
        print('поток',threading.current_thread())
        queue.task_done()
        time.sleep(10)
        print('размер очереди',queue.qsize())
        
        tt = queue.qsize()
    print('поток закрыт')


def start_thread_upload():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(upload_images())
    loop.close()



async def apend_item_quene():
    try:
        print(threading.active_count() )
        if threading.active_count() == 3:
            print('больше 2')
        if threading.active_count() < 3:
            print('создание потока нового')
            threading.Thread(target=start_thread_upload, args=()).start()
    except asyncio.QueueFull:
        pass
    

    
    

@app.get("/")
async def read_root(client:int):
    await queue.put(client)
    await apend_item_quene()
    return 'ok'

