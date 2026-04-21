import asyncio
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from app.database import SessionLocal
from app.models.models import Star, XiaohongshuData


async def main():
    from playwright.async_api import async_playwright
    
    print("正在启动浏览器...")
    
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,
        args=['--start-maximized', '--disable-blink-features=AutomationControlled']
    )
    
    context = await browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = await context.new_page()
    
    print("浏览器已启动，正在打开小红书...")
    
    await page.goto("https://www.xiaohongshu.com", wait_until='networkidle', timeout=60000)
    await asyncio.sleep(5)
    
    print("请在浏览器中登录小红书，登录后脚本会自动继续...")
    print("等待登录中... (最多等待60秒)")
    
    for i in range(60):
        await asyncio.sleep(1)
        logged_in = await page.query_selector('a[href*="/user/profile/"], [class*="user-name"], [class*="nickname"]')
        if logged_in:
            print("检测到已登录，开始采集...")
            break
    
    db = SessionLocal()
    
    stars = db.query(Star).filter(~Star.xiaohongshu_data.any()).limit(20).all()
    print(f"\n需要采集: {len(stars)} 个明星")
    
    added = 0
    for i, star in enumerate(stars):
        print(f"\n[{i+1}/{len(stars)}] {star.name}")
        
        try:
            url = f"https://www.xiaohongshu.com/search_result?keyword={star.name}&type=user"
            await page.goto(url, timeout=30000)
            await asyncio.sleep(3)
            
            links = await page.query_selector_all('a[href*="/user/profile/"]')
            print(f"  找到 {len(links)} 个用户")
            
            if links:
                link = links[0]
                href = await link.get_attribute('href')
                text = await link.inner_text()
                
                if text.strip() and href:
                    xhs_id = href.split('/user/profile/')[-1].split('?')[0]
                    
                    data = XiaohongshuData(
                        star_id=star.id,
                        xhs_name=text.strip(),
                        xhs_id=xhs_id,
                        fans_count=0,
                        has_official_account=True,
                        collect_date=date.today()
                    )
                    db.add(data)
                    db.commit()
                    added += 1
                    print(f"  已添加: {text.strip()}")
        except Exception as e:
            print(f"  错误: {e}")
        
        await asyncio.sleep(2)
    
    await browser.close()
    db.close()
    print(f"\n完成! 共添加 {added} 条")


if __name__ == "__main__":
    asyncio.run(main())
