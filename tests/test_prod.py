import main
import secrets

"""TODO: -Retrieve data from web"""


def test_get_data():

    results = main.get_data(
        f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,"
        f"school.state,school.name,school.city,2018.student.size,2017.student.size,"
        f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
        f"2016.repayment.3_yr_repayment.overall&api_key={secrets.api_key}&page={100}")
    assert len(results) > 0


"""TODO:    -Create new empty database
            -Run table creation function/method
            -Run save data to database method
            -Check to see that database contains test university"""

# def test_database
