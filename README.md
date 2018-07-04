# meal-booking-app

An application that allows customers to make food orders and helps the food vendor know what the customers want to eat.

[![Build Status](https://travis-ci.org/solnsubuga/meal-booking-app.svg?branch=master)](https://travis-ci.org/solnsubuga/meal-booking-app)
[![Maintainability](https://api.codeclimate.com/v1/badges/4f5531763259f4e6d2ae/maintainability)](https://codeclimate.com/github/solnsubuga/meal-booking-app/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/solnsubuga/meal-booking-app/badge.svg?branch=master)](https://coveralls.io/github/solnsubuga/meal-booking-app?branch=master)

## Description

meal-booking-app is a web application to be built with reactjs/redux and flask micro framework.

## Front End(UI) Designs

The front end version of the application is currently made with:

- HTML
- CSS
- Javascript

It is stored in the UI folder in the `app-ui branch` which includes the templates that capture the following.

- User sign,User login,
- A page showing current day menu and date filter to choose a specific day menu
- A page where an authenticated user can order for a meal.
- A page that allows caterers to sign up their businesses
- A page where an authenticated user can view their order history.
- A page where an admin can manage(add,delete, modify) meal options.
- A page where an admin can set menu for a specific using the meal options

- UI Designs for the front-end application are hosted on [Github-Pages](https://solnsubuga.github.io/meal-booking-app/ui/)

## Dependancies

- [python 3.6](https://www.python.org/downloads/release/python-360/)
- [flask](flask.pocoo.org/)
- [flask-Restplus](https://flask-restplus.readthedocs.io/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/)
- [flask-script]()

## Set Up

In order to run the API Application

1.  Clone this Repository to your development machine

    - Start by copying the url to this Repository
      > https://github.com/solnsubuga/meal-booking-app.git
    - Run this command in git bash to create the repo locally
      `git clone https://github.com/solnsubuga/meal-booking-app.git`

2.  Create a virtual environment in a terminal shell `virtualenv env`

3.  Activate the virtual environment but running the following command `env\scripts\activate`

4.  Install the dependencies by running the following command in a terminal shell `pip install -r requirements.txt`

5.  Run the application by running commands `python manage.py runserver`

## API End points

| EndPoint                       | Method |
| ------------------------------ | ------ |
| `/api/v1/auth/signup`          | POST   |
| `/api/v1/auth/login`           | POST   |
| `/api/v1/auth/business/signup` | POST   |
| `/api/v1/meals`                | GET    |
| `/api/v1/meals`                | POST   |
| `/api/v1/meals/<mealId>`       | DELETE |
| `/api/v1/meals/<mealId>`       | GET    |
| `/api/v1/meals/<mealId>`       | PUT    |
| `/api/v1/menu`                 | GET    |
| `/api/v1/menu`                 | POST   |
| `/api/v1/orders`               | GET    |
| `/api/v1/orders`               | POST   |
| `/api/v1/orders/<orderId>`     | GET    |
| `/api/v1/orders/<orderId>`     | PUT    |

1.  Test the endpoints using [Postman](https://www.getpostman.com/) or [Curl](https://curl.haxx.se/)

2.  To test the endpoints For example Run `python manage.py test`

## Deployment

The application is deployed on Heroku Server at and you can try it out.

> https://mealbooking-api.herokuapp.com/api/v1/#!/default

## License

The project is licensed under MIT License.
