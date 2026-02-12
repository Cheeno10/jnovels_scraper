<br>

<p align="center">
  <img src="fate-summon.gif" alt="Light Novel Gacha Demo" width="600">
</p>

# Light Novel Gacha

Light Novel Gacha is a desktop application designed to help users discover new light novels through a randomized gacha-style selection system.

The application scrapes live data from JNovels to retrieve available volumes and cover art, and integrates with the Jikan API (MyAnimeList) to fetch additional metadata such as ratings, authors, publication status, and synopses.

---

## Overview

Light Novel Gacha combines live web scraping with external API integration to provide dynamic recommendations. Each roll selects a random title from a large catalog of light novels and presents detailed information in a clean, selectable user interface.

The application is built with Python and uses CustomTkinter for the graphical interface.

---

## Features

- **Gacha System**  
  Instantly pull a random light novel from a large, dynamically scraped catalog.

- **Live Scraping**  
  Retrieves volume counts and cover images directly from JNovels.

- **Live Metadata Integration**  
  Fetches MyAnimeList scores, author information, and publication status using the Jikan API.

- **Selectable UI Fields**  
  Title and synopsis fields allow text highlighting and copying.

- **Direct Access**  
  One-click button to open the official JNovels page for verification and downloads.

---

## Installation

### Requirements

- Python 3.x

### Install Dependencies

```bash
pip install customtkinter requests pillow beautifulsoup4 lxml
```

### Run the Application

```bash
python LN_randomRecs.py
```

---

## Dependencies

- **CustomTkinter** — Modern UI framework for Tkinter  
- **Requests** — HTTP requests for web scraping and API calls  
- **BeautifulSoup4** — HTML parsing  
- **LXML** — Fast HTML parser  
- **Jikan API** — Unofficial MyAnimeList API wrapper  

---

## Disclaimer

### Metadata Accuracy
Because data is retrieved from multiple external sources, descriptions and author information may occasionally not perfectly align with the title and displayed cover image. But for the most part it works just fine.
