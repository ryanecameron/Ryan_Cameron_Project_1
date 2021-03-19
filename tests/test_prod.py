import main
import secrets
from main import compare_school_data_with_state_data
import us_state_abrev
current_database = ("collegescorecard.sqlite")

# NOTE: This got extremely messy when trying to test my data analysis...


def test_get_data():
    # This test will check if the 100th page, or 1000th result is empty.
    results = main.get_data(
        f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,"
        f"school.state,school.name,school.city,2018.student.size,2017.student.size"
        f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
        f"2016.repayment.3_yr_repayment.overall")
    assert len(results) > 0
    return results


def create_schools_db():
    main.execute_school_db(current_database)

def create_state_db():
    main.execute_state_db(current_database)

def test_create_database():
    conn, cursor = main.open_db("test_db.sqlite")
    main.open_db("test_db.sqlite")
    cursor.execute('''SELECT name FROM sqlite_master''')
    results = cursor.fetchall()
    assert results != []


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


def test_open_workbook():
    dataframe = main.open_workbook()
    results_rows = dataframe.shape[0]
    results_cols = dataframe.shape[1]

    assert results_rows == 1187
    assert results_cols == 7



''' The function test_create_table_states() will only test that an empty table 
    has been created for the data from the excel file.
'''
def test_create_table_states():
    results = main.open_workbook()
    conn, cursor = main.open_db('test_db.sqlite')
    main.setup_state_db(cursor)
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_states(
            area_title TEXT NOT NULL ,
        occ_code TEXT NOT NULL,
        occ_title TEXT NOT NULL,
        o_group TEXT NOT NULL,
        tot_emp INTEGER,
        h_pct25 DOUBLE,
        a_pct25 DOUBLE
            );''')
    cursor.execute('''SELECT * FROM test_school''')
    result = cursor.fetchone()
    assert result == None




def test_write_to_state_db():
    conn, cursor = main.open_db('test_db.sqlite')
    dataframe = main.open_workbook()
    dataframe = dataframe.loc[dataframe['o_group'] == 'major']
    dataframe.to_sql('test_states', conn, if_exists='append', index=False)


    cursor.execute('''SELECT area_title FROM test_states''')
    result = cursor.fetchone()

    assert result == ('Alabama',)


def test_compare_students_to_jobs():
    results = main.compare_school_data_with_state_data(current_database)
    specific_state_results_students = results[0]['students']
    specific_state_results_state = results[2]

    assert results != None
    assert specific_state_results_students > 100000
    assert specific_state_results_state != "Pizza Hut"



if __name__ == '__main__':
    create_schools_db()
    create_state_db()