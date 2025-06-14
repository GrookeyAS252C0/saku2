# Google Sheets連携セットアップ手順

## 1. Google Cloud Projectの作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成
   - プロジェクト名: `school-survey-app`（任意）
   - 組織: 必要に応じて選択

## 2. Google Sheets APIの有効化

1. Google Cloud Consoleで「APIとサービス」→「ライブラリ」を開く
2. 「Google Sheets API」を検索して有効化
3. 「Google Drive API」も検索して有効化

## 3. サービスアカウントの作成

1. 「APIとサービス」→「認証情報」を開く
2. 「認証情報を作成」→「サービスアカウント」を選択
3. サービスアカウント情報を入力：
   - 名前: `survey-app-service`（任意）
   - 説明: `アンケートアプリ用サービスアカウント`
4. 「作成して続行」をクリック
5. 役割は設定不要（「完了」をクリック）

## 4. サービスアカウントキーの作成

1. 作成したサービスアカウントをクリック
2. 「キー」タブを開く
3. 「鍵を追加」→「新しい鍵を作成」
4. 「JSON」を選択して「作成」
5. **JSONファイルをダウンロード**（重要：安全に保管）

## 5. Google Sheetsの準備

1. [Google Sheets](https://sheets.google.com/) で新しいスプレッドシートを作成
2. 名前を `学校説明会アンケート` に変更（または任意の名前）
3. サービスアカウントと共有：
   - 「共有」ボタンをクリック
   - JSONファイル内の `client_email` の値をコピー
   - 共有相手として追加（編集権限を付与）

## 6. Streamlit Cloudでの設定

### secrets.tomlファイルの設定

Streamlit Cloudの設定画面で以下を設定：

```toml
[admin]
password = "your-secure-password"

[google_sheets]
spreadsheet_name = "学校説明会アンケート"
share_email = "your-email@example.com"  # 管理者のメール（任意）

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

### JSONファイルの値の取得方法

ダウンロードしたJSONファイルを開き、以下の値をコピー：

- `project_id`: プロジェクトID
- `private_key_id`: プライベートキーID
- `private_key`: プライベートキー（改行を `\n` に置換）
- `client_email`: サービスアカウントのメールアドレス
- `client_id`: クライアントID
- `client_x509_cert_url`: 証明書URL

## 7. テスト

1. アプリを起動
2. 「データ保存状態」を展開
3. ✅ Google Sheets接続正常 が表示されることを確認
4. アンケートを送信してGoogle Sheetsにデータが保存されることを確認

## 8. セキュリティ注意事項

- **JSONファイルは機密情報です**
- GitHubなどの公開リポジトリにアップロードしないでください
- `.gitignore` に `*.json` を追加することを推奨
- 定期的にサービスアカウントキーを更新してください

## トラブルシューティング

### エラー: "Spreadsheet not found"
- スプレッドシート名が正確に一致していることを確認
- サービスアカウントがスプレッドシートに共有されていることを確認

### エラー: "Permission denied"
- サービスアカウントに編集権限が付与されていることを確認
- Google Sheets API / Google Drive APIが有効になっていることを確認

### エラー: "Invalid credentials"
- JSONファイルの内容が正確にコピーされていることを確認
- 特に `private_key` の改行が正しく `\n` に置換されていることを確認

## 運用上の利点

✅ **リアルタイムデータ保存**: アンケート送信と同時にGoogle Sheetsに保存
✅ **永続化**: ブラウザを閉じてもデータが残る
✅ **共有**: 複数人でデータを確認・分析可能
✅ **バックアップ**: Googleのクラウドに自動保存
✅ **Excel互換**: Google SheetsはExcelファイルとして出力可能