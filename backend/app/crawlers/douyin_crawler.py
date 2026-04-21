import re
from typing import Dict, Any, List
from datetime import datetime, date
from app.crawlers.base import BaseCrawler
from bs4 import BeautifulSoup

class DouyinCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(timeout=30)
        self.search_url = "https://www.douyin.com/search"
    
    async def search_user(self, keyword: str) -> List[Dict[str, Any]]:
        results = []
        try:
            url = f"{self.search_url}/{keyword}"
            content = await self.get_page_content(url, wait_selector=".search-user-item")
            
            if not content:
                return results
            
            soup = BeautifulSoup(content, 'lxml')
            items = soup.select('.search-user-item')
            
            for item in items[:10]:
                try:
                    name_elem = item.select_one('.user-name')
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    link = item.select_one('a')
                    href = link.get('href', '') if link else ''
                    douyin_id = self._extract_douyin_id(href)
                    
                    fans_elem = item.select_one('.user-fans')
                    fans_text = fans_elem.get_text(strip=True) if fans_elem else ''
                    
                    avatar_elem = item.select_one('img')
                    avatar = avatar_elem.get('src', '') if avatar_elem else ''
                    
                    verified_elem = item.select_one('.verified-icon')
                    
                    results.append({
                        'douyin_id': douyin_id,
                        'douyin_name': name,
                        'fans_count': self.parse_number(fans_text),
                        'verified': bool(verified_elem),
                        'avatar': avatar,
                        'profile_url': f"https://www.douyin.com/user/{douyin_id}"
                    })
                except Exception as e:
                    print(f"Error parsing douyin user: {e}")
                    continue
            
        except Exception as e:
            print(f"Error searching douyin user {keyword}: {e}")
        
        return results
    
    async def get_user_info(self, douyin_id: str) -> Dict[str, Any]:
        result = {
            'douyin_id': douyin_id,
            'douyin_name': None,
            'unique_id': None,
            'fans_count': 0,
            'following_count': 0,
            'likes_count': 0,
            'video_count': 0,
            'verified': False,
            'avatar': None,
            'signature': None,
            'collect_date': date.today()
        }
        
        try:
            url = f"https://www.douyin.com/user/{douyin_id}"
            content = await self.get_page_content(url)
            
            if not content:
                return result
            
            soup = BeautifulSoup(content, 'lxml')
            
            name_elem = soup.select_one('[data-e2e="user-page"] .user-title')
            if not name_elem:
                name_elem = soup.select_one('.user-nickname')
            if name_elem:
                result['douyin_name'] = name_elem.get_text(strip=True)
            
            fans_elem = soup.select_one('[data-e2e="follow"] .count')
            if not fans_elem:
                fans_elem = soup.select_one('.follower-count')
            if fans_elem:
                result['fans_count'] = self.parse_number(fans_elem.get_text())
            
            likes_elem = soup.select_one('[data-e2e="liked"] .count')
            if not likes_elem:
                likes_elem = soup.select_one('.liked-count')
            if likes_elem:
                result['likes_count'] = self.parse_number(likes_elem.get_text())
            
            video_elem = soup.select_one('[data-e2e="post"] .count')
            if not video_elem:
                video_elem = soup.select_one('.video-count')
            if video_elem:
                result['video_count'] = self.parse_number(video_elem.get_text())
            
            avatar_elem = soup.select_one('[data-e2e="user-page"] img')
            if not avatar_elem:
                avatar_elem = soup.select_one('.avatar img')
            if avatar_elem:
                result['avatar'] = avatar_elem.get('src', '')
            
            verified_elem = soup.select_one('.verified-icon')
            result['verified'] = bool(verified_elem)
            
            sig_elem = soup.select_one('[data-e2e="user-page"] .signature')
            if not sig_elem:
                sig_elem = soup.select_one('.signature')
            if sig_elem:
                result['signature'] = sig_elem.get_text(strip=True)
            
        except Exception as e:
            print(f"Error getting douyin user info {douyin_id}: {e}")
        
        return result
    
    def _extract_douyin_id(self, url: str) -> str:
        match = re.search(r'/user/([A-Za-z0-9_-]+)', url)
        if match:
            return match.group(1)
        return ''
