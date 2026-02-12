import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 1. FUNCTION UPDATED TO INCLUDE RATING (SCORE)
def get_mal_info(title):
    # Clean the title for better search results
    search_query = title.replace("Light Novel", "").replace("PDF", "").replace("EPUB", "").strip()
    
    search_url = "https://api.jikan.moe/v4/manga"
    params = {
        "q": search_query,
        "type": "lightnovel",
        "limit": 1
    }
    
    try:
        time.sleep(1) # Crucial to avoid API rate-limit bans
        response = requests.get(search_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['data']:
                result = data['data'][0]
                return {
                    "description": result.get('synopsis', "No description found."),
                    "status": result.get('status', "Unknown"),
                    "volumes": result.get('volumes', "Unknown"),
                    "score": result.get('score', "N/A") # Get the MAL Rating
                }
        return {"description": "Not found", "status": "Unknown", "volumes": "Unknown", "score": "N/A"}
    except Exception:
        return {"description": "Error", "status": "Error", "volumes": "Error", "score": "Error"}

# 2. MAIN SCRAPER SETUP
baseurl = "https://jnovels.com"
headers = {"User-Agent": "Mozilla/5.0"}
page_url = "https://jnovels.com/light-novel-pdf-jp/"

print("Scraping JNovels for links...")
r = requests.get(page_url, headers=headers)
soup = BeautifulSoup(r.content, "lxml")

lnlinks = []
for ol in soup.find_all("ol"):
    for li in ol.find_all("li"):
        a_tag = li.find("a", href=True)
        if not a_tag: continue
        
        href = a_tag["href"]
        title = a_tag.get_text(strip=True)
        
        if "-pdf" in href:
            full_link = urljoin(baseurl, href)
            lnlinks.append((title, full_link))

total_novels = len(lnlinks)
print(f"Collected {total_novels} titles. Starting MAL data fetch (this will take ~25 mins)...")

# 3. WRITING TO FILE WITH RATING INCLUDED
with open("light_novels_detailed.txt", "w", encoding="utf-8") as f:
    # Processing the FULL list now
    for idx, (title, link) in enumerate(lnlinks, start=1):
        # Progress tracking in the console
        print(f"[{idx}/{total_novels}] Fetching: {title}")
        
        info = get_mal_info(title)
        
        vol_count = info['volumes'] if info['volumes'] else "Ongoing"
        rating = f"{info['score']}/10" if info['score'] != "N/A" else "No Rating Available"
        
        f.write(f"{idx}. {title}\n")
        f.write(f"Link: {link}\n")
        f.write(f"MAL Rating: {rating}\n")
        f.write(f"Status: {info['status']}\n")
        f.write(f"Volumes: {vol_count}\n")
        f.write(f"Description: {info['description']}\n")
        f.write("-" * 60 + "\n\n")

print("\nDone! All data saved to light_novels_detailed.txt")