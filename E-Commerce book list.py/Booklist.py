import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

BASE_URL = "https://books.toscrape.com/catalogue/page-{page}.html"


def scrape_books(pages=5):
    books = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        response = requests.get(BASE_URL.format(page=page), headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        for book in soup.select(".product_pod"):
            title = book.find("h3").find("a")["title"]
            raw_price = book.select_one(".price_color").get_text(strip=True)
            clean_price = "£" + raw_price.split("£")[-1]

            books.append({
                "Book Name": title,
                "Price":     clean_price,
            })

    return books


if __name__ == "__main__":
    books = scrape_books(pages=5)
    df = pd.DataFrame(books)
    df.to_csv("books.csv", index=False, encoding="utf-8-sig")
    print(f"Done! {len(books)} books saved.")