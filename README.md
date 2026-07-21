# Smart Food Optimization and Waste Reduction System (Backend).
## Overview.
This repository contains the backend implementation of the Smart Food Optimization and Waste Reduction System.
The backend is responsible for user authentication, food inventory management, recipe retrieval, dashboard statistics, expiry alerts, and communication with the MySQL database through RESTful APIs.
The application was developed using **Django** and **Django REST Framework**.

## Project Objectives.
The backend provides secure and reliable services that enable users to:
* Register accounts.
* Authenticate securely using JWT.
* Store food inventory.
* Retrieve food records.
* Generate dashboard statistics.
* Receive expiry alerts.
* Access meal suggestions.
* Manage user profiles.
  
## Technologies Used.
### Programming Language.
* Python.
  
### Framework.
* Django.
  
### REST API.
* Django REST Framework.
  
### Authentication.
* JSON Web Tokens (JWT).
  
### Database.
* MySQL (Railway).
  
### Deployment.
* Render.
  
## Project Structure.
backend/

├── backend/
├── foodsystem/
│   ├── migrations/
│   ├── management/
│   ├── serializers.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── manage.py
├── requirements.txt
└── README.md

## API Features.
### Authentication.
* User Registration.
* User Login.
* JWT Token Generation.
* Password Reset.
  
### Food Inventory.
* Add Food.
* Retrieve Food Items.
* Update Food Items.
* Delete Food Items.

### Dashboard.
* Total food items.
* Expiring food count.
* Expired food count.

### Expiry Alerts.
* Food nearing expiry.
* Expired food.

### Recipes.
* Retrieve recipes.
* Match recipes with available ingredients.

### User Profile.
* View profile.
* Update profile.

## Main API Endpoints.

| Endpoint             | Method | Description         |
| -------------------- | ------ | ------------------- |
| /api/register/       | POST   | Register user       |
| /api/login/          | POST   | User login          |
| /api/fooditems/      | GET    | Retrieve food items |
| /api/fooditems/      | POST   | Add food item       |
| /api/fooditems/{id}/ | PUT    | Update food item    |
| /api/fooditems/{id}/ | DELETE | Delete food item    |
| /api/dashboard/      | GET    | Dashboard summary   |
| /api/alerts/         | GET    | Expiry alerts       |
| /api/recipes/        | GET    | Retrieve recipes    |
| /api/profile/        | GET    | User profile        |
| /api/profile/        | PUT    | Update profile      |

## Installation.
Clone the repository.
https://github.com/Gloriajebet/smart-food-backend/.git
Navigate into the project.
cd backend
Install dependencies.
pip install -r requirements.txt
Apply migrations.
python manage.py migrate
Run the development server
python manage.py runserver
The API will be available at
http://127.0.0.1:8000

## Environment Variables.
Configure the following environment variables before running the application:
* MYSQLDATABASE
* MYSQLUSER
* MYSQLPASSWORD
* MYSQLHOST
* MYSQLPORT
Email configuration:
* EMAIL_HOST_USER
* EMAIL_HOST_PASSWORD

## Deployment.
The backend is deployed on **Render**.

Live API.
https://smart-food-dyp3.onrender.com

## Frontend Repository.
The frontend source code is available at:
https://github.com/Gloriajebet/smart-food-frontend

## Database.
The application uses a MySQL database hosted on **Railway**.

The backend stores:
* User Accounts.
* Food Inventory.
* Recipes.
* User Profiles.

## Security.
The system uses:

* JWT Authentication.
* Protected API Endpoints.
* Password Hashing.
* User-specific data isolation.

## Author.
**Gloria Masit**
Bachelor of Software Engineering.
Senior Project.

## License.
This project was developed for academic purposes as part of a Bachelor of Science in Software Engineering final-year project.
