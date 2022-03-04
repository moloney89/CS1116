# Script Name: holidays.py
# Script Author: Jack Moloney, 120492066

import holidays
from datetime import *
from database import *
from time import strftime

# db = get_db()


# Create table
# db.execute("""
#     DROP TABLE IF EXISTS holidays;

#     CREATE TABLE holidays 
#     (
#         holiday_name TEXT NOT NULL PRIMARY KEY,
#         date TEXT NOT NULL,
#         country TEXT NOT NULL
#     );

# """)
# db.commit()

# Insert entries

irish_holidays = holidays.country_holidays("IE")

start_date = "2022-01-01"

def increase_date_by_1(current_date:str):

    current_month = current_date.strftime("%m")
    current_day = current_date.strftime("")
    thirty_days = ()

    current_day += 1

    if current_month == 2 and current_day = :
    elif current_month in thirty_days = 


# close_db()
