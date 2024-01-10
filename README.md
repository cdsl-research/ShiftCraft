# ShiftCraft

<p>このプログラムは, WordPressを移行した際(VMからコンテナ環境など)に, 移行後の確認を支援するためのものです.</p>

## 使い方

### コンテナ環境(Kubernetes)上にMySQLがある場合
[抽出検索(公開されているページの上位10%を抜き出して確認する方法)]  
file: check-k8s.py

```
# Pythonの仮想環境を読み込む.
source .venv/bin/activate
python3 check-k8s.py
```

[全数検索(公開されているWordPressサイトのページすべてを検索する)]  
file: all-check-k8s.py
```
# Pythonの仮想環境を読み込む.
source .venv/bin/activate
python3 all-check-k8s.py
```

※なお, もう一度同じプログラムを実行する際, 現在の状態では, 更にテーブルを書き込む動作を行ってしまうため, 検索対象をもう一度検出するためにプログラムで作成したテーブルを削除する必要があります.

[もう一度実行する際]  
file:delete-k8s.py
```
# Pythonの仮想環境を読み込む.
source .venv/bin/activate
python3 delete-k8s.py
```
これによって, プログラムが作成したテーブルを削除し, もう一度プログラムを実行できるようになります.

## ご自身でプログラムを実行する際に, 変更していただく部分

` def check_http_status ` の部分.
- curlコマンドでステータスコードからページの有無を判断しています.
```
curl -I http://192.168.100.155:30280{cleaned_uri} | head -n 1 | cut -d' ' -f2
```
の部分のIPアドレス・Port番号(192.168.100.155:30280)はWordPressの公開しているURLの変更をお願いします.

` db_config ` の部分.
- 接続可能なデータベースの状態に変更してください.
(なお, データベースの接続情報は移行前のサーバーの指定が必要です.
これによって, 新環境にデータを移せているかどうかの判断を行います.)
