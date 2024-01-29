# django-app

## How to get started with website

    0. Ensure you are in a python virtual environment
    1. Install python libraries from requirements.txt.
    2. Download PostgreSQL for system.
    3. Create .env file and add SECRETKEY, USER, and PASSWORD as it appears in settings.py file.
    4. Make sure that USER and PASSWORD matches with the user and password you create for the 
       PostgreSQL database.
    5. Also make sure that settings.py NAME for the database matches what the name of the 
       database you created in PostgreSQL.
    6. You will probably need to run `python3 manage.py makemigrations` and/or `python3 manage.py migrate` to make sure the server matches the code
        - If you are getting an error that "expenses..." doesn't exist, comment out the helper.py file and rerun the migrate commands
    7. run python3 manage.py runserver to run the server, make sure the postgres server is also running

## Plan For Website

### Phase 3
 - Fix the mouse-over part on the pie chart. Doesn't need to say "Expenses: $" only the dollar amount
 - Add "Sum or Combine" button on the comparison chart, where you can click it and instead of comparing the months, it adds them together to see total amount saved over that span
 - Add a budget feature so a user can create a dynamic monthly budget and compare it with expenses for past and current month
 - Can we have the parts of the chart be clickable? Click a section of the chart and it pulls up those expenses for that. [Check this out](https://stackoverflow.com/questions/20964443/highcharts-making-a-point-clickable)
 - Web scrape: user enters a URL of a recipe and it automatically gets scraped off and inserted into the database
 - Fix Update recipe date bug
 - Style website that looks acceptable and not from 2006
 - Try to really clean up the code (if possible) and think about optimization

### Phase 2
 - ~~Add Search feature for receipes~~ :white_check_mark:
 - ~~Add Display for a queried recipe~~ :white_check_mark:
 - ~~Add user authentication (still really janky needs updating eventually)~~ :white_check_mark:
 - ~~Start on data viz, look at section below for charts needed~~ :white_check_mark:
 - ~~Fix UpdateView in recipes~~ :white_check_mark:
 - ~~Order ingredient properly for recipe database~~ :white_check_mark:
 - ~~Add filters for recipes in search~~ :white_check_mark:
 - ~~Make sure instructions are also ordered vertically like ingredients~~ :white_check_mark:

### Phase 1
 - Implement bare bones of website that stores input in database tables:
    1. ~~Expense Tracker~~ :white_check_mark:
    2. ~~Recipes Database~~ :white_check_mark:

#### Feature Wishlist

- Expense Tracker
    1. OCR for receipts instead of manually entering it
    2. Add a budget feature that gives goals on what you want to spend that month
    3. Wrap the database around an A.I. (LLM) that can compute any data viz you ask it for
    4. *It would be really cool to build this dynamically, so when a user first launches the website, they can choose what categories they want, and also add or remove categories as needed (This would be more like an app that can save data)*
    5. "ChartGPT" - build or connect and LLM that allows you to ask it any question about your data and enable it to give you a visualization about it.

- Receipes Database
    1. Select a recipe (or many) and compile a grocery list from those recipe(s) selected
    2. Have a URL input that has a recipe on it and scraps the recipe off of it and stores it into the database 
    3. OCR for recipes instead of manual imput

- Overall Website
    1. Improve user authentication
    2. Be able to have a GUI that can insert data into the database without having to boot up the server and code all the time.

### Random ideas for website

    1. What if there was a website that could find the fastest path in a grocery story to find all your items?
        - User would build grocery list for a specific grocery store and a shortest path algo would generate
        - User would also be able to search for a specific item and see its location in the store
    2. What if there was a way to find the cheapest items in a grocery store to build the cheapest grocery list?
        - User would choose a location (or mile range) to set the searchable grocery stores
        - User would add items to a grocery list and filter to how many grocery stores they want to build the cheapest list from
            - if one store, build the cheapest list from one store in the area
            - if more than one store, build a list from multiple stores to get the cheapest list