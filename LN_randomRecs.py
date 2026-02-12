import customtkinter as ctk
import requests
import random
import webbrowser
import re
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LNRandApp(ctk.CTk):
    def __init__(self, ln_list):
        super().__init__()
        self.ln_list = ln_list
        self.current_link = ""
        
        # --- SIZE DEFINITIONS ---
        self.wide_size = (400, 225)   # For NA and Matte
        self.cover_size = (250, 350)  # For actual Book Covers
        
        try:
            # Load wide assets
            na_pil = Image.open("NA.png")
            self.na_image = ctk.CTkImage(light_image=na_pil, size=self.wide_size)
            
            load_pil = Image.open("matte2.jpg")
            self.load_image = ctk.CTkImage(light_image=load_pil, size=self.wide_size)
        except Exception as e:
            print(f"Error loading assets: {e}")
            self.na_image = None
            self.load_image = None

        # --- WINDOW SETUP ---
        self.title("Light Novel Gacha version 0.10")
        self.geometry("1000x850")
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="CONTROLS", font=("Arial", 20, "bold")).pack(pady=20)
        self.shuffle_button = ctk.CTkButton(self.sidebar, text="✨ GACHA", command=self.pick_novel, 
                                            height=60, font=("Arial", 16, "bold"), 
                                            fg_color="#8e44ad", hover_color="#9b59b6")
        self.shuffle_button.pack(pady=10, padx=20, fill="x")
        self.dl_button = ctk.CTkButton(self.sidebar, text="🔗 JNOVELS PAGE", command=self.open_link, fg_color="gray25")
        self.dl_button.pack(pady=10, padx=20, fill="x")

        # --- MAIN CONTENT ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Initial state is wide
        self.cover_label = ctk.CTkLabel(self.main_frame, text="", image=self.na_image)
        self.cover_label.pack(pady=15)

        self.res_title = ctk.CTkTextbox(self.main_frame, height=70, font=("Arial", 24, "bold"), 
                                        fg_color="transparent", border_width=0, activate_scrollbars=False)
        self.res_title.pack(pady=5, fill="x")
        self.res_title.tag_config("center", justify='center')
        self.update_text_widget(self.res_title, "Ready to Roll?")

        self.res_stats = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 14, "bold"), text_color="#f1c40f")
        self.res_stats.pack(pady=2)
        
        self.res_author = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 15, "italic"), text_color="#3498db")
        self.res_author.pack()

        self.res_synopsis = ctk.CTkTextbox(self.main_frame, width=700, height=250, wrap="word", font=("Arial", 13))
        self.res_synopsis.pack(pady=10, fill="x")
        self.res_synopsis.configure(state="disabled")

    def update_text_widget(self, widget, content):
        widget.configure(state="normal")
        widget.delete("0.0", "end")
        widget.insert("0.0", content)
        if widget == self.res_title:
            widget.tag_add("center", "1.0", "end")
        widget.configure(state="disabled")

    def clear_previous_data(self):
        """Wipes UI and displays the wide matte2.jpg"""
        self.res_stats.configure(text="")
        self.res_author.configure(text="")
        # Set to wide loading image
        self.cover_label.configure(image=self.load_image)
        self.update_text_widget(self.res_title, "Rolling...")
        self.update_text_widget(self.res_synopsis, "")

    def scrape_jnovels_details(self, url):
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=7)
            soup = BeautifulSoup(r.content, "lxml")
            
            # 1. Targeting the featured-media div
            img_div = soup.find("div", class_="featured-media")
            img_url = None
            
            if img_div:
                img_tag = img_div.find("img")
                if img_tag:
                    # Check for Lazy Loading attributes first, fallback to src
                    img_url = (img_tag.get("data-lazy-src") or 
                               img_tag.get("data-src") or 
                               img_tag.get("src"))

            # 2. Count Volumes (Improved targeting)
            content = soup.find("div", class_="post-content clear") or soup.find("div", class_="entry-content")
            total_vols = 0
            if content:
                # We specifically look for list items containing links
                for ol in content.find_all("ol"):
                    for li in ol.find_all("li"):
                        if li.find("a"): 
                            total_vols += 1
                            
            return img_url, total_vols
        except Exception as e:
            print(f"Scrape Error: {e}")
            return None, 0

    def get_mal_metadata(self, title):
        clean_q = re.sub(r'Light Novel|PDF|EPUB|Vol\.|Volume|\d+', '', title, flags=re.IGNORECASE).strip()
        try:
            resp = requests.get("https://api.jikan.moe/v4/manga", params={"q": clean_q, "type": "lightnovel", "limit": 1}, timeout=5)
            if resp.status_code == 200:
                data = resp.json().get('data')
                if data:
                    item = data[0]
                    creators = [f"{a['name'].split(',')[1].strip()} {a['name'].split(',')[0].strip()}" if ',' in a['name'] else a['name'] for a in item.get('authors', [])]
                    return {
                        "rating": f"{item.get('score'):.2f}/10" if item.get('score') else "N/A",
                        "status": item.get('status', "Unknown"),
                        "synopsis": item.get('synopsis', "No description found."),
                        "authors": " • ".join(creators)
                    }
        except: return None

    def pick_novel(self):
        self.clear_previous_data()
        self.update()

        title_raw, link = random.choice(self.ln_list)
        self.current_link = link
        img_url, vol_count = self.scrape_jnovels_details(link)
        mal = self.get_mal_metadata(title_raw)

        self.update_text_widget(self.res_title, title_raw)
        
        rating = mal['rating'] if mal else "N/A"
        status = mal['status'] if mal else "Unknown"
        self.res_stats.configure(text=f"⭐ Rating: {rating}  |  Status: {status}  |  Volumes downloadable: {vol_count}")
        
        if mal:
            self.res_author.configure(text=f"Creators: {mal['authors']}")
            self.update_text_widget(self.res_synopsis, mal['synopsis'])
        
        self.update_image(img_url)

    def update_image(self, url):
        """Uses vertical ratio for real covers and wide ratio for placeholders"""
        if not url:
            self.cover_label.configure(image=self.na_image) # Reverts to Wide NA
            return
        try:
            r = requests.get(url, timeout=5)
            img = Image.open(BytesIO(r.content))
            # FIX: Real covers use vertical self.cover_size (250x350)
            self.cover_label.configure(image=ctk.CTkImage(light_image=img, size=self.cover_size))
        except: 
            self.cover_label.configure(image=self.na_image)

    def open_link(self):
        if self.current_link: webbrowser.open(self.current_link)

def initial_scrape():
    url = "https://jnovels.com/light-novel-pdf-jp/"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.content, "lxml")
        return [(li.get_text(strip=True), urljoin(url, li.a["href"])) for li in soup.select("ol li") if li.a]
    except: return []

if __name__ == "__main__":
    my_novels = initial_scrape()
    if my_novels:
        app = LNRandApp(my_novels)
        app.mainloop()