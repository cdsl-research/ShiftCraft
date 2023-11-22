import mysql.connector

# # Kubernetes上のSQLサービスの情報
# k8s_ns = "nissy"
# k8s_svc = "nissy-sql"

# # Kubernetesクラスタ内のSQLサービスに接続するための情報を取得
# # サービスのClusterIPを使用する
# sql_service_cluster_ip = f"{k8s_svc}.{k8s_ns}.svc.cluster.local"
# print(sql_service_cluster_ip)

# MySQLデータベースへの接続設定
db_config = {
    'host': 'c0a21099-local1',
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
    query = 'SELECT id, cleaned_uri, post_title, post_date FROM wp_nissy_kekka_new;'
    cursor.execute(query)

    # 結果を取得
    results = cursor.fetchall()

    # 結果を表示
    for row in results:
        id_value = row[0]  # idは結果の最初の列にあると仮定
        cleaned_uri_value = row[1]  # cleaned_uriは結果の2番目の列にあると仮定

        ids.append(id_value)
        cleaned_uris.append(cleaned_uri_value)

        # print(row)
        print(row[0], row[1])
        # print(row[1])

    # idsとcleaned_urisを使って何かをすることができます

finally:
    # 接続を閉じる
    conn.close()
