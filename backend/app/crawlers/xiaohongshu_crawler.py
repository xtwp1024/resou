import re
from typing import Dict, Any, List
from datetime import datetime, date
from app.crawlers.base import BaseCrawler
from bs4 import BeautifulSoup

class XiaohongshuCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(timeout=30)
        self.search_url = "https://www.xiaohongshu.com/search_result"
    
    async def search_user(self, keyword: str) -> List[Dict[str, Any]]:
        results = []
        try:
            url = f"{self.search_url}?keyword={keyword}&type=user"
            content = await self.get_page_content(url, wait_selector=".user-item")
            
            if not content:
                return results
            
            soup = BeautifulSoup(content, 'lxml')
            items = soup.select('.user-item')
            
            for item in items[:10]:
                try:
                    name_elem = item.select_one('.user-name')
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    link = item.select_one('a')
                    href = link.get('href', '') if link else ''
                    xhs_id = self._extract_xhs_id(href)
                    
                    fans_elem = item.select_one('.user-fans')
                    fans_text = fans_elem.get_text(strip=True) if fans_elem else ''
                    
                    likes_elem = item.select_one('.user-likes')
                    likes_text = likes_elem.get_text(strip=True) if likes_elem else ''
                    
                    avatar_elem = item.select_one('img')
                    avatar = avatar_elem.get('src', '') if avatar_elem else ''
                    
                    verified_elem = item.select_one('.verified-icon')
                    
                    results.append({
                        'xhs_id': xhs_id,
                        'xhs_name': name,
                        'fans_count': self.parse_number(fans_text),
                        'likes_collects_count': self.parse_number(likes_text),
                        'verified': bool(verified_elem),
                        'avatar': avatar,
                        'profile_url': f"https://www.xiaohongshu.com/user/profile/{xhs_id}"
                    })
                except Exception as e:
                    print(f"Error parsing xiaohongshu user: {e}")
                    continue
            
        except Exception as e:
            print(f"Error searching xiaohongshu user {keyword}: {e}")
        
        return results
    
    async def get_user_info(self, xhs_id: str) -> Dict[str, Any]:
        result = {
            'xhs_id': xhs_id,
            'xhs_name': None,
            'fans_count': 0,
            'following_count': 0,
            'likes_collects_count': 0,
            'notes_count': 0,
            'verified': False,
            'has_official_account': False,
            'avatar': None,
            'signature': None,
            'collect_date': date.today()
        }
        
        try:
            url = f"https://www.xiaohongshu.com/user/profile/{xhs_id}"
            content = await self.get_page_content(url)
            
            if not content:
                return result
            
            soup = BeautifulSoup(content, 'lxml')
            
            name_elem = soup.select_one('.user-name')
            if name_elem:
                result['xhs_name'] = name_elem.get_text(strip=True)
            
            fans_elem = soup.select_one('.fans .count')
            if fans_elem:
                result['fans_count'] = self.parse_number(fans_elem.get_text())
            
            following_elem = soup.select_one('.follows .count')
            if following_elem:
                result['following_count'] = self.parse_number(following_elem.get_text())
            
            likes_elem = soup.select_one('.liked .count')
            if likes_elem:
                result['likes_collects_count'] = self.parse_number(likes_elem.get_text())
            
            notes_elem = soup.select_one('.notes .count')
            if notes_elem:
                result['notes_count'] = self.parse_number(notes_elem.get_text())
            
            avatar_elem = soup.select_one('.avatar img')
            if avatar_elem:
                result['avatar'] = avatar_elem.get('src', '')
            
            verified_elem = soup.select_one('.verified-icon')
            result['verified'] = bool(verified_elem)
            
            sig_elem = soup.select_one('.user-desc')
            if sig_elem:
                result['signature'] = sig_elem.get_text(strip=True)
            
            result['has_official_account'] = result['verified'] or bool(result['xhs_name'])
            
        except Exception as e:
            print(f"Error getting xiaohongshu user info {xhs_id}: {e}")
        
        return result
    
    def _extract_xhs_id(self, url: str) -> str:
        match = re.search(r'/user/profile/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        match = re.search(r'/user/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        return ''
