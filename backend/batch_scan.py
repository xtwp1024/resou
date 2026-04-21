import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"

QUERIES = [
    "发现10个中国顶流男演员",
    "发现10个中国一线女演员",
    "发现10个中国顶流歌手",
    "发现10个中国知名导演",
    "发现10个中国知名主持人",
    "发现10个中国流量明星",
    "发现10个中国实力派演员",
    "发现10个中国新生代演员",
    "发现10个中国喜剧演员",
    "发现10个中国动作演员",
]

async def batch_discover():
    async with httpx.AsyncClient(timeout=120) as client:
        total_discovered = 0
        total_added = 0
        
        for i, query in enumerate(QUERIES):
            print(f"\n[{i+1}/{len(QUERIES)}] 正在查询: {query}")
            
            try:
                response = await client.post(
                    f"{BASE_URL}/api/ai/discover",
                    params={"query": query, "auto_add": "true"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    discovered = data.get("discovered", 0)
                    added = data.get("added", [])
                    skipped = data.get("skipped", [])
                    
                    total_discovered += discovered
                    total_added += len(added)
                    
                    print(f"  发现: {discovered} 个明星")
                    print(f"  新增: {added}")
                    if skipped:
                        print(f"  跳过(已存在): {skipped}")
                else:
                    print(f"  错误: {response.status_code} - {response.text}")
                
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"  异常: {e}")
        
        print(f"\n========== 扫描完成 ==========")
        print(f"总共发现: {total_discovered} 个明星")
        print(f"总共新增: {total_added} 个明星")

if __name__ == "__main__":
    asyncio.run(batch_discover())
