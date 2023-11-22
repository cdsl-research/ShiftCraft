import pymysql

# Kubernetes上のSQLサービスの情報
k8s_ns = "nissy"
k8s_svc = "nissy-sql"

# Kubernetesクラスタ内のSQLサービスに接続するための情報を取得
sql_service_cluster_ip = f"{k8s_svc}.{k8s_ns}"

# MySQLデータベースへの接続設定
db_config = {
    'host': 'c0a21099-master.a910.tak-cslab.org',
    'port': 30200,  # お使いのSQLサービスのポートに置き換えてください
    'user': 'cdsl',
    'password': 'cdsl2023',
    'database': 'wordpress',
}

# MySQLデータベースに接続
conn = pymysql.connect(**db_config)

try:
    # カーソルを取得
    with conn.cursor() as cursor:

        # SQLクエリを実行
        query = 'SELECT post_date, cleaned_uri, total_count FROM wp_nissy_kekka_new;'
        query2 = 'select * from wp_nissy_counts;'
        cursor.execute(query)
        cursor.execute(query2)

        # 結果を取得
        results = cursor.fetchall()

        # 結果を表示
        for row in results:
            print(row)

finally:
    # 接続を閉じる
    conn.close()
