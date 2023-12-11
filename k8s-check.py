import mysql.connector
import subprocess

import time


start_time = time.time()  # プログラムの実行開始時刻

print("プログラム実行時間計測開始.")

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

# MySQLデータベース(k8s用)
db_config_k8s = {
    'host': 'c0a21099-master.a910.tak-cslab.org',
    'port': 30200,
    'user': 'cdsl',
    'password': 'cdsl2023',
    'database': 'wordpress',
    'auth_plugin': 'mysql_native_password',
}

# MySQLデータベースに接続
conn = mysql.connector.connect(**db_config_k8s)

conn.ping(reconnect=True)
print(conn.is_connected())

# idとcleaned_uriを保存するためのリスト
ids = []
cleaned_uris = []

try:
    # カーソルを取得
    cursor = conn.cursor()

    # SQLクエリを実行
    queries = [
        # Publishのみの記事の情報を保存するテーブルの作成.
        """CREATE TABLE IF NOT EXISTS wp_nissy_posts (
            post_title VARCHAR(255),
            post_name VARCHAR(255),
            guid VARCHAR(255),
            post_status VARCHAR(255),
            post_type VARCHAR(50)
        );""",
        
        # 記事の情報を上のテーブルに挿入.
        """INSERT INTO wp_nissy_posts (post_title, post_name, guid, post_status, post_type)
        SELECT post_title, post_name, guid, post_status, post_type
        FROM wp_posts
        WHERE post_status = 'publish';""",

        # アクセス数の情報をまとめ保存するテーブルの作成.
        """CREATE TABLE IF NOT EXISTS wp_nissy_counts (
            cleaned_uri VARCHAR(255),
            total_count INT
        );""",

        # アクセス数の情報を上のテーブルに挿入.
        """INSERT INTO wp_nissy_counts (cleaned_uri, total_count)
        SELECT
            CASE
                WHEN RIGHT(uri, 1) = '/' THEN LEFT(uri, CHAR_LENGTH(uri) - 1)
                ELSE uri
            END as cleaned_uri,
            SUM(count) AS total_count
        FROM wp_statistics_pages
        GROUP BY cleaned_uri
        ORDER BY total_count DESC;""",

        # # wp_nissy_kekkaテーブルが存在しない場合、作成する
        """CREATE TABLE IF NOT EXISTS wp_nissy_kekka (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cleaned_uri VARCHAR(255),
            total_count INT,
            post_title VARCHAR(255),
            post_name VARCHAR(255),
            guid VARCHAR(255),
            post_status VARCHAR(50),
            post_type VARCHAR(50),
            post_date datetime
        );""",
        
        # # wp_nissy_countsとwp_nissy_postsを結合して、一致するデータをwp_nissy_kekkaに挿入
        """INSERT INTO wp_nissy_kekka (cleaned_uri, total_count, post_title, post_name, guid, post_status)
            SELECT 
                nc.cleaned_uri,
                nc.total_count,
                np.post_title,
                np.post_name,
                np.guid,
                np.post_status
            FROM wp_nissy_counts nc
            INNER JOIN wp_nissy_posts np ON
                SUBSTRING_INDEX(SUBSTRING_INDEX(nc.cleaned_uri, '/', -1), '(', 1) = SUBSTRING_INDEX(SUBSTRING_INDEX(np.guid, '=', -1), '(', 1)
                OR
                SUBSTRING_INDEX(SUBSTRING_INDEX(nc.cleaned_uri, '/', -1), '(', 1) = SUBSTRING_INDEX(SUBSTRING_INDEX(np.guid, '=', -1), ')', 1);""",

        # WordPressの固定ページのような投稿タイプがpageのときの処理をここに追加しておく
        """
        INSERT INTO wp_nissy_kekka (post_title, post_name, guid, post_status, post_type, total_count)
        SELECT 
            post_title, 
            post_name, 
            guid, 
            post_status, 
            post_type, 
            total_count 
        FROM 
            wp_nissy_posts 
        JOIN 
            wp_nissy_counts 
        ON 
            SUBSTRING_INDEX(wp_nissy_posts.post_name, "/", -1) = SUBSTRING_INDEX(wp_nissy_counts.cleaned_uri, "/", -1) 
        WHERE 
            wp_nissy_posts.post_type = "page";
        """,

        # 固定ページまで含めた結果
        # # wp_nissy_kekka_newテーブルが存在しない場合、作成する
        """CREATE TABLE IF NOT EXISTS wp_nissy_kekka_new (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cleaned_uri VARCHAR(255),
            total_count INT,
            post_title VARCHAR(255),
            post_name VARCHAR(255),
            guid VARCHAR(255),
            post_status VARCHAR(50),
            post_type VARCHAR(50),
            post_date datetime
        );""",

        # WordPressの固定ページのような投稿タイプがpageのときの処理をここに追加しておく
        """
        INSERT INTO wp_nissy_kekka_new (cleaned_uri, post_title, post_name, guid, post_status, post_type, total_count)
        SELECT 
            cleaned_uri,
            post_title, 
            post_name, 
            guid, 
            post_status, 
            post_type, 
            total_count 
        FROM 
            wp_nissy_kekka
        ORDER BY total_count DESC;
        """,
    ]
        
    cursor.execute(queries[0])  # テーブルの作成
    print("テーブル作成完了済み.")
    cursor.execute(queries[1])  # データの挿入
    print("デーブル挿入完了済み.")
    
    print()

    cursor.execute(queries[2])  # テーブルの作成
    print("テーブル作成完了済み.")
    cursor.execute(queries[3])  # データの挿入
    print("デーブル挿入完了済み.")
    
    print()

    cursor.execute(queries[4])  # テーブルの作成
    print("テーブル作成完了済み.")
    cursor.execute(queries[5])  # データの挿入
    print("デーブル挿入完了済み.")
    print()
    cursor.execute(queries[6])  # データの挿入
    print("デーブル挿入完了済み.")

    print()
    cursor.execute(queries[7])  # wp_nissy_kekka_new
    print("テーブル作成完了済み.")
    cursor.execute(queries[8])  # データの挿入
    print("デーブル挿入完了済み.")
    
    # wp_nissy_kekka_new テーブルの最後のIDを取得
    cursor.execute("SELECT MAX(id) FROM wp_nissy_kekka_new;")
    max_id = cursor.fetchone()[0]

    # 最後のIDの1割を計算
    range_start = 1
    range_end = max(1, int(0.1 * max_id))

    print()
    print("range_end : " + str(range_end))
    print()

    # wp_nissy_kekka_new テーブルから指定範囲のデータを取得
    cursor.execute(f"SELECT id, cleaned_uri, total_count, post_title, guid FROM wp_nissy_kekka_new WHERE id BETWEEN {range_start} AND {range_end};")
    selected_data = cursor.fetchall()

    # 取得したデータを変数に格納
    result_data = list(selected_data)
    print("check\n" )

    for i in range(0, range_end):
        id_value = result_data[i][0]
        cleaned_uri_value = result_data[i][1]

        # Curlを使用してHTTPステータスコードを取得
        curl_command = f"curl -I http://192.168.100.146:30080{cleaned_uri_value} | head -n 1 | cut -d' ' -f2"
        status_code = subprocess.check_output(curl_command, shell=True, text=True).strip()

        # ステータスコードに応じてメッセージを表示
        if status_code.startswith('2'):
            print(f"page_{id_value} : ok")
        else:
            print(f"page_{id_value} : NG")

        print("No:" + str(id_value) + ": " + str(cleaned_uri_value) + "\n")

    # ファイルにデータを書き込む
    with open('output.txt', 'w') as f:
        for row in result_data:
            f.write(str(row) + '\n')


    # # 取得したデータを表示
    # for row in selected_data:
    #     print(row)

    print()

    print(result_data)

    print()

    # print("subprocessのテスト")
    # proc = subprocess.run(["ls"],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    # print(proc.stdout.decode("utf8"))

    conn.commit()

finally:
    # 接続を閉じる
    conn.close()
    print()
    print("Closed SQL Connection.")

end_time = time.time()  # プログラムの実行終了時刻
elapsed_time = end_time - start_time

print()
print("計測終了.")
print(f"Elapsed Time: {elapsed_time:.2f} seconds.")