import main
import secrets
import pandas as pd
import pytest

def test_get_data():
    # This test will check if the 100th page, or 1000th result is empty.
    results = main.get_data(
        f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,"
        f"school.state,school.name,school.city,2018.student.size,2017.student.size,"
        f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
        f"2016.repayment.3_yr_repayment.overall&api_key={secrets.api_key}&page={100}")
    assert len(results) > 0


def test_create_empty_database():
    conn, cursor = main.open_db("test_db.sqlite")
    main.open_db("test_db.sqlite")
    cursor.execute('''SELECT name FROM sqlite_master''')
    results = cursor.fetchall()
    assert results == []


def test_schools_table_create():
    results = main.get_data(
        f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields="
        f"school.name&api_key={secrets.api_key}")
    conn, cursor = main.open_db("test_db.sqlite")
    main.setup_school_db(cursor)
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_school(
        test TEXT
        );''')
    cursor.execute('''INSERT INTO test_school VALUES(?)''', [results[1000]['school.name']])
    cursor.execute('''SELECT * FROM test_school''')
    result = cursor.fetchone()
    assert result == ('Olympic College',)


def test_work_book():
    dataframe = main.open_workbook()
    results = dataframe.empty

    assert results == False


def create_test_excel():
    dataframe = main.open_workbook()
    writer = pd.ExcelWriter('test_excel.xlsx', engine='xlsxwriter')
    cols = ['area_title', 'tot_emp']
    test_excel = dataframe.to_excel(writer, columns=cols)
    return test_excel


def test_create_table():
    results = create_test_excel()

    assert results == None
