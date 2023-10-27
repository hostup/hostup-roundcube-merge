import mysql.connector

def merge_databases(config_db1, config_db2):
    db1_cnx = mysql.connector.connect(**config_db1)
    db2_cnx = mysql.connector.connect(**config_db2)

    db1_cursor = db1_cnx.cursor(dictionary=True)
    db2_cursor = db2_cnx.cursor(dictionary=True)

    # Merge Users, Contacts, Identities, and Collected Addresses
    user_id_map = merge_users(db1_cursor, db2_cursor, db2_cnx)
    merge_contacts(db1_cursor, db2_cursor, db2_cnx, user_id_map)
    merge_identities(db1_cursor, db2_cursor, db2_cnx, user_id_map)
    merge_collected_addresses(db1_cursor, db2_cursor, db2_cnx, user_id_map)

    # Close connections
    db1_cursor.close()
    db1_cnx.close()
    db2_cursor.close()
    db2_cnx.close()

def merge_users(db1_cursor, db2_cursor, db2_cnx):
    user_id_map = {}
    db1_cursor.execute("SELECT * FROM users")
    users = db1_cursor.fetchall()

    for user in users:
        mail_host = "mail." + user['username'].split('@')[1]
        db2_cursor.execute("SELECT user_id FROM users WHERE username = %s", (user['username'],))
        row = db2_cursor.fetchone()

        if row:
            new_user_id = row['user_id']
        else:
            db2_cursor.execute(
                "INSERT INTO users (username, mail_host, created, last_login, failed_login, failed_login_counter, language, preferences) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (user['username'], mail_host, user['created'], user['last_login'], user['failed_login'], user['failed_login_counter'], user['language'], user['preferences']))
            new_user_id = db2_cursor.lastrowid
        
        user_id_map[user['user_id']] = new_user_id
    
    db2_cnx.commit()
    return user_id_map

def merge_contacts(db1_cursor, db2_cursor, db2_cnx, user_id_map):
    db1_cursor.execute("SELECT * FROM contacts")
    contacts = db1_cursor.fetchall()

    for contact in contacts:
        new_user_id = user_id_map[contact['user_id']]
        db2_cursor.execute(
            "INSERT INTO contacts (changed, del, name, email, firstname, surname, vcard, words, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (contact['changed'], contact['del'], contact['name'], contact['email'], contact['firstname'], contact['surname'], contact['vcard'], contact['words'], new_user_id))
    
    db2_cnx.commit()

def merge_identities(db1_cursor, db2_cursor, db2_cnx, user_id_map):
    db1_cursor.execute("SELECT * FROM identities")
    identities = db1_cursor.fetchall()

    for identity in identities:
        new_user_id = user_id_map[identity['user_id']]
        db2_cursor.execute(
            "INSERT INTO identities (name, organization, email, bcc, `reply-to`, signature, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (identity['name'], identity['organization'], identity['email'], identity['bcc'], identity['reply-to'], identity['signature'], new_user_id))
    
    db2_cnx.commit()

def merge_collected_addresses(db1_cursor, db2_cursor, db2_cnx, user_id_map):
    db1_cursor.execute("SELECT * FROM collected_addresses")
    addresses = db1_cursor.fetchall()

    for address in addresses:
        new_user_id = user_id_map[address['user_id']]
        
        # Check if entry exists in db2
        db2_cursor.execute("SELECT address_id FROM collected_addresses WHERE user_id = %s AND type = %s AND email = %s",
                           (new_user_id, address['type'], address['email']))
        row = db2_cursor.fetchone()

        if not row:
            db2_cursor.execute(
                "INSERT INTO collected_addresses (changed, name, email, user_id, type) VALUES (%s, %s, %s, %s, %s)",
                (address['changed'], address['name'], address['email'], new_user_id, address['type']))
    
    db2_cnx.commit()

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

merge_databases(config_db1, config_db2)
