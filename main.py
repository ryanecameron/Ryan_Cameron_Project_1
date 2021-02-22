import requests
import sqlite3
from typing import Tuple
import secrets

final_data = []


def get_data(url: str):
    # final_data = []
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


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


def setup_school_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS schools(
        earnings_2017 INTEGER,
        school_name TEXT NOT NULL,
        student_size_2017 INTEGER,
        student_size_2018 INTEGER,
        school_state TEXT NOT NULL,
        school_id INTEGER,
        school_city TEXT NOT NULL,
        repayment_2016 INTEGER
        );''')
    
def setup_state_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS states(
    state TEXT,
    occupation TEXT,
    total_employment INTEGER,
    25th_percentile_salary INTEGER,
    occupation_code TEXT
    );''')



def make_initial_schools(cursor: sqlite3.Cursor):
    for i in range(len(final_data)):
        db_data = final_data[i]
        cursor.execute('''INSERT INTO schools VALUES(?,?,?,?,?,?,?,?)''',
                       [db_data['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
                        db_data['school.name'],
                        db_data['2017.student.size'],
                        db_data['2018.student.size'],
                        db_data['school.state'],
                        db_data['id'],
                        db_data['school.city'],
                        db_data['2016.repayment.3_yr_repayment.overall']]
                       )


def main():
    url = (f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,"
           f"school.state,school.name,school.city,2018.student.size,2017.student.size,"
           f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
           f"2016.repayment.3_yr_repayment.overall")
    all_data = get_data(url)
    line_counter = 1
    # For loop returns results by line, with line number
    for school_data in all_data:
        print(line_counter, ": ", school_data)
        line_counter += 1

    conn, cursor = open_db("collegescorecard.sqlite")
    print(type(conn))
    setup_school_db(cursor)
    make_initial_schools(cursor)
    close_db(conn)


if __name__ == '__main__':
    main()
