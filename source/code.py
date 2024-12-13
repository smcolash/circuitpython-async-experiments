
import asyncio
import time
import traceback

async def monitor (lock, event):
    while True:
        async with lock:
            try:
                print (time.time ())
                if int (time.time ()) % 5 == 0:
                    print ('TRIGGER')
                    event.set ()
            finally:
                await asyncio.sleep (0.1)

async def activate (lock, event):
    while True:
        if event.is_set ():
            event.clear ()
            async with lock:
                try:
                    print ('+' * 10)
                    print ('PROCESSING')
                    await asyncio.sleep (2.5)
                finally:
                    print ('-' * 10)
        await asyncio.sleep (0.1)

def main ():
    try:
        lock = asyncio.Lock ()
        event = asyncio.Event ()
        loop = asyncio.new_event_loop ()

        tasks = [
            loop.create_task (monitor (lock, event)),
            loop.create_task (activate (lock, event))
        ]

        loop.run_until_complete (asyncio.wait (tasks))
        loop.close ()
    except:
        print (traceback.format_exc ())
        time.sleep (5)

