# django-app

## How to get started with website

    0. Ensure you are in a python virtual environment
    1. Install python libraries from requirements.txt.
    2. Download PostgreSQL for system.
    3. Create .env file and add SECRETKEY, USER, and PASSWORD as it appears in settings.py file.
    4. Make sure that USER and PASSWORD matches with the user and password you create for the PostgreSQL database.
    5. Also make sure that settings.py NAME for the database matches what the name of the database you created in PostgreSQL.
    6. run python3 manage.py runserver to run the server.

## Plan for website

### Phase 1
 - Implement bare bones of website that stores input in database tables:
    1. Expense Tracker :white_check_mark:
    2. Recipes Database :white_check_mark:

### Phase 2
 - Add Search feature for receipes :white_check_mark:
 - Add Display for a queried recipe :white_check_mark:
 - Add user authentication (still really janky needs updating eventually) :white_check_mark:
 - Start on data viz, look at section below for charts needed :white_check_mark:
 - Fix UpdateView :white_check_mark:
 - Order ingredient properly for recipe database :white_check_mark:
 - Add filters for recipes in search

 - Style website that looks acceptable and not from 2006

 - #### Data Viz Needs
    - since I include income, show savings over expenses for that month :white_check_mark:
    - Month versus month comparison :white_check_mark:
    - add types of charts to choose from (bar, line graph, pie chart)
    - Year over Year comparison (eventually) 
    - Add a credit card percentage calculator -> based on what cashback you get for each card, calculate the average percent return over all expenses

#### Feature Wishlist

- Expense Tracker
    1. OCR for receipts instead of manually entering it
    2. Add a budget feature that gives goals on what you want to spend that month
    3. Wrap the database around an A.I. (LLM) that can compute any data viz you ask it for

- Receipes Database
    1. Select a recipe (or many) and compile a grocery list from those recipe(s) selected
    2. Have a URL input that has a recipe on it and scraps the recipe off of it and stores it into the database 
    3. OCR for recipes instead of manual imput
    5. It would be really cool to build this dynamically, so when a user first launches the website, they can choose what categories they want, and also add or remove categories as needed
    6. Be able to have a GUI that can insert data into the database without having to boot up the server and code all the time.

- Overall Website
    1. Improve user authentication

## Implement ideas for website

    1. What if there was a website that could find the fastest path in a grocery story to find all your items?
        - User would build grocery list for a specific grocery store and a shortest path algo would generate
        - User would also be able to search for a specific item and see its location in the store
    2. What if there was a way to find the cheapest items in a grocery store to build the cheapest grocery list?
        - User would choose a location (or mile range) to set the searchable grocery stores
        - User would add items to a grocery list and filter to how many grocery stores they want to build the cheapest list from
            - if one store, build the cheapest list from one store in the area
            - if more than one store, build a list from multiple stores to get the cheapest list