import asyncio
import time 

async def countdown(name, seconds):
    for i in range(seconds):
        print(f"{name}: {i+1}")
        await asyncio.sleep(1)
        
async def run_sequential():
    print("Running sequnetial coroutines...")
    start = time.time()
    await countdown("First", 3)
    await countdown("Second", 3)
    end = time.time()
    print(f"Total Time taken(sequential): {end-start:.2f} seconds")

async def run_concurrently():
    start = time.time()
    task1 = asyncio.create_task(countdown("First", 3))
    task2 = asyncio.create_task(countdown("Second", 3))
    await task1
    await task2
    end = time.time()
    
    print(f"Total time taken(concurrent): {end-start:.2f} seconds")

async def main():
    await run_sequential()
    await run_concurrently()
    
asyncio.run(main())

