# 学校説明会アンケートシステム

私立中学・高等学校の広報活動で使用する、Streamlit Cloudで動作するアンケートシステムです。

## 機能概要

### アンケートアプリ (app.py)
- 最大10名の同時接続をサポート
- アンケートの履歴管理（前後への移動、編集機能）
- 確定ボタンで送信し、新規作成で次のアンケートへ
- CSVダウンロード機能（その場でデータ出力可能）

### 管理画面 (admin.py)
- パスワード認証による保護
- リアルタイムでのデータ集計・可視化
- フィルタリング機能（期間、学年、地域）
- CSV/Excelでのデータエクスポート

## Streamlit Cloudでのデプロイ方法

1. GitHubにリポジトリを作成し、全ファイルをプッシュ

2. Streamlit Cloudでアプリを作成
   - https://share.streamlit.io/ にアクセス
   - GitHubアカウントでログイン
   - "New app"をクリック
   - リポジトリとブランチを選択
   - Main file pathに`app.py`を指定

3. シークレット設定
   - Streamlit Cloudの設定画面で"Secrets"タブを開く
   - 以下の内容を追加：

```toml
[admin]
password = "your-secure-password"

# Google Sheets連携を使用する場合（オプション）
[google_sheets]
spreadsheet_name = "学校説明会アンケート"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-key-id"
private_key = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email = "your-service-account@project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

## ローカルでの実行方法

```bash
# 仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# パッケージのインストール
pip install -r requirements.txt

# アンケートアプリの起動
streamlit run app.py

# 管理画面の起動（別ターミナル）
streamlit run admin.py --server.port 8502
```

## 使用方法

### アンケート入力（受験生・保護者向け）
1. アプリにアクセス
2. 「新規作成」ボタンをクリック
3. アンケートに回答
4. 「確定して送信」で送信完了
5. 「前へ」「次へ」ボタンで過去のアンケートを確認・編集可能

### データ管理（管理者向け）
1. 管理画面にアクセス
2. パスワードを入力してログイン
3. データの集計・分析を確認
4. 必要に応じてCSV/Excelでデータをエクスポート

## Google Sheets連携（推奨）

このアプリはGoogle Sheetsと連携してデータを永続保存できます。

### セットアップ
1. `GOOGLE_SHEETS_SETUP.md` の手順に従ってGoogle Cloud Projectを設定
2. サービスアカウントを作成し、JSONキーを取得
3. Google Sheetsを作成し、サービスアカウントと共有
4. Streamlit Cloudの設定画面でシークレットを設定

### 利点
- ✅ リアルタイムでデータが保存される
- ✅ ブラウザを閉じてもデータが残る
- ✅ 複数人でデータを共有・分析可能
- ✅ Excelファイルとして出力可能

## 注意事項

- Streamlit Cloudの無料プランは、アプリがアクティブでない場合スリープ状態になります
- Google Sheets連携なしの場合、データはセッション中のみ保持されます
- 管理者パスワードは必ず強固なものに変更してください
- Google Cloud Service AccountのJSONキーは機密情報として厳重に管理してください

## カスタマイズ

アンケート項目を変更する場合は、`app.py`の以下の部分を編集してください：
- 学年選択肢: 160-163行目
- 地域選択肢: 173-178行目
- 各質問の選択肢: 183-264行目