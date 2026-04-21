import httpx
import asyncio
import json

async def test():
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            "http://localhost:8000/api/ai/discover",
            params={"query": "发现5个中国男演员", "auto_add": "false"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

asyncio.run(test())
