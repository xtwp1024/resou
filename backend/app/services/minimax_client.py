import httpx
from typing import Dict, Any, List
import json
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

class MiniMaxClient:
    def __init__(self, api_key: str, group_id: str = "", base_url: str = "https://api.minimaxi.com/v1/chat/completions", model: str = "MiniMax-M2.5"):
        self.api_key = api_key
        self.group_id = group_id
        self.base_url = base_url
        self.model = model
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def chat(self, messages: List[Dict], temperature: float = 0.0) -> str:
        payload = {
            "model": self.model,
            "messages": messages
        }
        
        if temperature:
            payload["temperature"] = temperature
        
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    content=json.dumps(payload, ensure_ascii=False).encode('utf-8')
                )
                result = response.json()
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            error_msg = str(e)
            try:
                with open("minimax_error.log", "a", encoding="utf-8") as f:
                    f.write(f"Error: {error_msg}\n")
            except:
                pass
            return ""
    
    async def discover_stars(self, query: str) -> List[Dict[str, Any]]:
        prompt = f"""你是一个专业的明星发现助手。请根据以下查询，发现中国明星。

查询: {query}

请返回JSON格式的列表，每个元素包含:
- name: 明星姓名
- category: 明星类型（演员/歌手/主持人/导演/其他）
- level: 明星等级（顶流/一线/二线/三线）
- description: 简短描述
- weibo_fans: 微博粉丝数（如果知道）
- douyin_fans: 抖音粉丝数（如果知道）

只返回JSON格式的列表，不要包含任何解释。"""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        result = await self.chat(messages, temperature=0.7)
        
        try:
            import re
            result = re.sub(r'<think[^>]*>[\s\S]*?</think\s*>', '', result, flags=re.IGNORECASE)
            if "```json" in result:
                match = re.search(r'```json\s*([\s\S]*?)\s*```', result)
                if match:
                    result = match.group(1)
            elif "```" in result:
                match = re.search(r'```\s*([\s\S]*?)\s*```', result)
                if match:
                    result = match.group(1)
            json_match = re.search(r'\[[\s\S]*\]', result)
            if json_match:
                result = json_match.group(0)
            result = result.strip()
            stars = json.loads(result)
            if isinstance(stars, list):
                return stars
            return []
        except Exception as e:
            error_msg = str(e)
            try:
                with open("minimax_error.log", "a", encoding="utf-8") as f:
                    f.write(f"Parse error: {error_msg}, result: {result[:500]}\n")
            except:
                pass
            return []
    
    async def complete_star_data(self, star_name: str) -> Dict[str, Any]:
        prompt = f"""请为明星"{star_name}"补全以下信息：
- weibo_fans: 微博粉丝数
- douyin_fans: 抖音粉丝数
- category: 所属类型（演员/歌手/主持人/导演/其他）
- level: 等级（顶流/一线/二线/三线）

请返回JSON格式。"""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        result = await self.chat(messages, temperature=0.7)
        
        try:
            if result.startswith("```json"):
                result = result[7:]
            if result.endswith("```"):
                result = result[:-3]
            data = json.loads(result)
            if isinstance(data, dict):
                return data
            return {}
        except Exception as e:
            with open("minimax_error.log", "a", encoding="utf-8") as f:
                f.write(f"Parse error: {str(e)}\n")
            return {}
    
    def analyze_star_level(self, fans_count: int, platform: str = "weibo") -> str:
        if platform == "weibo":
            if fans_count >= 50000000:
                return "顶流"
            elif fans_count >= 20000000:
                return "一线"
            elif fans_count >= 5000000:
                return "二线"
            else:
                return "三线"
        elif platform == "douyin":
            if fans_count >= 30000000:
                return "顶流"
            elif fans_count >= 10000000:
                return "一线"
            elif fans_count >= 3000000:
                return "二线"
            else:
                return "三线"
        return "三线"
