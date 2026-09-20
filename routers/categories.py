# Import APIRouter from FastAPI.
# APIRouter lets us organize related API endpoints in a separate file
# instead of putting every endpoint inside main.py.
from fastapi import APIRouter

# Import the shared product dataset from products.py.
# This allows the categories endpoint to find the categories that
# actually exist in our product data instead of hard-coding them.
from .products import PRODUCTS


# Create a router for all category-related endpoints.
# Later, main.py will connect this router to the main FastAPI application.
router = APIRouter()


# Define a GET endpoint at the "/categories" URL path.
# @router.get() connects the function directly below it to this endpoint.
# The additional metadata controls how the endpoint appears in FastAPI's
# automatically generated Swagger documentation at /docs.
@router.get(
    "/categories",

    # Group this endpoint under the "Categories" section in Swagger UI.
    tags=["Categories"],

    # Provide a short title for the endpoint in the API documentation.
    summary="Get all product categories",

    # Explain in more detail what this endpoint does.
    description="Returns a list of distinct product categories.",

    # Describe what a successful response from this endpoint contains.
    response_description="A list of available product categories",
)
def get_categories():
    """
    Return all distinct product categories.

    The categories are collected from the shared PRODUCTS dataset so
    that each category appears only once in the response.

    Returns:
        list: A list containing the unique product category names.
    """

    # Create an empty list that will store each unique category.
    # We use a list instead of a set so the categories stay in the same
    # order in which they first appear in the PRODUCTS dataset.
    categories = []

    # Loop through every product in the PRODUCTS list one at a time.
    for product in PRODUCTS:

        # Get the category value from the current product dictionary.
        category = product["category"]

        # Only add the category if it has not already been added.
        # This prevents duplicate categories from appearing in the response.
        if category not in categories:
            categories.append(category)

    # Return the completed list of unique categories.
    # FastAPI will automatically convert this Python list into JSON.
    return categories