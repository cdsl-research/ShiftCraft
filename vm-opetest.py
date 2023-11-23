import mysql.connector

# Kubernetes上のSQLサービスの情報
k8s_ns = "nissy"
k8s_svc = "nissy-sql"

# Kubernetesクラスタ内のSQLサービスに接続するための情報を取得
# サービスのClusterIPを使用する
sql_service_cluster_ip = f"{k8s_svc}.{k8s_ns}.svc.cluster.local"
print(sql_service_cluster_ip)

# MySQLデータベースへの接続設定
db_config = {
    'host': 'c0a21099-local1.a910.tak-cslab.org',
    'port': 3306,  # お使いのSQLサービスのポートに置き換えてください
    'user': 'cdsl',
    'password': 'cdsl2023',
    'database': 'wordpress',
    'auth_plugin': 'mysql_native_password',
}

# MySQLデータベースに接続
conn = mysql.connector.connect(**db_config)

# idとcleaned_uriを保存するためのリスト
ids = []
cleaned_uris = []

try:
    # カーソルを取得
    cursor = conn.cursor()

    # SQLクエリを実行
    query = '''
            CREATE TABLE IF NOT EXISTS wp_nissy_posts (
                post_title VARCHAR(255),
                post_name VARCHAR(255),
                guid VARCHAR(255),
                post_status VARCHAR(255)
            );

            INSERT INTO wp_nissy_posts (post_title, post_name, guid, post_status)
            SELECT post_title, post_name, guid, post_status
            FROM wp_posts
            WHERE post_status = 'publish';
            '''
    
    # query2 = 'SELECT * FROM wp_nissy_posts;' 

    cursor.execute(query)
    # cursor.execute(query2)

    results = cursor.fetchall()

    # 結果を表示（INSERT文の実行結果）
    print(f"Inserted {cursor.rowcount} rows.")

    for row in results:
        print(row)

    # idsとcleaned_urisを使って何かをすることができます

finally:
    # 接続を閉じる
    conn.close()