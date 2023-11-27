import mysql.connector

print()
print("Started SQL Connection.")
print()

# MySQLデータベースへの接続設定
db_config = {
    'host': 'c0a21099-local1.a910.tak-cslab.org',
    'port': 3306,
    'user': 'cdsl',
    'password': 'cdsl2023',
    'database': 'wordpress',
    'auth_plugin': 'mysql_native_password',
}

# MySQLデータベースに接続
conn = mysql.connector.connect(**db_config)

conn.ping(reconnect=True)
print(conn.is_connected())

# カーソルを取得
cursor = conn.cursor()

# WordPressのテーブルを削除
tables_to_drop = ['wp_nissy_counts', 'wp_nissy_kekka', 'wp_nissy_posts']

for table in tables_to_drop:
    query = f"DROP TABLE IF EXISTS {table};"
    cursor.execute(query)
    print(f"テーブル {table} を削除しました.")

# コミットして接続を閉じる
conn.commit()
conn.close()

print()
print("Closed SQL Connection.")
