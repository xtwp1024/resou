import asyncio
import re
from abc import ABC, abstractmethod
from datetime import datetime, date
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, Page
import httpx
from bs4 import BeautifulSoup

class BaseCrawler(ABC):
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.browser: Optional[Browser] = None
    
    async def init_browser(self):
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
    
    async def close_browser(self):
        if self.browser:
            await self.browser.close()
    
    async def get_page_content(self, url: str, wait_selector: str = None) -> str:
        if not self.browser:
            await self.init_browser()
        
        page = await self.browser.new_page()
        try:
            await page.goto(url, timeout=self.timeout * 1000)
            if wait_selector:
                await page.wait_for_selector(wait_selector, timeout=self.timeout * 1000)
            else:
                await asyncio.sleep(2)
            content = await page.content()
            return content
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""
        finally:
            await page.close()
    
    def parse_number(self, text: str) -> int:
        if not text:
            return 0
        
        text = text.strip()
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
    
    @abstractmethod
    async def search_user(self, keyword: str) -> list:
        pass
    
    @abstractmethod
    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        pass
