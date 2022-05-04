import asyncio
# https://stackoverflow.com/questions/63292747/how-to-start-async-function-from-async-function-without-wating-for-it-while-usi

async def coro2():
    print("coro2")

async def coro1():
    loop = asyncio.get_running_loop()
    task = loop.create_task(coro2())
    print("created task")
    return

async def main():
    await coro1()
    print("done with main")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("done with loop")