# Commands

# VENV

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt


# Scripts

## Local DB Creation + Seeding

python3 scripts/local_db_create_db.py

python3 scripts/local_db_connect.py

python3 scripts/local_db_create_schema.py

python3 scripts/local_db_seed_data.py

python3 scripts/local_db_test_queries.py


## Local DB to Spreadsheet Export

python scripts/local_export_mysql_to_excel.py
