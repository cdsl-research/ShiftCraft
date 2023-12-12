import mysql.connector
import subprocess
import time

def execute_query(cursor, query, message):
    cursor.execute(query)
    print(f"{message} 完了済み.")

def create_and_insert_table(cursor, create_query, insert_query=None):
    execute_query(cursor, create_query, "テーブルの作成")
    if insert_query:
        execute_query(cursor, insert_query, "データの挿入")

def check_http_status(cleaned_uri):
    curl_command = f"curl -I http://192.168.100.146:30080{cleaned_uri} | head -n 1 | cut -d' ' -f2"
    return subprocess.check_output(curl_command, shell=True, text=True).strip()

def print_status_message(prefix, id_value, status, cleaned_uri_value):
    print(f"{prefix}_{id_value} : {status}")
    print(f"{prefix.lower()}:{id_value}: {cleaned_uri_value}\n")

start_time = time.time()

print("抽出検索用プログラム実行.\n")
print("実行時間計測開始.")

print()
print("Started SQL Connection.")
print()

# MySQLデータベースへの接続設定
db_config = {
    'host': 'c0a21099-master.a910.tak-cslab.org',
    'port': 30200,
    'user': 'cdsl',
    'password': 'cdsl2023',
    'database': 'wordpress',
    'auth_plugin': 'mysql_native_password',
}

# MySQLデータベースに接続
conn = mysql.connector.connect(**db_config)
conn.ping(reconnect=True)
print(f"DB_接続状態 : {conn.is_connected()}")

# idとcleaned_uriを保存するためのリスト
ids = []
cleaned_uris = []

# ページ結果を保存するためのリスト
ok_pages = []
ng_pages = []

try:
    # カーソルを取得
    cursor = conn.cursor()

    # SQLクエリをまとめる
    create_and_insert_table(cursor, 
                            """CREATE TABLE IF NOT EXISTS wp_nissy_posts (
                                post_title VARCHAR(255),
                                post_name VARCHAR(255),
                                guid VARCHAR(255),
                                post_status VARCHAR(255),
                                post_type VARCHAR(50)
                            );""",
                            """INSERT INTO wp_nissy_posts (post_title, post_name, guid, post_status, post_type)
                                SELECT post_title, post_name, guid, post_status, post_type
                                FROM wp_posts
                                WHERE post_status = 'publish';"""
                            )

    create_and_insert_table(cursor,
                            """CREATE TABLE IF NOT EXISTS wp_nissy_counts (
                                cleaned_uri VARCHAR(255),
                                total_count INT
                            );""",
                            """INSERT INTO wp_nissy_counts (cleaned_uri, total_count)
                                SELECT
                                    CASE
                                        WHEN RIGHT(uri, 1) = '/' THEN LEFT(uri, CHAR_LENGTH(uri) - 1)
                                        ELSE uri
                                    END as cleaned_uri,
                                    SUM(count) AS total_count
                                FROM wp_statistics_pages
                                GROUP BY cleaned_uri
                                ORDER BY total_count DESC;"""
                            )

    create_and_insert_table(cursor,
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
                                    SUBSTRING_INDEX(SUBSTRING_INDEX(nc.cleaned_uri, '/', -1), '(', 1) = SUBSTRING_INDEX(SUBSTRING_INDEX(np.guid, '=', -1), ')', 1);"""
                            )

    create_and_insert_table(cursor,
                            """INSERT INTO wp_nissy_kekka (cleaned_uri, post_title, post_name, guid, post_status, post_type, total_count)
                                SELECT 
                                    cleaned_uri,
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
                                    wp_nissy_posts.post_type = "page";"""
                            )

    create_and_insert_table(cursor,
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
                            """INSERT INTO wp_nissy_kekka_new (cleaned_uri, post_title, post_name, guid, post_status, post_type, total_count)
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
                                ORDER BY total_count DESC;"""
                            )

    print("All-Contents insert Completed.")

    # wp_nissy_kekka_new テーブルの最後のIDを取得
    cursor.execute("SELECT MAX(id) FROM wp_nissy_kekka_new;")
    max_id = cursor.fetchone()[0]
    # print(f"max_id : {max_id}")

    # 最後のIDの1割を計算
    range_start = 1
    range_end = max(1, int(0.1 * max_id))
    print()
    print("range_end : " + str(range_end))
    print()

    # wp_nissy_kekka_new テーブルから指定範囲のデータを取得
    cursor.execute("SELECT id, cleaned_uri, total_count, post_title, guid FROM wp_nissy_kekka_new;")
    selected_data = cursor.fetchall()

    # 取得したデータを変数に格納
    result_data = list(selected_data)

    ok_count, ng_count = 0, 0

    for i in range(0, range_end):
        id_value = result_data[i][0]
        cleaned_uri_value = result_data[i][1]

        # Curlを使用してHTTPステータスコードを取得
        status_code = check_http_status(cleaned_uri_value)

        # ステータスコードに応じてメッセージを表示
        if status_code.startswith(('2', '3')):
            ok_pages.append(f"{id_value}: {cleaned_uri_value}")
            print_status_message("page", id_value, "OK", cleaned_uri_value)
            ok_count += 1
        else:
            ng_pages.append(f"{id_value}: {cleaned_uri_value}")
            print_status_message("page", id_value, "NG", cleaned_uri_value)
            ng_count += 1

    # ファイルにデータを書き込む
    output_file_path = 'check-output.txt'
    try:
        with open(output_file_path, 'w') as f:
            f.write("OK Pages:\n")
            f.write("\n".join(ok_pages))
            f.write("\n\nNG Pages:\n")
            f.write("\n".join(ng_pages))
        print(f"データを {output_file_path} に書き込みました.")
    except Exception as e:
        print(f"Error: データの書き込みに失敗しました. 内容: {str(e)}")


    print(f"OK_TotalCount : {ok_count}")
    print(f"NG_TotalCount : {ng_count}")

    conn.commit()

finally:
    # 接続を閉じる
    conn.close()
    print()
    print("Closed SQL Connection.")

end_time = time.time()
elapsed_time = end_time - start_time

print()
print("計測終了.")
print(f"Elapsed Time: {elapsed_time:.2f} seconds.")