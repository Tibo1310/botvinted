from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import VintedItem
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/items', methods=['GET'])
def get_items():
    items = session.query(VintedItem).all()
    return jsonify([{'title': item.title, 'price': item.price} for item in items])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
