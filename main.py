import requests
import secrets


def get_data(url: str):
    final_data = []
    # There are 3203 pages of data.
    # For loop iterates 32 times, printing 100 pages per iteration.
    get_pages = f"{url}&api_key={secrets.api_key}"
    get_response = requests.get(get_pages)

    for pages in range(32):
        final_url = f"{url}&api_key={secrets.api_key}&per_page=100, page={pages}"
        response = requests.get(final_url)
        if response.status_code != 200:
            print(response.text)
            return []
        json_data = response.json()
        page_data = json_data["results"]
        final_data.extend(page_data)
    return final_data


def main():
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3&fields=id,school.state,school.name,school.city,2018.student.size,2017.student.size,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,2016.repayment.3_yr_repayment.overall"
    all_data = get_data(url)
    for school_data in all_data:
        print(school_data)



if __name__ == '__main__':
    main()
