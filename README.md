# E-Commerce Website

Welcome to our E-Commerce website! This platform offers customers a seamless shopping experience while empowering sellers to showcase and sell their products with ease.

## Features

### For Customers:
- **User Authentication**: Customers can sign in or create accounts.
- **Product Browsing**: Browse through a diverse selection of products available on the platform.
- **Shopping Cart**: Add items to the cart and manage them before making purchases.
- **Checkout Process**: Easily complete purchases.

### For Sellers:
- **Shop Management**: Sellers can showcase and manage their products within their shops.
- **Product Listings**: Add, update, or remove products available for sale.
- **Order Fulfillment**: Manage orders and fulfill customer requests efficiently.

## Technologies Used

- **Django**: Python-based web framework used for backend development.
- **HTML/CSS and Bootstrap**: Frontend development for creating user interfaces with responsive design.
- **Python**: Backend logic and application functionalities.
- **SQLite**: Database management system for storing product and user data.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/e-commerce.git
    ```

2. Browse to the project(Which directory contains manage.py file):

    ```bash
    cd e-commerce
   

3. Run migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Start the development server:

    ```bash
    python manage.py runserver
    ```

5. Access the application in your web browser at `http://localhost:8000`.


## Creating a Superuser

To access the Django admin panel and manage the application's data, you can create a superuser account using the following steps:

1. Ensure your Django project is running. If not, start the development server:

    ```bash
    python manage.py runserver
    ```

2. Open a terminal or command prompt and navigate to your project directory.

3. Run the following command:

    ```bash
    python manage.py createsuperuser
    ```

4. You will be prompted to enter a username, email address, and password for the superuser account.

5. Once the superuser account is created successfully, you can access the Django admin panel by going to `http://localhost:8000/admin/` in your web browser.

6. Log in with the superuser credentials to access the admin panel and manage users, content, and other site functionalities.



## Usage

1. Register a new account or log in with existing credentials as a customer or seller.
2. Customers can browse products, add them to the cart, and proceed to checkout.
3. Sellers can manage their shops, add new products, and fulfill orders.


## Acknowledgments
- Learning purpose project
- Thanks to the course teacher Dr. Farhad Rabby sir who guide me.
- Special thanks to the Django and open-source community for their valuable contributions.

