import asyncio
import sys
import os
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

from app.database import SessionLocal
from app.models.models import Star, XiaohongshuData
from playwright.async_api import async_playwright


USER_DATA_DIR = Path(__file__).parent / "browser_data_xiaohongshu"


async def main():
    db = SessionLocal()
    
    async with async_playwright() as p:
        print("正在启动浏览器...")
        print(f"浏览器数据目录: {USER_DATA_DIR}")
        print("请在浏览器中登录小红书...")
        print("登录完成后，按回车继续采集...")
        input()
        
        page = await p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_dir),
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            args=['--disable-blink-features=AutomationControlled']
        ).new_page()
        
        print("\n浏览器窗口已打开！请在浏览器中登录小红书...")
        print("登录完成后，在终端窗口中按回车键继续...")
        
        stars = db.query(Star).filter(~Star.xiaohongshu_data.any()).limit(30).all()
        print(f"\n需要采集小红书数据的明星: {len(stars)} 个")
        
        added = 0
        for i, star in enumerate(stars):
            print(f"\n[{i+1}/{len(stars)}] {star.name}")
            
            try:
                search_url = f"https://www.xiaohongshu.com/search_result?keyword={star.name}&type=user"
                await page.goto(search_url, wait_until='networkidle', timeout=30000)
                await asyncio.sleep(3)
                
                await page.screenshot(path=f"screenshot_xhs_{i}.png")
                
                user_links = await page.query_selector_all('a[href*="/user/profile/"]')
                print(f"  找到 {len(user_links)} 个用户链接")
                
                if user_links:
                    link = user_links[0]
                    href = await link.get_attribute('href')
                    text = await link.inner_text()
                    xhs_id = href.split('/user/profile/')[-1].split('?')[0] if href else None
                        text = await link.inner_text()
                        if text.strip():
                            xhs_id = xhs_id
                        if href:
                            xhs_id = xhs_id.split('?')[0] if '?' else:
                            xhs_id = xhs_id
                        
                        xhs_data = XiaohongshuData(
                            star_id=star.id,
                            xhs_name=text.strip(),
                            xhs_id=xhs_id,
                            fans_count=0,
                            has_official_account=True,
                            collect_date=date.today()
                        )
                        db.add(xhs_data)
                        db.commit()
                        added += 1
                        print(f"  已添加: {text.strip()}")
                    else:
                        print(f"  未找到")
                
                except Exception as e:
                    print(f"  错误: {e}")
                
                await asyncio.sleep(2)
        
        await context.close()
        print(f"\n完成！共添加 {added} 条小红书数据")
    
    db.close()


if __name__ == "__main__":
    asyncio.run(main())
