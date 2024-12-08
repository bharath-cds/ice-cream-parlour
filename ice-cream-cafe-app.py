import sqlite3
import os
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Flavor:
    id: Optional[int] = None
    name: str = ''
    description: str = ''
    is_seasonal: bool = False
    price: float = 0.0

@dataclass
class Ingredient:
    id: Optional[int] = None
    name: str = ''
    quantity: float = 0.0
    unit: str = 'grams'

@dataclass
class Allergen:
    id: Optional[int] = None
    name: str = ''

@dataclass
class Cart:
    id: Optional[int] = None
    flavor_id: int = 0
    quantity: int = 1

class IceCreamCafeDatabase:
    def __init__(self, db_path: str = 'ice_cream_cafe.db'):
        """Initialize database connection and create tables if not exist."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create necessary tables if they don't exist."""
        # Flavors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flavors (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                description TEXT,
                is_seasonal BOOLEAN,
                price REAL
            )
        ''')

        # Ingredients table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                quantity REAL,
                unit TEXT
            )
        ''')

        # Allergens table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS allergens (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE
            )
        ''')

        # Cart table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY,
                flavor_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY(flavor_id) REFERENCES flavors(id)
            )
        ''')
        self.conn.commit()

    def add_flavor(self, flavor: Flavor) -> int:
        """Add a new flavor to the database."""
        try:
            self.cursor.execute('''
                INSERT INTO flavors (name, description, is_seasonal, price)
                VALUES (?, ?, ?, ?)
            ''', (flavor.name, flavor.description, flavor.is_seasonal, flavor.price))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Flavor {flavor.name} already exists.")
            return -1

    def add_ingredient(self, ingredient: Ingredient) -> int:
        """Add a new ingredient to the database."""
        try:
            self.cursor.execute('''
                INSERT INTO ingredients (name, quantity, unit)
                VALUES (?, ?, ?)
            ''', (ingredient.name, ingredient.quantity, ingredient.unit))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Ingredient {ingredient.name} already exists.")
            return -1

    def add_allergen(self, allergen: Allergen) -> int:
        """Add a new allergen to the database."""
        try:
            self.cursor.execute('''
                INSERT INTO allergens (name)
                VALUES (?)
            ''', (allergen.name,))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Allergen {allergen.name} already exists.")
            return -1

    def search_flavors(self, keyword: str = '', is_seasonal: Optional[bool] = None) -> List[Flavor]:
        """Search and filter flavors."""
        query = "SELECT * FROM flavors WHERE 1=1 "
        params = []

        if keyword:
            query += "AND (name LIKE ? OR description LIKE ?) "
            params.extend([f'%{keyword}%', f'%{keyword}%'])

        if is_seasonal is not None:
            query += "AND is_seasonal = ? "
            params.append(is_seasonal)

        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        return [Flavor(id=row[0], name=row[1], description=row[2], 
                       is_seasonal=bool(row[3]), price=row[4]) for row in results]

    def add_to_cart(self, flavor_id: int, quantity: int = 1) -> int:
        """Add a flavor to the cart."""
        self.cursor.execute('''
            INSERT INTO cart (flavor_id, quantity)
            VALUES (?, ?)
        ''', (flavor_id, quantity))
        self.conn.commit()
        return self.cursor.lastrowid

    def view_cart(self) -> List[Dict]:
        """View cart contents with flavor details."""
        self.cursor.execute('''
            SELECT cart.id, cart.quantity, flavors.name, flavors.price
            FROM cart
            JOIN flavors ON cart.flavor_id = flavors.id
        ''')
        results = self.cursor.fetchall()
        return [
            {
                'cart_id': row[0], 
                'quantity': row[1], 
                'flavor_name': row[2], 
                'unit_price': row[3],
                'total_price': row[1] * row[3]
            } for row in results
        ]

    def close(self):
        """Close database connection."""
        self.conn.close()

def main():
    # Example usage
    db = IceCreamCafeDatabase()

    # Add some initial flavors
    db.add_flavor(Flavor(name="Summer Strawberry", description="Fresh strawberry delight", is_seasonal=True, price=4.99))
    db.add_flavor(Flavor(name="Classic Vanilla", description="Traditional favorite", is_seasonal=False, price=3.99))

    # Add some ingredients
    db.add_ingredient(Ingredient(name="Fresh Strawberries", quantity=500, unit="grams"))
    db.add_ingredient(Ingredient(name="Vanilla Beans", quantity=100, unit="grams"))

    # Add some allergens
    db.add_allergen(Allergen(name="Milk"))
    db.add_allergen(Allergen(name="Nuts"))

    # Search and demonstrate functionality
    seasonal_flavors = db.search_flavors(is_seasonal=True)
    print("Seasonal Flavors:", [flavor.name for flavor in seasonal_flavors])

    # Add to cart
    flavor_id = db.search_flavors(keyword="Strawberry")[0].id
    db.add_to_cart(flavor_id, 2)

    # View cart
    cart_contents = db.view_cart()
    print("Cart Contents:", cart_contents)

    db.close()

if __name__ == "__main__":
    main()
