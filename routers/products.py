# Import Optional so some query parameters can either contain a value
# or be None when the user does not provide them.
from typing import Optional

# Import APIRouter to organize the product endpoints.
# Import Query to define and validate query parameters.
# Import Path to define and validate path parameters.
# Import HTTPException so the API can return an appropriate error
# when a requested product does not exist.
from fastapi import APIRouter, Query, Path, HTTPException


# Create a router for all product-related endpoints.
# Later, main.py will register this router with the main FastAPI application.
router = APIRouter()

# This list acts as our temporary product database.
# Each item in the list is a Python dictionary representing one product.
# We are using an in-memory list because a database is not required for this task.
PRODUCTS = [
    {
        "id": 1,
        "name": "Wireless Ergonomic Mouse",
        "category": "electronics",
        "price": 29.99,
    },
    {
        "id": 2,
        "name": "Mechanical Keyboard",
        "category": "electronics",
        "price": 89.99,
    },
    {
        "id": 3,
        "name": "Relaxed Fit Linen Shirt",
        "category": "apparel",
        "price": 45.00,
    },
    {
        "id": 4,
        "name": "Running Shoes",
        "category": "apparel",
        "price": 115.50,
    },
    {
        "id": 5,
        "name": "Stainless Steel Water Bottle",
        "category": "home",
        "price": 18.25,
    },
]

# GET /products route decorator & function
# Define a GET endpoint at the "/products" URL path.
# This endpoint will return products and will later support optional
# filtering by category and price, as well as pagination.
# The metadata below controls how the endpoint appears in Swagger UI.
@router.get(
    "/products",

    # Group this endpoint under the "Products" section in Swagger UI.
    tags=["Products"],

    # Provide a short title for the endpoint in the API documentation.
    summary="Get products",

    # Explain the main purpose of the endpoint.
    description="Returns products with optional filtering and pagination.",

    # Describe what a successful response from this endpoint contains.
    response_description="A list of products",
)
def get_products(
    category: Optional[str] = Query(
        None,
        description="Filter products by category (case-insensitive).",
    ),
    min_price: Optional[float] = Query(
        None,
        ge=0,
        description="Return products with a price greater than or equal to this value.",
    ),
    max_price: Optional[float] = Query(
        None,
        ge=0,
        description="Return products with a price less than or equal to this value.",
    ),
    limit: int = Query(
        10,
        gt=0,
        description="Maximum number of products to return.",
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Number of products to skip before returning results.",
    ),
):
    """
    Return products from the product catalog.

    Products can be filtered by category, minimum price, and maximum price.
    The results can also be paginated using the limit and skip parameters.

    Args:
        category (str, optional): The category used to filter products.
        min_price (float, optional): The minimum product price to include.
        max_price (float, optional): The maximum product price to include.
        limit (int): The maximum number of products to return.
        skip (int): The number of products to skip before returning results.

    Returns:
        list: A list of products that match the requested filters
        and pagination settings.
    """

    # Start with all products from the PRODUCTS dataset.
    # We create a copy so that filtering does not modify the original list.
    filtered_products = PRODUCTS.copy()

    # Check whether the user provided a category query parameter.
    # If category is None, no category filtering should be performed.
    if category is not None:

        # Keep only the products whose category matches the requested category.
        # .lower() makes the comparison case-insensitive, so values such as
        # "Electronics", "ELECTRONICS", and "electronics" are treated the same.
        filtered_products = [
            product
            for product in filtered_products
            if product["category"].lower() == category.lower()
        ]

    # Check whether the user provided a minimum price.
    # If min_price is None, no minimum-price filtering is performed.
    if min_price is not None:

        # Keep only products whose price is greater than or equal
        # to the minimum price requested by the user.
        filtered_products = [
            product
            for product in filtered_products
            if product["price"] >= min_price
        ]

    # Check whether the user provided a maximum price.
    # If max_price is None, no maximum-price filtering is performed.
    if max_price is not None:

        # Keep only products whose price is less than or equal
        # to the maximum price requested by the user.
        filtered_products = [
            product
            for product in filtered_products
            if product["price"] <= max_price
        ]

    # Apply pagination after all filtering is complete.
    # "skip" determines where the returned results should start,
    # and "limit" determines the maximum number of products to return.
    paginated_products = filtered_products[skip: skip + limit]

    # Return the final filtered and paginated list of products.
    # FastAPI will automatically convert the Python list into JSON.
    return paginated_products

# Define a GET endpoint that retrieves one product by its ID.
# The value inside {product_id} is a path parameter, which FastAPI
# will take from the URL and pass to the function below.
# The metadata controls how this endpoint appears in Swagger UI.
@router.get(
    "/products/{product_id}",

    # Group this endpoint under the "Products" section in Swagger UI.
    tags=["Products"],

    # Provide a short title for the endpoint in the API documentation.
    summary="Get product by ID",

    # Explain the purpose of this endpoint.
    description="Returns a single product that matches the requested product ID.",

    # Describe what a successful response contains.
    response_description="The requested product",
)
def get_product(
    product_id: int = Path(
        ...,
        gt=0,
        description="The ID of the product to retrieve.",
    ),
):
    """
    Return a single product that matches the requested product ID.

    Args:
        product_id (int): The unique ID of the product to retrieve.

    Returns:
        dict: The product that matches the requested ID.

    Raises:
        HTTPException: A 404 error if no product exists with the requested ID.
    """

    # Loop through every product in the PRODUCTS dataset.
    # Each product is checked to see whether its ID matches
    # the product_id provided in the URL.
    for product in PRODUCTS:

        # Compare the current product's ID with the requested product ID.
        # If they match, we found the product the user requested.
        if product["id"] == product_id:

            # Return the matching product immediately.
            # Once return runs, the function stops and does not continue
            # checking the remaining products.
            return product

    # If the loop finishes without returning a product, then no product
    # in the PRODUCTS dataset has the requested ID.
    # Raise a 404 Not Found error with the exact message required
    # by the assignment.
    raise HTTPException(
        status_code=404,
        detail="Product not found",
    )