echo 'Eliminacion de BD'
rm db.sqlite3
echo 'Eliminacion de assets'
rm -r main/assets
mkdir main/assets
echo 'Restablecimiento de BD'
python3 manage.py makemigrations
python3 manage.py migrate
