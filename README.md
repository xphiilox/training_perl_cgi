# training_perl_cgi

CGI方式でのHTML表示と、PostgreSQL 18 を使った登録フォームの練習用リポジトリです。

## 使い方

```sh
make build
make up
```

ブラウザで開く:

```txt
http://localhost:3000
```

## PostgreSQL 18

PostgreSQL 18 は Docker Compose の `db` サービスとして起動します。初回起動時に `db/schema.sql` が読み込まれ、登録フォーム用の `registrations` テーブルが作成されます。

接続設定の初期値:

```sh
DB_HOST=db
DB_PORT=5432
DB_NAME=training_perl
DB_USER=training_perl
DB_PASSWORD=training_perl
```

接続情報を変える場合は `.env.example` を参考に `.env` を作成してください。

## 画面

- `http://localhost:3000/`
- `http://localhost:3000/register.cgi`

## テスト

```sh
make test
```
