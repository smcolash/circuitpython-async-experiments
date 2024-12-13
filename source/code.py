import asyncio
import board
import digitalio
import microcontroller
import time
import traceback

async def monitor (lock, event):
    while True:
        async with lock:
            try:
                print (time.time ())
                if int (time.time ()) % 10 == 0:
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

                    with digitalio.DigitalInOut (board.LED) as led:
                        led.switch_to_output (value=False)
                        for _ in range (10):
                            led.value = True
                            await asyncio.sleep (0.25)
                            led.value = False
                            await asyncio.sleep (0.25)

                finally:
                    print ('-' * 10)
        await asyncio.sleep (0.1)

async def main ():
    try:
        lock = asyncio.Lock ()
        event = asyncio.Event ()

        tasks = [
            asyncio.create_task (monitor (lock, event)),
            asyncio.create_task (activate (lock, event))
        ]

        await asyncio.gather (*tasks)
    except Exception as e:
        traceback.print_exception (e)
        time.sleep (5)

if __name__ == '__main__':
    try:
        #
        # run the main function
        #
        asyncio.run (main ())
    except KeyboardInterrupt:
        #
        # exit to REPL
        #
        pass
    except Exception as e:
        #
        # reboot the system
        #
        traceback.print_exception (e)
        time.sleep (10)
        microcontroller.reset ()

