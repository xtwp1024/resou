import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'


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
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    )
    page = await context.new_page()
    
    print("正在打开小红书首页...")
    await page.goto("https://www.xiaohongshu.com", wait_until='networkidle', timeout=60000)
    await asyncio.sleep(5)
    
    print("等待登录... (60秒)")
    for i in range(60):
        await asyncio.sleep(1)
    
    print("\n正在搜索: 肖战")
    await page.goto("https://www.xiaohongshu.com/search_result?keyword=肖战&type=user", timeout=30000)
    await asyncio.sleep(5)
    
    await page.screenshot(path="screenshot_xhs_debug.png")
    print("已保存截图: screenshot_xhs_debug.png")
    
    content = await page.content()
    with open("page_xhs_debug.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("已保存页面: page_xhs_debug.html")
    
    print("\n分析页面元素...")
    
    all_links = await page.query_selector_all('a')
    print(f"页面中所有链接数量: {len(all_links)}")
    
    user_links = []
    for link in all_links:
        try:
            href = await link.get_attribute('href')
            if href and ('user' in href.lower() or 'profile' in href.lower()):
                text = await link.inner_text()
                user_links.append((href, text.strip()))
        except:
            pass
    
    print(f"\n包含 user/profile 的链接: {len(user_links)}")
    for href, text in user_links[:10]:
        print(f"  - {text}: {href}")
    
    all_divs = await page.query_selector_all('div')
    print(f"\n页面中所有 div 数量: {len(all_divs)}")
    
    print("\n请在浏览器中手动查看页面结构")
    print("按回车键关闭浏览器...")
    input()
    
    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
