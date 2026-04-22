import re
import httpx
from typing import Dict, Any, List
from datetime import date
from bs4 import BeautifulSoup

class SimpleCrawler:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    def parse_number(self, text: str) -> int:
        if not text:
            return 0
        text = str(text).strip()
        text = re.sub(r'[^\d.万千百亿]', '', text)
        if not text:
            return 0
        try:
            if '亿' in text:
                num = float(text.replace('亿', ''))
                return int(num * 100000000)
            elif '万' in text:
                num = float(text.replace('万', ''))
                return int(num * 10000)
            elif '千' in text:
                num = float(text.replace('千', ''))
                return int(num * 1000)
            elif '百' in text:
                num = float(text.replace('百', ''))
                return int(num * 100)
            else:
                return int(float(text))
        except:
            return 0

class WeiboCrawler(SimpleCrawler):
    def __init__(self):
        super().__init__(timeout=30)
    
    async def search_user(self, keyword: str) -> List[Dict[str, Any]]:
        results = []
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                url = f"https://s.weibo.com/user?q={keyword}"
                response = await client.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    cards = soup.select('.card-wrap[action-type="user_item"]')
                    
                    for card in cards[:10]:
                        try:
                            name_elem = card.select_one('.name')
                            if not name_elem:
                                continue
                            
                            name = name_elem.get_text(strip=True)
                            user_link = name_elem.get('href', '')
                            
                            fans_text = ''
                            fans_elem = card.select_one('.info')
                            if fans_elem:
                                info_text = fans_elem.get_text()
                                fans_match = re.search(r'粉丝(\d+\.?\d*[万千百亿]?)', info_text)
                                if fans_match:
                                    fans_text = fans_match.group(1)
                            
                            verified = bool(card.select_one('.icon-vip') or card.select_one('.icon-vip-o'))
                            
                            avatar_elem = card.select_one('img')
                            avatar = avatar_elem.get('src', '') if avatar_elem else ''
                            
                            results.append({
                                'weibo_id': self._extract_user_id(user_link),
                                'weibo_name': name,
                                'fans_count': self.parse_number(fans_text),
                                'verified': verified,
                                'avatar': avatar,
                                'profile_url': user_link
                            })
                        except Exception as e:
                            print(f"Error parsing card: {e}")
                            continue
        except Exception as e:
            print(f"Error searching weibo user {keyword}: {e}")
        
        return results
    
    def _extract_user_id(self, url: str) -> str:
        match = re.search(r'/u/(\d+)', url)
        if match:
            return match.group(1)
        match = re.search(r'/(\d+)', url)
        if match:
            return match.group(1)
        return ''

class DouyinCrawler(SimpleCrawler):
    def __init__(self):
        super().__init__(timeout=30)
    
    async def search_user(self, keyword: str) -> List[Dict[str, Any]]:
        results = []
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                url = f"https://www.douyin.com/search/{keyword}?type=user"
                response = await client.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    items = soup.select('.search-user-item')
                    
                    for item in items[:10]:
                        try:
                            name_elem = item.select_one('.user-name')
                            if not name_elem:
                                continue
                            
                            name = name_elem.get_text(strip=True)
                            link = item.select_one('a')
                            href = link.get('href', '') if link else ''
                            
                            fans_elem = item.select_one('.user-fans')
                            fans_text = fans_elem.get_text(strip=True) if fans_elem else ''
                            
                            avatar_elem = item.select_one('img')
                            avatar = avatar_elem.get('src', '') if avatar_elem else ''
                            
                            verified_elem = item.select_one('.verified-icon')
                            
                            results.append({
                                'douyin_id': self._extract_douyin_id(href),
                                'douyin_name': name,
                                'fans_count': self.parse_number(fans_text),
                                'verified': bool(verified_elem),
                                'avatar': avatar,
                                'profile_url': f"https://www.douyin.com/user/{self._extract_douyin_id(href)}"
                            })
                        except Exception as e:
                            print(f"Error parsing douyin user: {e}")
                            continue
        except Exception as e:
            print(f"Error searching douyin user {keyword}: {e}")
        
        return results
    
    def _extract_douyin_id(self, url: str) -> str:
        match = re.search(r'/user/([A-Za-z0-9_-]+)', url)
        if match:
            return match.group(1)
        return ''

class XiaohongshuCrawler(SimpleCrawler):
    def __init__(self):
        super().__init__(timeout=30)
    
    async def search_user(self, keyword: str) -> List[Dict[str, Any]]:
        results = []
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                url = f"https://www.xiaohongshu.com/search_result?keyword={keyword}&type=user"
                response = await client.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'lxml')
                    items = soup.select('.user-item')
                    
                    for item in items[:10]:
                        try:
                            name_elem = item.select_one('.user-name')
                            if not name_elem:
                                continue
                            
                            name = name_elem.get_text(strip=True)
                            link = item.select_one('a')
                            href = link.get('href', '') if link else ''
                            
                            fans_elem = item.select_one('.user-fans')
                            fans_text = fans_elem.get_text(strip=True) if fans_elem else ''
                            
                            likes_elem = item.select_one('.user-likes')
                            likes_text = likes_elem.get_text(strip=True) if likes_elem else ''
                            
                            avatar_elem = item.select_one('img')
                            avatar = avatar_elem.get('src', '') if avatar_elem else ''
                            
                            verified_elem = item.select_one('.verified-icon')
                            
                            results.append({
                                'xhs_id': self._extract_xhs_id(href),
                                'xhs_name': name,
                                'fans_count': self.parse_number(fans_text),
                                'likes_collects_count': self.parse_number(likes_text),
                                'verified': bool(verified_elem),
                                'avatar': avatar,
                                'profile_url': f"https://www.xiaohongshu.com/user/profile/{self._extract_xhs_id(href)}"
                            })
                        except Exception as e:
                            print(f"Error parsing xiaohongshu user: {e}")
                            continue
        except Exception as e:
            print(f"Error searching xiaohongshu user {keyword}: {e}")
        
        return results
    
    def _extract_xhs_id(self, url: str) -> str:
        match = re.search(r'/user/profile/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        match = re.search(r'/user/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        return ''
