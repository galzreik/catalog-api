# Import the FastAPI class from the fastapi package.
# We need this class to create the main API application.
from fastapi import FastAPI

# Import the categories and products modules from our routers package.
# This gives main.py access to the router objects created inside
# routers/categories.py and routers/products.py.
from routers import categories, products


# Create the main FastAPI application.
# The variable "app" represents our entire API and will later
# connect the different routers, such as products and categories.
# This creates an instance of the FastAPI class and stores it in a variable called app.
app = FastAPI()

# Register the categories router with the main FastAPI application.
# Without include_router(), the routes defined in categories.py would
# exist in that file but would not be available through the main API.
app.include_router(categories.router)

# Register the products router with the main FastAPI application.
# This makes the product endpoints defined in products.py available
# through our API.
app.include_router(products.router)