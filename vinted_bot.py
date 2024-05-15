import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import VintedItem, Base
import os
import logging

# Configurer les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    for item in soup.find_all('div', class_='feed-grid__item'):
        title_tag = item.find('div', class_='new-item-box__title')
        price_tag = item.find('p', class_='web_ui__Text__text web_ui__Text__subtitle web_ui__Text__left web_ui__Text__amplified web_ui__Text__bold')

        if title_tag and price_tag:
            title = title_tag.text.strip()
            price = price_tag.text.strip()
            
            if "dracaufeu 223/197" in title.lower():
                items.append({
                    'title': title,
                    'price': price
                })
    
    logger.info(f"Fetched {len(items)} items from Vinted.")
    return items

def save_items_to_db(items):
    for item in items:
        vinted_item = VintedItem(
            title=item['title'],
            price=item['price'],
        )
        session.add(vinted_item)
    session.commit()
    logger.info(f"Saved {len(items)} items to the database.")

if __name__ == "__main__":
    items = fetch_vinted_items()
    save_items_to_db(items)
