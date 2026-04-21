import asyncio
import httpx
import json
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

API_KEY = "sk-cp-6Ihf42qq6X-XYEy6TwwGKRi5hokXlm9d0ofpMZmhx95AIo5PK4Sr5PecepJSkQ3ol_ofZEJdTEkyvuprYzgOA5dfqSPquyt9SAmwKvPEFjHttetnJHwl6iI"

async def test():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    models_to_test = [
        ("https://api.minimaxi.com/v1/chat/completions", "MiniMax-M2.5"),
        ("https://api.minimaxi.com/v1/chat/completions", "MiniMax-M2.5-highspeed"),
        ("https://api.minimax.chat/v1/chat/completions", "MiniMax-M2.5"),
    ]
    
    for base_url, model in models_to_test:
        print(f"\n--- Testing: {base_url} with model {model} ---")
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Say hello"}
            ]
        }
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    base_url,
                    headers=headers,
                    content=json.dumps(payload, ensure_ascii=False).encode('utf-8')
                )
                
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text[:500]}")
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(test())
