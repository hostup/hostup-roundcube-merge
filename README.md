# Roundcube Database Merge Script

This script merges data from one Roundcube database to another, focusing on the `users`, `contacts`, `collected_addresse` and `identities` tables. The primary use-case is for merging multiple roundcube installations database into a single one.

By default the script will set `mail_host` under the users table to mail.site.tld where site.tld is the domain name. It's important that you change this record to match the mail server for the user. For example to change mail host to localhost for all merged users replace the following line
`mail_host = "mail." + user['username'].split('@')[1]`
with
`mail_host = localhost`

## Prerequisites

1. Ensure you have **Python** installed (the script was tested with Python 3.12).
2. Install the `mysql-connector-python` package:
   ```bash
   pip install mysql-connector-python
   ```

## Configuration

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hostup/roundcube-merge.git
   cd roundcube-merge
   ```

2. **Set up the database configurations:** Open `merge.py` in your preferred text editor and edit the `config_db1` and `config_db2` dictionaries at the bottom of the script:

   ```python
   config_db1 = {
       'user': 'YOUR_DB1_USERNAME',
       'password': 'YOUR_DB1_PASSWORD',
       'host': 'YOUR_DB1_HOST',
       'database': 'YOUR_DB1_DATABASE_NAME',
   }

   config_db2 = {
       'user': 'YOUR_DB2_USERNAME',
       'password': 'YOUR_DB2_PASSWORD',
       'host': 'YOUR_DB2_HOST',
       'database': 'YOUR_DB2_DATABASE_NAME',
   }
   ```

   Replace the placeholders (`YOUR_DB1_USERNAME`, etc.) with your actual database configuration details.

## Running the Script

After configuring, you can run the script using:

```bash
python merge.py
```

Monitor the console output for any errors or issues.

## Warning

:warning: This script directly modifies the databases. Before using it, make sure to **take a backup** of both databases. Always test the script on a non-production or staging environment before applying it to live data.
