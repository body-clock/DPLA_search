# DPLA_search
DPLA_search is designed to take a search term from user input, use the term to search the DPLA database, and return results formatted as HTML.

# How to Run
1. Clone this repository
2. Navigate to the folder in Terminal using `cd /Users/your_name/DPLA_search`
3. Install requirements using `pip3 install -r requirements.txt`
4. Run the `dpla_search.py` script using `python3 dpla_search.py`

# Postmortem
This was an interesting little project. I've done stuff like it before, but never using this specific API. I've also never outputted data to HTML, so it was really nice to learn how simple that process really is. Since I was limited on the time I was to spend on the project, I didn't get to style it as much as I'd like to. I tried going for a Penn theme, but working with CSS and Pandas dataframe output is a bit tricky. If I had a bit more time, I would have liked to implement a simple NLP search term correction. If a user were to misspell a word, they would be returned the most likely result. Additionally, a call to the API returns 10 results at maximum. It would also be iintersting to explore a method of allowing the user to specify how many results they'd like. It's pretty cool what can be accomplished under 100 lines of Python code and some strong lbraries.


