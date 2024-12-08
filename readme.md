# Ice Cream Cafe Management Application

## Overview
This is a Python-based SQLite application for managing a fictional ice cream parlor cafe. The application allows management of seasonal flavors, ingredient inventory, and customer interactions.

## Features
- Maintain seasonal flavor offerings
- Track ingredient inventory
- Add and manage allergen information
- Shopping cart functionality
- Search and filter flavors

## Prerequisites
- Python 3.8+
- SQLite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ice-cream-cafe-app.git
cd ice-cream-cafe-app
```

2. Create a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python ice_cream_cafe.py
```

## Testing Steps

1. Add Flavors
- Verify flavor creation
- Check unique constraint on flavor names
- Test seasonal and non-seasonal flavors

2. Ingredient Management
- Add ingredients
- Verify quantity tracking
- Test unique ingredient constraints

3. Allergen Management
- Add new allergens
- Verify unique allergen constraints

4. Cart Functionality
- Add items to cart
- View cart contents
- Verify price calculations

## Docker Setup

### Build Docker Image
```bash
docker build -t ice-cream-cafe-app .
```

### Run Docker Container
```bash
docker run -p 8000:8000 ice-cream-cafe-app
```

## Database Schema
- `flavors`: Stores ice cream flavor details
- `ingredients`: Tracks ingredient inventory
- `allergens`: Manages known allergens
- `cart`: Maintains user's cart items

## Potential Improvements
- Add user authentication
- Implement order processing
- Create a web interface
- Add more advanced filtering

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
