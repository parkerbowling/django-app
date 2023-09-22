# django-app

## Plan for website

### Phase 1
 - Implement bare bones of website that stores input in database tables:
    1. Expense Tracker :white_check_mark:
    2. Recipes Database :white_check_mark:

### Phase 2
 - Add Search feature for receipes :white_check_mark:
 - Add Display for a queried recipe :white_check_mark:
 - Add user authentication (still really janky needs updating eventually) :white_check_mark:
 - Start on data viz, look at section below for charts needed
 - Add automatic reoccuring expenses like rent and bills and income that are automatically added each month (django-crontab library)
 - Can the cron jobs be dynamically made (can a user add a reoccuring expense/income)

 - Style website that looks acceptable and not from 2006

 - #### Data Viz Needs
    - since I include income, show savings over expenses for that month
    - Compare across categories (comparing across different categories wouldn't make sense)
    - Month versus month comparison
    - add types of charts to choose from (bar, line graph, pie chart)
    - week versus week comparison?
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
    4. Grocery store Djikstra's algorithm - find the shortest path to buying all grocery store items

- Overall Website
    1. Improve user authentication