# Ryan_Cameron_Project_1
# by Ryan Cameron
# This program pulls data from "https://api.data.gov/ed/collegescorecard", and filters the results based on assigned fields.
# This program does not write to a .txt file, and only prints the results in the terminal.
# The results are added to a database named 'collegescorecard.sqlite.
# The database has only one table name 'schools' and contains data based on the assigned fields('school.state', 'school.city', etc.)
# As of right now the only issue I am having is within the .github/Workflows directory.
# I am getting the following error:
''' ./secrets.py:1:13: E999 SyntaxError: invalid syntax
  api_key = "***"
              ^
  1     E999 SyntaxError: invalid syntax
  1
  Error: Process completed with exit code 1.
'''
