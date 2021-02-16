import requests
import sqlite3
from typing import Tuple
import secrets


def get_data(url: str):
    final_data = []
    # There are 3203 pages of data.
    # For loop iterates 161 times, printing 20 pages per iteration and 3 pages
    # for the final iteration.
    for pages in range(161):
        final_url = f"{url}&api_key={secrets.api_key}&page={pages}"
        response = requests.get(final_url)
        if response.status_code != 200:
            print(response.text)
            return []
        json_data = response.json()
        page_data = json_data["results"]
        final_data.extend(page_data)
    return final_data

def open_db(filename: str) ->Tuple[sqlite3.Connection,sqlite3.Cursor]:
    db_connection =sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor

def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()

def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS schools(
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gpa REAL DEFAULT 0,
        credits INTEGER DEFAULT 0
        );''')







def main():
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,school.state,school.name,school.city,2018.student.size,2017.student.size,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall"
    all_data = get_data(url)
    line_counter = 1
    # For loop returns results by line, with line number
    for school_data in all_data:
        print(line_counter, ": ", school_data)
        line_counter += 1

    conn, cursor = open_db("collegescorecard.sqlite")
    print(type(conn))
    setup_db(cursor)
    close_db(conn)





if __name__ == '__main__':
    main()
