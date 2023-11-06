<h1 align="center">
  <br>
  TST Microservice
  <br>
  <br>
</h1>

<h2 align="center">
  <br>
    Order Management API
  <br>
</h2>

## Table of Contents
- [Description of the services](#description-of-the-services)
- [API URL](#api-url)
- [API Endpoint](#api-endpoint)
- [References](#references)

## Description of the services

Order Management API enables authorized user to managing orders and product by providing a standardized way for software to exchange information with database that include creation, deletion, and modification of customer orders. I use PostgreSQL as the database and containerized using instance from Microsoft Azure.

## API URL
    
    http://20.247.139.109/docs

## API Endpoint
### Orders
#### Get All Users Orders
- GET /orders/ <br>
This endpoint retrieves all orders placed by users. It returns a list of orders, allowing clients to view the details of all orders made by various users.

#### Create Order
- POST /orders/ <br>
This endpoint allows clients to create a new order. Customer need to send the product_id and quantity in the request body to create a new order.

#### Get All Orders
- GET /orders/all <br>
This endpoint retrieves all orders in the system. It returns a list of all orders available in the database. Only admin can access this endpoint.

#### Get Order
- GET /orders/{id} <br>
This endpoint retrieves the details of a specific order identified by the {id} parameter. Clients can access information about a particular order by specifying its unique identifier in the URL.

#### Update Order
- PUT /orders/{id} <br>
This endpoint allows clients to update the details of a specific order. Clients need to send the updated order information in the request body, and the order with the specified {id} parameter will be modified accordingly. Only admin can access this endpoint.

#### Delete Order
- DELETE /orders/{id} <br>
This endpoint enables clients to delete a specific order identified by the {id} parameter. Upon successful deletion, the order will be removed from the database. Only admin can access this endpoint.

### Users
#### Create User
- POST /users/ <br>
This endpoint allows clients to create a new user. Clients need to provide user-related information (such as username, email, password, etc.) in the request body to register a new user.

### Auth
#### Login
- POST /login <br>
This endpoint handles user authentication. Clients can send login credentials (such as username and password) in the request body. If the credentials are valid, the server responds with an authentication token, allowing the client to access authorized data.

### Products
#### Get All Products
- GET /products/ <br>
This endpoint retrieves a list of all products available in the database. It provides clients with information about various products, including their names, prices, and other details.

#### Create Product
- POST /products/ <br>
This endpoint allows clients to create a new product. Clients need to provide product-related information in the request body to add a new product to the database.

#### Get Product
- GET /products/{id} <br>
This endpoint retrieves the details of a specific product identified by the {id} parameter. Clients can access information about a particular product by specifying its unique identifier in the URL.

#### Update Product
- PUT /products/{id} <br>
This endpoint allows clients to update the details of a specific product. Clients need to send the updated product information in the request body, and the product with the specified {id} parameter will be modified accordingly.

#### Delete Product
- DELETE /products/{id} <br>
This endpoint enables clients to delete a specific product identified by the {id} parameter. Upon successful deletion, the product will be removed from the database.


## References
### Libraries
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [pydantic](https://docs.pydantic.dev/latest/)
- [jose](https://python-jose.readthedocs.io/en/latest/)

## Author
Reinhart Wisely Lim (18221154) <br>
Information System and Technology <br>
Bandung Institute of Technology