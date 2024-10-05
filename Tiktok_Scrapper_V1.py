import nodriver as uc
import asyncio
from bs4 import BeautifulSoup
import json



async def scrape_tiktok_profile(username):
    try:
        print(f"Initiating scrape for TikTok profile: @{username}")
        browser = await uc.start(headless=False)
        print("Browser started successfully")

        page = await browser.get(f"https://www.tiktok.com/@{username}")
        print("TikTok profile page loaded successfully")

        await asyncio.sleep(10)  # Wait for 10 seconds
        print("Waited for 10 seconds to allow content to load")


        html_content = await page.evaluate('document.documentElement.outerHTML')
        print(f"HTML content retrieved (length: {len(html_content)} characters)")


        soup = BeautifulSoup(html_content, 'html.parser')
        #script = soup.find('div', class_="product parbase").find('script').string 
        script = soup.css("script[type='text/javascript']")
        print(script)
    
        print("HTML content parsed with BeautifulSoup")


        profile_info = { 'username': soup.select_one('h1[data-e2e="user-title"]').text.strip() if soup.select_one('h1[data-e2e="user-title"]') else None,
                                'display_name': soup.select_one('h2[data-e2e="user-subtitle"]').text.strip() if soup.select_one('h2[data-e2e="user-subtitle"]') else None,
                                'follower_count': soup.select_one('strong[data-e2e="followers-count"]').text.strip() if soup.select_one('strong[data-e2e="followers-count"]') else None,
                                'following_count': soup.select_one('strong[data-e2e="following-count"]').text.strip() if soup.select_one('strong[data-e2e="following-count"]') else None,
                                'like_count': soup.select_one('strong[data-e2e="likes-count"]').text.strip() if soup.select_one('strong[data-e2e="likes-count"]') else None,
                                'bio': soup.select_one('h2[data-e2e="user-bio"]').text.strip() if soup.select_one('h2[data-e2e="user-bio"]') else None
                            }
        print("Profile information extracted successfully")

        return profile_info

    except Exception as e:
        print(f"An error occurred while scraping: {str(e)}")
        return None
    finally:
        if 'browser' in locals():
            browser.stop()
        print("Browser closed")



async def main():
    username = "Roxy-Crafty Elf"
    profile_info = await scrape_tiktok_profile(username)

    if profile_info:
        print("\nProfile Information:")
        for key, value in profile_info.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    else:
        print("Failed to scrape profile information.")

if __name__ == "__main__":
    uc.loop().run_until_complete(main())







