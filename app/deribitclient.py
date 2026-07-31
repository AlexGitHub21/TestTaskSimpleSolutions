import aiohttp


class DeribitService:
    async def get_ticker_data(self, ticker: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://test.deribit.com/api/v2/public/ticker?instrument_name={ticker}-PERPETUAL") as response:
                if response.status != 200:
                    return {"id": id, "error": "not found"}
                return await response.json()