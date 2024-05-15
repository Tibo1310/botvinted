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
        title = item.find('h3', class_='catalog-item-title').text.strip()
        price = item.find('div', class_='catalog-item-price').text.strip()
        
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
    save_items_to_db(items)
