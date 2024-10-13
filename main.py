import asyncio
from weather import periodic_task


async def main():
    await periodic_task(5)  # 3 минуты в секундах


if __name__ == '__main__':
    asyncio.run(main())