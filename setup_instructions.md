# 学校アカウント連携セットアップ手順

## 1. Google Cloud Console設定

### 新しいプロジェクト作成
1. 学校のGoogleアカウントでログイン
2. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
3. 新しいプロジェクト作成：`nichidai-survey-app`

### API有効化
1. Google Sheets API を有効化
2. Google Calendar API を有効化

### サービスアカウント作成
1. IAM & Admin → サービスアカウント
2. 「サービスアカウントを作成」をクリック
3. 名前：`survey-app-service`
4. 説明：`Survey app service account`
5. 権限：`編集者` を付与
6. JSONキーを作成・ダウンロード

## 2. データ移行

### スプレッドシート
1. 現在のデータをCSVでエクスポート
2. 学校アカウントで新しいスプレッドシートを作成
3. データをインポート
4. スプレッドシートIDを記録
5. サービスアカウントのメールアドレスに編集者権限を付与

### カレンダー
1. `nichidai1.haishin@gmail.com` カレンダーの設定
2. サービスアカウントのメールアドレスに閲覧者権限を付与

## 3. Streamlit設定更新

### secrets.toml の更新
```toml
[gcp_service_account]
type = "service_account"
project_id = "新しいプロジェクトID"
private_key_id = "新しいキーID"
private_key = "新しい秘密鍵"
client_email = "新しいサービスアカウントメール"
client_id = "新しいクライアントID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "新しいX509 URL"
universe_domain = "googleapis.com"
```

### app.py の更新
```python
# スプレッドシートIDを更新
SPREADSHEET_ID = "新しいスプレッドシートID"
```

## 4. 権限確認

### サービスアカウントが以下にアクセスできることを確認：
- ✅ Google Sheets（編集権限）
- ✅ Google Calendar（閲覧権限）

## 5. テスト

1. アプリを再起動
2. アンケート送信テスト
3. カレンダー表示テスト