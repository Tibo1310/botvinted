from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import VintedItem

app = Flask(__name__)

engine = create_engine('mysql://root:rootpassword@db/vinted_db')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/items', methods=['GET'])
def get_items():
    items = session.query(VintedItem).all()
    return jsonify([{'title': item.title, 'price': item.price} for item in items])

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
