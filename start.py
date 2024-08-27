import asyncio
import random

from logzero import logger


class Albert:
    def __init__(self):
        self.listen_queue = asyncio.Queue()
        self.read_queue = asyncio.Queue()
        self.say_queue = asyncio.Queue()
        self.write_queue = asyncio.Queue()

    async def listen(self):
        while True:
            logger.info("listening...")
            self.write_queue.put_nowait(random.randint(1, 100))
            await asyncio.sleep(0.1)

    async def say(self):
        while True:
            logger.info("say...")
            await asyncio.sleep(0.1)

    async def read(self):
        while True:
            logger.info("reading...")
            await asyncio.sleep(0.1)

    async def write(self):
        while True:
            w = self.write_queue.get_nowait()
            logger.info(f"write...{w}")
            await asyncio.sleep(0.1)

    async def main(self):
        await asyncio.gather(self.listen(), self.say(), self.read(), self.write())


if __name__ == "__main__":
    a = Albert()
    loop = asyncio.get_event_loop()
    loop.create_task(a.main())
    loop.run_forever()
