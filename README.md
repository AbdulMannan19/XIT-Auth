python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python.exe -m pip install --upgrade pip
python db_test.py

git status
git add .
git config user.email "abdulmannan34695@gmail.com"
git config user.name "AbdulMannan19"
git commit -m "quick commit"
git push