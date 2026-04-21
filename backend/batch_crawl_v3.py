import asyncio
import sys
import os
from datetime import date
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from app.database import SessionLocal
from app.models.models import Star, WeiboData
from playwright.async_api import async_playwright
import httpx
import json
import re

API_KEY = "sk-cp-6Ihf42qq6X-XYEy6TwwGKRi5hokXlm9d0ofpMZmhx95AIo5PK4Sr5PecepJSkQ3ol_ofZEJdTEkyvuprYzgOA5dfqSPquyt9SAmwKvPEFjHttetnJHwl6iI"
MINIMAX_URL = "https://api.minimaxi.com/v1/chat/completions"
MODEL = "MiniMax-M2.5"


async def discover_stars_ai(query: str):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""你是一个专业的明星发现助手。请根据以下查询，发现中国明星。

查询: {query}

要求：返回的明星必须是与之前不同的、新的明星。不要返回常见的顶流明星。

请返回JSON格式的列表，每个元素包含:
- name: 明星姓名
- category: 明星类型（演员/歌手/主持人/导演/其他）
- level: 明星等级（顶流/一线/二线/三线）
- description: 简短描述

只返回JSON格式的列表"""
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9
    }
    
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                MINIMAX_URL,
                headers=headers,
                content=json.dumps(payload, ensure_ascii=False).encode('utf-8')
            )
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            content = re.sub(r'<think[^>]*>[\s\S]*?</think\s*>', '', content, flags=re.IGNORECASE)
            json_match = re.search(r'\[[\s\S]*\]', content)
            if json_match:
                return json.loads(json_match.group(0))
    except Exception as e:
        print(f"AI 错误: {e}")
    return []


async def crawl_weibo_fans(star_name: str, headless: bool = True):
    results = []
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=headless,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            
            search_url = f"https://s.weibo.com/user?q={star_name}&Refer=weibo_user"
            await page.goto(search_url, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(2)
            
            user_cards = await page.query_selector_all('.card-user-b')
            
            for card in user_cards[:3]:
                try:
                    name_elem = await card.query_selector('.name')
                    fans_elem = await card.query_selector('.s-nobr')
                    
                    if name_elem:
                        name = await name_elem.inner_text()
                        fans_text = "0"
                        if fans_elem:
                            fans_text = await fans_elem.inner_text()
                            if '粉丝：' in fans_text:
                                fans_text = fans_text.replace('粉丝：', '')
                        
                        fans_count = parse_fans(fans_text)
                        results.append({
                            "weibo_name": name.strip(),
                            "fans_count": fans_count,
                        })
                except:
                    pass
            
            await browser.close()
    except Exception as e:
        print(f"  微博爬虫错误: {e}")
    
    return results


def parse_fans(text: str) -> int:
    text = text.strip().replace(',', '')
    if '万' in text:
        num = float(text.replace('万', '').strip())
        return int(num * 10000)
    elif '亿' in text:
        num = float(text.replace('亿', '').strip())
        return int(num * 100000000)
    else:
        try:
            return int(text.replace(',', '').strip())
        except:
            return 0


async def main():
    db = SessionLocal()
    
    existing_names = set(name[0] for name in db.query(Star.name).all())
    print(f"数据库中已有 {len(existing_names)} 个明星\n")
    
    queries = [
        "发现10个2024年新晋流量明星",
        "发现10个中国新生代演员（00后）",
        "发现10个中国新生代歌手（95后）",
        "发现10个中国知名话剧演员",
        "发现10个中国知名音乐剧演员",
        "发现10个中国知名配音演员",
        "发现10个中国知名脱口秀演员",
        "发现10个中国知名喜剧演员",
        "发现10个中国知名童星出身的演员",
        "发现10个中国知名综艺咖",
        "发现10个中国知名选秀节目出身的艺人",
        "发现10个中国知名男团成员",
        "发现10个中国知名女团成员",
        "发现10个中国知名摇滚歌手",
        "发现10个中国知名民谣歌手",
        "发现10个中国知名说唱歌手",
        "发现10个中国知名网络歌手",
        "发现10个中国知名影视配角演员",
        "发现10个中国知名老戏骨演员",
        "发现10个中国知名港台演员",
    ]
    
    random.shuffle(queries)
    
    total_added = 0
    
    for query in queries[:15]:
        print(f"=== 查询: {query} ===")
        
        stars = await discover_stars_ai(query)
        print(f"AI 发现 {len(stars)} 个明星")
        
        new_count = 0
        for star_info in stars:
            name = star_info.get("name")
            if not name:
                continue
            
            if name in existing_names:
                continue
            
            star = Star(
                name=name,
                category=star_info.get("category", "其他"),
                level=star_info.get("level", "三线"),
                description=star_info.get("description", "")
            )
            db.add(star)
            db.flush()
            
            print(f"  添加 {name}...")
            
            weibo_results = await crawl_weibo_fans(name, headless=True)
            if weibo_results:
                best_match = weibo_results[0]
                weibo = WeiboData(
                    star_id=star.id,
                    weibo_name=best_match.get("weibo_name"),
                    fans_count=best_match.get("fans_count", 0),
                    collect_date=date.today()
                )
                db.add(weibo)
                print(f"    微博粉丝: {best_match.get('fans_count', 0):,}")
            
            db.commit()
            existing_names.add(name)
            total_added += 1
            new_count += 1
            
            await asyncio.sleep(2)
        
        if new_count == 0:
            print("  未发现新明星")
        
        await asyncio.sleep(3)
    
    db.close()
    print(f"\n完成！共添加 {total_added} 个新明星")


if __name__ == "__main__":
    asyncio.run(main())
