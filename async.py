import asyncio
import aiohttp
import time
from statistics import mean


async def temp1(session):
    resp = await session.get(
        'https://www.7timer.info/bin/astro.php?lon=114.1&lat=22.3&ac=0&unit=metric&output=json&tzshift=0')
    json = await resp.json(content_type='text/html')
    temperature_list = []
    for step in range(0, 24):
        temperature_list.append(json['dataseries'][step]['temp2m'])
    return mean(temperature_list)


async def temp2(session):
    resp = await session.get(
        'https://api.open-meteo.com/v1/forecast?latitude=22.31&longitude=114.16&hourly=temperature_2m')
    json = await resp.json()
    return mean(json['hourly']['temperature_2m'])


async def temp3(session):
    resp = await session.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en')
    json = await resp.json()
    temperature_list = []
    for step in range(0, 25):
        temperature_list.append(json['temperature']['data'][step]['value'])
    return mean(temperature_list)


async def main():
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(temp1(session), temp2(session), temp3(session))
        avg_temperature = round(mean(result), 1)
        print(f'Average temperature in Hong Kong is  {avg_temperature} degrees Celsius')


if __name__ == '__main__':
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f'{__file__} executed in {elapsed:0.2f} seconds.')
