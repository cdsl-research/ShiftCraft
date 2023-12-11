# 評価実験用 (全数検査用)
import mysql.connector

print("全数検査-WordPressDB-")
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


