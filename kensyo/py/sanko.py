import mysql.connector as mydb

# コネクション
conn = mydb.connect (
    host = '192.168.100.230',
    port = 3306,
    user = 'cdsl',
    password = 'cdsl2023',
    database = 'wordpress',
    auth_plugin = 'mysql_native_password',
)

# コネクション切れたときに再接続する.
conn.ping(reconnect=True)

# print("DBの接続状態" + conn.is_connected())

# DB操作用にカーソル作成
cur = conn.cursor()

table = 'wp_nissy_kekka'
cur.execute("DROP TABLE IF EXISTS `%s`;", table)

cur.execute (
    """
    CREATE TABLE IF NOT EXISTS wp_nissy_posts (
    post_title VARCHAR(255),
    post_name VARCHAR(255),
    guid VARCHAR(255),
    post_status VARCHAR(255)
    ); 
    """,table
)

# DB操作が終わったらカーソル閉じる.
cur.close()
conn.close()
