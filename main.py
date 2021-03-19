from typing import Tuple, List, Dict
import pandas as pd
import requests
import secrets
import sqlite3
import openpyxl
import sys
import PySide2.QtWidgets
from PySide2.QtWidgets import QApplication
import window
import us_state_abrev
import main_window_stacked






# excel_file = "PATH "
excel_file = "state_M2019_dl.xlsx"
final_data = []


def get_data(url: str):
    final_url = f"{url}&api_key={secrets.api_key}"
    response = requests.get(final_url)
    json_data = response.json()
    total_pages = json_data['metadata']['total']
    per_page = json_data['metadata']['per_page']
    pages_to_iterate = (total_pages//per_page) + 1

    for page in range(pages_to_iterate):
        current_url = f"{url}&api_key={secrets.api_key}&page={page}"
        response = requests.get(current_url)
        if response.status_code != 200:
            print(response.text)
            return []
        current_page_json = response.json()
        page_data = current_page_json["results"]
        final_data.extend(page_data)
        page += 1
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
            repayment_2016 INTEGER,
            repayment_cohort_2016 DOUBLE 
            );
            '''
                       )


def make_initial_schools(cursor: sqlite3.Cursor):
    for idx in range(len(final_data)):
        db_data = final_data[idx]
        cursor.execute(
            '''
            INSERT INTO schools VALUES(?,?,?,?,?,?,?,?,?)
            ''',
                [db_data['2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line'],
                 db_data['school.name'],
                 db_data['2017.student.size'],
                 db_data['2018.student.size'],
                 db_data['school.state'],
                 db_data['id'],
                 db_data['school.city'],
                 db_data['2016.repayment.3_yr_repayment.overall'],
                 db_data['2016.repayment.repayment_cohort.3_year_declining_balance']]
            )


def open_workbook():
    cols = ['area_title', 'occ_code', 'occ_title', 'o_group', 'tot_emp', 'h_pct25', 'a_pct25']
    dataframe = pd.read_excel(excel_file, usecols=cols, engine='openpyxl')
    dataframe = dataframe.loc[dataframe['o_group'] == 'major']
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

    dataframe.to_sql('states', conn, if_exists='append', index=False)
    close_db(conn)


def execute_school_db():
    url = (f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,"
           f"school.state,school.name,school.city,2018.student.size,2017.student.size,"
           f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
           f"2016.repayment.3_yr_repayment.overall,2016.repayment.repayment_cohort.3_year_declining_balance")
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


def data_frame_to_list(dataframe):
    dict_keys = ['area_title', 'occ_code', 'occ_title', 'o_group', 'tot_emp', 'h_pct25', 'a_pct25']
    dict_list = []
    data_list = dataframe.values.tolist()
    for item in data_list:
        dict_item = dict(zip(dict_keys, item))
        dict_list.append(dict_item)

    return dict_list

def compare_school_data_with_state_data():
    comparison = []
    states_list = us_state_abrev.list_of_state_abbrev
    for states in states_list:
        jobs_dict = get_jobs_in_a_state(states)
        students_dict = get_college_students_in_a_state(states)
        jobs_dict.update(students_dict)
        jobs_dict["More Jobs than Students"] = round((jobs_dict['jobs'] / jobs_dict['students']),2)
        comparison.append(jobs_dict)
    return comparison


def get_college_students_in_a_state(state):
    students_in_state = 0
    state = "'" + state + "'"
    conn, cursor = open_db("collegescorecard.sqlite")

    cursor.execute(f'''SELECT student_size_2018
                        FROM schools
                        WHERE school_state = {state}''')
    school_state = cursor.fetchall()

    for data in school_state:
        num = []
        data = str(data)
        for char in data:
            if char.isdigit():
                num.append(char)
            else:
                continue

        if num:
            students_in_state = students_in_state + int(''.join(num))
    state = state.replace('"', '')
    final_students_in_state = {'state': state, "students": int(students_in_state//4), "More Jobs than Students": 0 }
    return final_students_in_state


def get_jobs_in_a_state(state):
    state = state
    num_jobs = []
    jobs_in_state = 0
    final_jobs_in_state = {}
    onn, cursor = open_db("collegescorecard.sqlite")
    abbrev_of_state = us_state_abrev.abbrev_us_state[state]
    abbrev_of_state = "'" + abbrev_of_state + "'"

    cursor.execute(f'''SELECT tot_emp,occ_code
                            FROM states
                            WHERE area_title = {abbrev_of_state}''')

    jobs_in_state = cursor.fetchall()
    for jobs in jobs_in_state:
        job_digits = jobs[1]
        if int(job_digits[0]) == 3 or int(job_digits[0]) == 4:
            continue
        else:
            jobs_data = jobs[0]
            num_jobs.append(jobs_data)
    jobs_in_state = (sum(num_jobs))
    state = ("'" + state + "'")
    final_jobs_in_state = {'state': state, "jobs": int(jobs_in_state), "More Jobs than Students": 0}
    return final_jobs_in_state


def display_data():
    '''app = PySide2.QtWidgets.QApplication(sys.argv)
    win = visualizer_window.Visualizer_window(data)
    sys.exit(app.exec_())'''

    app = PySide2.QtWidgets.QApplication(sys.argv)
    win = main_window_stacked.MainWindow()
    sys.exit(app.exec_())





def main():
    # workflow comment
    #execute_school_db()
    #execute_state_db()

    #data = compare_school_data_with_state_data()
    #print(data)
    #display_data(data)
    #test_gui(data)
    #print(get_college_students_in_a_state('MA'))
    #print(get_jobs_in_a_state('MA'))
    #print(compare_school_data_with_state_data())
    main_window_stacked.main()

if __name__ == '__main__':
    main()
