import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

baseurl = "https://jnovels.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}

page_url = "https://jnovels.com/light-novel-pdf-jp/"

r = requests.get(page_url, headers=headers)
soup = BeautifulSoup(r.content, "lxml")

lnlinks = []

for ol in soup.find_all("ol"):
    for li in ol.find_all("li"):
        a_tag = li.find("a", href=True)
        if not a_tag:
            continue

        href = a_tag["href"]
        title = a_tag.get_text(strip=True)

        if "-pdf" in href:
            full_link = urljoin(baseurl, href)
            lnlinks.append((title, full_link))

# Write results to a text file
with open("light_novels.txt", "w", encoding="utf-8") as f:
    for idx, (title, link) in enumerate(lnlinks, start=1):
        f.write(f"{idx}. {title}\n")
        f.write(f"{link}\n\n")

    f.write(f"Total light novels collected: {len(lnlinks)}\n")

print(f"Saved {len(lnlinks)} light novels to light_novels.txt")
