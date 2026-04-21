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
    
    print("\n浏览器已启动！")
    print("请在浏览器中手动操作：")
    print("1. 访问 https://www.xiaohongshu.com 并登录")
    print("2. 搜索一个明星名字（如：肖战）")
    print("3. 切换到用户搜索结果")
    print("4. 完成后按回车继续分析...")
    input()
    
    print("\n分析当前页面...")
    
    await page.screenshot(path="screenshot_xhs_manual.png")
    print("已保存截图: screenshot_xhs_manual.png")
    
    content = await page.content()
    with open("page_xhs_manual.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("已保存页面: page_xhs_manual.html")
    
    all_links = await page.query_selector_all('a')
    print(f"\n页面中所有链接数量: {len(all_links)}")
    
    user_links = []
    for link in all_links:
        try:
            href = await link.get_attribute('href')
            if href:
                text = await link.inner_text()
                user_links.append((href, text.strip() if text else ""))
        except:
            pass
    
    print(f"\n包含 user/profile 的链接:")
    for href, text in user_links:
        if 'user' in href.lower() or 'profile' in href.lower():
            print(f"  - {text}: {href}")
    
    print("\n按回车键关闭浏览器...")
    input()
    
    await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
