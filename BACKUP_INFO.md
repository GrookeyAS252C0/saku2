# バックアップ情報

## 作成日時
2025年6月14日 19:54

## バックアップ内容
日本大学第一中学・高等学校 学校説明会アンケートシステム

### 主要機能
- Google Sheets連携によるデータ永続化
- アンケート履歴管理（前後移動・編集機能）
- 管理画面での分析・エクスポート機能
- Streamlit Cloud完全対応

### バックアップファイル
- **フォルダ**: `/Users/takashikemmoku/Desktop/saku2_backup_20250614_195424/`
- **圧縮ファイル**: `/Users/takashikemmoku/Desktop/saku2_backup_20250614_195432.tar.gz`

### 含まれるファイル
- `app.py` - メインアプリケーション
- `admin.py` - 管理画面
- `requirements.txt` - 依存パッケージ
- `.streamlit/config.toml` - Streamlit設定
- `README.md` - 使用方法
- `GOOGLE_SHEETS_SETUP.md` - Google Sheets設定手順
- `.gitignore` - Git除外設定

### バージョン情報
- 学年デフォルト: 小学6年生
- 受験決め手: チェックボックス形式（制限なし）
- 学校名表示: 日本大学第一中学・高等学校

### GitHubリポジトリ
https://github.com/GrookeyAS252C0/saku2.git
最新コミット: 669bcf0

## 復元方法

### フォルダから復元
```bash
cp -r /Users/takashikemmoku/Desktop/saku2_backup_20250614_195424 /path/to/restore/location
```

### 圧縮ファイルから復元
```bash
tar -xzf /Users/takashikemmoku/Desktop/saku2_backup_20250614_195432.tar.gz -C /path/to/restore/location
```

### GitHubから復元
```bash
git clone https://github.com/GrookeyAS252C0/saku2.git
```