import mysql.connector

# Kubernetes上のSQLサービスの情報
k8s_ns = "nissy"
k8s_svc = "nissy-sql"

# Kubernetesクラスタ内のSQLサービスに接続するための情報を取得
# サービスのClusterIPを使用する
# sql_service_cluster_ip = f"{k8s_svc}.{k8s_ns}.svc.cluster.local"
# print(sql_service_cluster_ip)

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

        CREATE TABLE IF NOT EXISTS wp_nissy_counts (
            cleaned_uri VARCHAR(255),
            total_count INT
        );

        INSERT INTO wp_nissy_counts (cleaned_uri, total_count)
        SELECT 
            CASE
                WHEN RIGHT(uri, 1) = '/' THEN LEFT(uri, CHAR_LENGTH(uri) - 1)
                ELSE uri
            END as cleaned_uri,
            SUM(count) AS total_count
        FROM wp_statistics_pages
        GROUP BY cleaned_uri
        ORDER BY total_count DESC;

        # -- wp_nissy_kekkaテーブルが存在しない場合、作成する
        # CREATE TABLE IF NOT EXISTS wp_nissy_kekka (
        #     -- 必要に応じて適切なカラムを追加
        #     id INT AUTO_INCREMENT PRIMARY KEY,
        #     cleaned_uri VARCHAR(255),
        #     total_count INT,
        #     post_title VARCHAR(255),
        #     post_name VARCHAR(255),
        #     guid VARCHAR(255),
        #     post_status VARCHAR(50),
        #     post_type VARCHAR(50)
        # );

        # -- wp_nissy_countsとwp_nissy_postsを結合して、一致するデータをwp_nissy_kekkaに挿入
        # INSERT INTO wp_nissy_kekka (cleaned_uri, total_count, post_title, post_name, guid, post_status, post_type, post_date)
        # SELECT 
        #     nc.cleaned_uri,
        #     nc.total_count,
        #     np.post_title,
        #     np.post_name,
        #     np.guid,
        #     np.post_status,
        #     np.post_type,
        #     np.post_date
        # FROM wp_nissy_counts nc
        # INNER JOIN wp_nissy_posts np ON
        #     SUBSTRING_INDEX(SUBSTRING_INDEX(nc.cleaned_uri, '/', -1), '(', 1) = SUBSTRING_INDEX(SUBSTRING_INDEX(np.guid, '=', -1), '(', 1)
        #     OR
        #     SUBSTRING_INDEX(SUBSTRING_INDEX(nc.cleaned_uri, '/', -1), '(', 1) = SUBSTRING_INDEX(SUBSTRING_INDEX(np.guid, '=', -1), ')', 1);

        # -- 固定ページの部分の要素も挿入して, 一致するデータをwp_nissy_kekkaに挿入
        # INSERT INTO wp_nissy_kekka (cleaned_uri, total_count, post_title, post_name, guid, post_status, post_type, post_date)
        # SELECT 
        #     nc.cleaned_uri,
        #     nc.total_count,
        #     np.post_title,
        #     np.post_name,
        #     np.guid,
        #     np.post_status,
        #     np.post_type,
        #     np.post_date
        # FROM wp_nissy_counts nc
        # INNER JOIN wp_nissy_posts np ON
        #     SUBSTRING_INDEX(SUBSTRING_INDEX(nc.cleaned_uri, '/', -1), '(', 1) = SUBSTRING_INDEX(SUBSTRING_INDEX(np.guid, '=', -1), '(', 1)
        #     OR
        #     SUBSTRING_INDEX(SUBSTRING_INDEX(nc.cleaned_uri, '/', -1), '(', 1) = SUBSTRING_INDEX(SUBSTRING_INDEX(np.guid, '=', -1), ')', 1);

        # -- 固定ページの部分の要素も挿入して, 一致するデータをwp_nissy_kekkaに挿入
        # SELECT 
        #     post_title, 
        #     post_name, 
        #     guid, 
        #     post_status, 
        #     post_type, 
        #     total_count 
        # FROM 
        #     wp_nissy_posts 
        # JOIN 
        #     wp_nissy_counts 
        # ON 
        #     SUBSTRING_INDEX(wp_nissy_posts.post_name, "/", -1) = SUBSTRING_INDEX(wp_nissy_counts.cleaned_uri, "/", -1) 
        # WHERE 
        #     wp_nissy_posts.post_type = "page";
    '''

    # query2 = 'SELECT cleaned_uri, total_count, post_title FROM wp_nissy_kekka;' 

    cursor.execute(query, multi=True)
    # cursor.execute(query2)

    # results = cursor.fetchall()

    # 結果を表示（INSERT文の実行結果）
    print(f"Inserted {cursor.rowcount} rows.")

    # for row in results:
    #     print(row)

    # idsとcleaned_urisを使って何かをすることができます

finally:
    # 接続を閉じる
    conn.close()