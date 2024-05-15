import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import VintedItem, Base
import os

# Charger l'URL de la base de données depuis les variables d'environnement
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# S'assurer que les tables sont créées
Base.metadata.create_all(engine)

def fetch_vinted_items():
    url = "https://www.vinted.fr/catalog?search_text=dracaufeu+223/197"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    items = []
    for item in soup.find_all('div', class_='catalog-item'):
        title_element = item.find('div', {'data-testid': lambda x: x and 'title-container' in x})
        price_element = item.find('p', {'data-testid': lambda x: x and 'price-text' in x})
        
        if title_element and price_element:
            title = title_element.get_text(strip=True)
            price = price_element.get_text(strip=True)
            if "dracaufeu 223/197" in title.lower():
                items.append({
                    'title': title,
                    'price': price
                })
    
    return items

def save_items_to_db(items):
    for item in items:
        vinted_item = VintedItem(
            title=item['title'],
            price=item['price'],
        )
        session.add(vinted_item)
    session.commit()

if __name__ == "__main__":
    items = fetch_vinted_items()
    print(f"Fetched items: {items}")
    save_items_to_db(items)
    print("Items saved to database.")
