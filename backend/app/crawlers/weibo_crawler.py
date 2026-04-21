import re
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from app.crawlers.base import BaseCrawler
from bs4 import BeautifulSoup

class WeiboCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(timeout=30)
        self.search_url = "https://s.weibo.com/user"
    
    async def search_user(self, keyword: str) -> List[Dict[str, Any]]:
        results = []
        try:
            url = f"{self.search_url}?q={keyword}"
            content = await self.get_page_content(url, wait_selector=".card-wrap")
            
            if not content:
                return results
            
            soup = BeautifulSoup(content, 'lxml')
            cards = soup.select('.card-wrap[action-type="user_item"]')
            
            for card in cards[:10]:
                try:
                    name_elem = card.select_one('.name')
                    if not name_elem:
                        continue
                    
                    name = name_elem.get_text(strip=True)
                    user_link = name_elem.get('href', '')
                    user_id = self._extract_user_id(user_link)
                    
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
                        'weibo_id': user_id,
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
    
    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        result = {
            'weibo_id': user_id,
            'weibo_name': None,
            'fans_count': 0,
            'following_count': 0,
            'posts_count': 0,
            'verified': False,
            'verified_type': 0,
            'verified_reason': None,
            'description': None,
            'avatar': None,
            'collect_date': date.today()
        }
        
        try:
            url = f"https://weibo.com/u/{user_id}"
            content = await self.get_page_content(url)
            
            if not content:
                return result
            
            soup = BeautifulSoup(content, 'lxml')
            
            name_elem = soup.select_one('.ProfileHeader_name')
            if name_elem:
                result['weibo_name'] = name_elem.get_text(strip=True)
            
            fans_elem = soup.select_one('[data-key="followers"]')
            if fans_elem:
                result['fans_count'] = self.parse_number(fans_elem.get_text())
            
            following_elem = soup.select_one('[data-key="follows"]')
            if following_elem:
                result['following_count'] = self.parse_number(following_elem.get_text())
            
            posts_elem = soup.select_one('[data-key="weibo"]')
            if posts_elem:
                result['posts_count'] = self.parse_number(posts_elem.get_text())
            
            verified_elem = soup.select_one('.icon-vip')
            result['verified'] = bool(verified_elem)
            
            desc_elem = soup.select_one('.ProfileHeader_description')
            if desc_elem:
                result['description'] = desc_elem.get_text(strip=True)
            
            avatar_elem = soup.select_one('.ProfileHeader_avatar img')
            if avatar_elem:
                result['avatar'] = avatar_elem.get('src', '')
            
        except Exception as e:
            print(f"Error getting weibo user info {user_id}: {e}")
        
        return result
    
    async def get_hot_search(self, keyword: str) -> List[Dict[str, Any]]:
        results = []
        try:
            url = f"https://s.weibo.com/top/summary?cate=realtimehot"
            content = await self.get_page_content(url)
            
            if not content:
                return results
            
            soup = BeautifulSoup(content, 'lxml')
            items = soup.select('tbody tr')
            
            for item in items[:50]:
                try:
                    text_elem = item.select_one('td a')
                    if not text_elem:
                        continue
                    
                    text = text_elem.get_text(strip=True)
                    if keyword in text:
                        rank_elem = item.select_one('td:first-child')
                        rank = int(rank_elem.get_text(strip=True)) if rank_elem else 0
                        
                        hot_elem = item.select_one('td:last-child')
                        hot_value = self.parse_number(hot_elem.get_text()) if hot_elem else 0
                        
                        results.append({
                            'keyword': text,
                            'rank': rank,
                            'hot_value': hot_value,
                            'collect_date': date.today()
                        })
                except Exception as e:
                    print(f"Error parsing hot search item: {e}")
                    continue
            
        except Exception as e:
            print(f"Error getting hot search: {e}")
        
        return results
    
    def _extract_user_id(self, url: str) -> str:
        match = re.search(r'/u/(\d+)', url)
        if match:
            return match.group(1)
        match = re.search(r'/(\d+)', url)
        if match:
            return match.group(1)
        return ''
