import asyncio
import httpx
import json
import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

API_KEY = "sk-cp-6Ihf42qq6X-XYEy6TwwGKRi5hokXlm9d0ofpMZmhx95AIo5PK4Sr5PecepJSkQ3ol_ofZEJdTEkyvuprYzgOA5dfqSPquyt9SAmwKvPEFjHttetnJHwl6iI"
BASE_URL = "https://api.minimaxi.com/v1/chat/completions"
MODEL = "MiniMax-M2.5"

async def discover_stars(query: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""你是一个专业的明星发现助手。请根据以下查询，发现中国明星。

查询: {query}

请返回JSON格式的列表，每个元素包含:
- name: 明星姓名
- category: 明星类型（演员/歌手/主持人/导演/其他）
- level: 明星等级（顶流/一线/二线/三线）
- description: 简短描述
- weibo_fans: 微博粉丝数（数字，如80000000）
- douyin_fans: 抖音粉丝数（数字，如5000000）

只返回JSON格式的列表
不要包含任何解释。"""
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            BASE_URL,
            headers=headers,
            content=json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )
        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        content = re.sub(r'<think[^>]*>[\s\S]*?</think\s*>', '', content, flags=re.IGNORECASE)
        
        json_match = re.search(r'\[[\s\S]*\]', content)
        if json_match:
            json_str = json_match.group(0)
            try:
                stars = json.loads(json_str)
                return stars
            except:
                print(f"Parse error: {json_str[:200]}")
                return []
        return []

QUERIES = [
    "发现10个中国知名网红",
    "发现10个中国知名博主",
    "发现10个中国知名UP主",
    "发现10个中国知名主播",
    "发现10个中国知名电竞选手",
    "发现10个中国知名游戏主播",
    "发现10个中国知名户外主播",
    "发现10个中国知名美食博主",
    "发现10个中国知名旅游博主",
]

async def main():
    all_stars = []
    
    for i, query in enumerate(QUERIES):
        print(f"\n[{i+1}/{len(QUERIES)}] 查询: {query}")
        
        try:
            stars = await discover_stars(query)
            print(f"  发现 {len(stars)} 个明星:")
            for star in stars:
                print(f"    - {star.get('name')} ({star.get('level')}, {star.get('category')})")
            all_stars.extend(stars)
        except Exception as e:
            print(f"  错误: {e}")
        
        await asyncio.sleep(2)
    
    print(f"\n总共发现: {len(all_stars)} 个明星")
    
    with open("discovered_stars_9.json", "w", encoding="utf-8") as f:
        json.dump(all_stars, f, ensure_ascii=False, indent=2)
    print("结果已保存到 discovered_stars_9.json")

if __name__ == "__main__":
    asyncio.run(main())
