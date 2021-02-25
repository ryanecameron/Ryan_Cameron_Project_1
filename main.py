from typing import Tuple
import pandas as pd
import requests
import secrets
import sqlite3
import openpyxl

# excel_file = "PATH "
excel_file = "state_M2019_dl.xlsx"
final_data = []


def get_data(url: str):
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
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS schools(
            earnings_2017 INTEGER,
            school_name TEXT NOT NULL,
            student_size_2017 INTEGER,
            student_size_2018 INTEGER,
            school_state TEXT NOT NULL,
            school_id INTEGER,
            school_city TEXT NOT NULL,
            repayment_2016 INTEGER
            );
            '''
                       )


def make_initial_schools(cursor: sqlite3.Cursor):
    for idx in range(len(final_data)):
        db_data = final_data[idx]
        cursor.execute(
            '''
            INSERT INTO schools VALUES(?,?,?,?,?,?,?,?)
            ''',
                [db_data['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
                 db_data['school.name'],
                 db_data['2017.student.size'],
                 db_data['2018.student.size'],
                 db_data['school.state'],
                 db_data['id'],
                 db_data['school.city'],
                 db_data['2016.repayment.3_yr_repayment.overall']]
            )


def open_workbook():
    cols = ['area_title', 'occ_code', 'occ_title', 'o_group', 'tot_emp', 'h_pct25', 'a_pct25']
    dataframe = pd.read_excel(excel_file, usecols=cols, engine='openpyxl')
    return dataframe


def setup_state_db(cursor: sqlite3.Cursor):
    cursor.execute(
        '''
    CREATE TABLE IF NOT EXISTS states (
        area_title TEXT NOT NULL ,
        occ_code TEXT NOT NULL,
        occ_title TEXT NOT NULL,
        o_group TEXT NOT NULL,
        tot_emp INTEGER,
        h_pct25 DOUBLE,
        a_pct25 DOUBLE
    );
    '''
    )


def make_initial_state():
    conn, cursor = open_db("collegescorecard.sqlite")
    dataframe = open_workbook()
    dataframe = dataframe.loc[dataframe['o_group'] == 'major']
    dataframe.to_sql('states', conn, if_exists='append', index=False)
    close_db(conn)


def execute_school_db():
    url = (f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,"
           f"school.state,school.name,school.city,2018.student.size,2017.student.size,"
           f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
           f"2016.repayment.3_yr_repayment.overall")
    all_data = get_data(url)
    line_counter = 1

    for school_data in all_data:
        print(line_counter, ": ", school_data)
        line_counter += 1

    conn, cursor = open_db("collegescorecard.sqlite")
    print(type(conn))
    setup_school_db(cursor)
    make_initial_schools(cursor)
    close_db(conn)


def execute_state_db():
    conn, cursor = open_db("collegescorecard.sqlite")
    setup_state_db(cursor)
    make_initial_state()
    close_db(conn)


def main():
    # workflow comment
    execute_school_db()
    execute_state_db()


if __name__ == '__main__':
    main()
