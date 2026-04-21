import httpx
import asyncio
import json

async def test():
    api_key = "sk-cp-6Ihf42qq6X-XYEy6TwwGKRi5hokXlm9d0ofpMZmhx95AIo5PK4Sr5PecepJSkQ3ol_ofZEJdTEkyvuprYzgOA5dfqSPquyt9SAmwKvPEFjHttetnJHwl6iI"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    prompt = """你是一个专业的明星发现助手。请根据以下查询，发现中国明星。

查询: 发现5个中国男演员

请返回JSON格式的列表，每个元素包含:
- name: 明星姓名
- category: 明星类型（演员/歌手/主持人/导演/其他）
- level: 明星等级（顶流/一线/二线/三线）
- description: 简短描述
- weibo_fans: 微博粉丝数（如果知道）
- douyin_fans: 抖音粉丝数（如果知道）

只返回JSON格式的列表，不要包含任何解释。"""
    
    payload = {
        "model": "MiniMax-M2.5",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://api.minimaxi.com/v1/chat/completions",
            headers=headers,
            content=json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"Content:\n{content}")

asyncio.run(test())
