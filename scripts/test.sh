source venv/bin/activate
echo -e "\n #### [Info] Running Tests #### \n"
coverage run -m pytest 
echo -e "\n #### [Info] Running Type Checking #### \n"
mypy .
echo -e "\n #### [Info] Running Code Checking & Format #### \n" 
ruff check .
ruff format .
echo -e "\n #### [Info] Generating Coverage Report #### \n"
coverage html