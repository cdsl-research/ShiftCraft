from kubernetes import client, config
import pymysql  # または適切なデータベースモジュールをインポート

def get_sql_service_endpoint(namespace, service_name):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    # サービスのエンドポイントを取得
    service = v1.read_namespaced_service(service_name, namespace)
    endpoint = service.spec.cluster_ip

    return endpoint

def execute_select_query_k8s(namespace, service_name, select_query):
    # Kubernetes上のSQLデータベースのエンドポイントを取得
    db_endpoint = get_sql_service_endpoint(namespace, service_name)
    # service_port = service.spec.port
    print(db_endpoint)

    # データベースに接続
    connection = pymysql.connect(
        host=db_endpoint,
        user='root',
        password='c0a21099',
        database='wordpress',
        port=3306  # MySQLの場合はポート3306を使用
    )
    cursor = connection.cursor()

    try:
        # SELECT文を実行
        cursor.execute(select_query)

        # 結果を取得
        results = cursor.fetchall()

        # 結果を表示
        for row in results:
            print(row)

    except pymysql.Error as e:
        print("MySQLエラー:", e)

    finally:
        # 接続を閉じる
        connection.close()

# Kubernetesのネームスペースとサービス名
namespace = "nissy"
service_name = "nissy-sql"

# 実行したいSELECT文
select_query = "SELECT * FROM wp_post;"

# SELECT文の実行
execute_select_query_k8s(namespace, service_name, select_query)
