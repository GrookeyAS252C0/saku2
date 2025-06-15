import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
import json
import uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import time

# 日本時間（JST）の設定
JST = timezone(timedelta(hours=+9))

def get_jst_now():
    """現在の日本時間を取得"""
    return datetime.now(JST)

@st.cache_data(ttl=3600)  # 1時間キャッシュ
def get_calendar_events():
    """Google Calendarからイベントを取得"""
    try:
        # 認証情報の設定（既存のGoogle Sheets認証を流用）
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/calendar.readonly"
            ]
        )
        
        # Calendar APIサービスの構築
        service = build('calendar', 'v3', credentials=credentials)
        
        # カレンダーID
        calendar_id = 'nichidai1.haishin@gmail.com'
        
        # 現在から1年先までのイベントを取得
        now = datetime.now(JST).isoformat()
        one_year_later = (datetime.now(JST) + timedelta(days=365)).isoformat()
        
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=one_year_later,
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # イベントデータをDataFrameに変換
        event_data = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            # 日付の解析と表示用フォーマット
            if 'T' in start:  # 時刻あり
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                # JSTに変換
                start_jst = start_dt.astimezone(JST)
                end_jst = end_dt.astimezone(JST)
                date_str = start_jst.strftime('%Y年%m月%d日')
                time_str = f"{start_jst.strftime('%H:%M')} - {end_jst.strftime('%H:%M')}"
            else:  # 終日イベント
                start_dt = datetime.fromisoformat(start + 'T00:00:00')
                date_str = start_dt.strftime('%Y年%m月%d日')
                time_str = "終日"
            
            event_data.append({
                'title': event.get('summary', '無題'),
                'date': date_str,
                'time': time_str,
                'description': event.get('description', ''),
                'start_datetime': start_dt
            })
        
        return pd.DataFrame(event_data)
    
    except Exception as e:
        st.error(f"カレンダーの読み込みに失敗しました: {str(e)}")
        return pd.DataFrame()

def display_calendar_events():
    """カレンダーイベントを美しく表示"""
    events_df = get_calendar_events()
    
    if events_df.empty:
        st.info("📅 現在表示できるイベントがありません")
        return
    
    st.markdown("### 📅 学校行事・年間予定")
    
    # 今月のイベント
    current_month = datetime.now(JST).strftime('%Y年%m月')
    current_events = events_df[events_df['date'].str.contains(current_month)]
    
    if not current_events.empty:
        st.markdown(f"#### 🗓️ {current_month}の予定")
        for _, event in current_events.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{event['title']}**")
                    if event['description']:
                        st.markdown(f"_{event['description']}_")
                with col2:
                    st.markdown(f"📅 {event['date']}")
                    st.markdown(f"⏰ {event['time']}")
                st.divider()
    
    # 今後のイベント（来月以降）
    next_month_events = events_df[~events_df['date'].str.contains(current_month)]
    
    if not next_month_events.empty:
        st.markdown("#### 📆 今後の予定")
        
        # 月ごとにグループ化
        for month in next_month_events['date'].str[:7].unique()[:3]:  # 最大3ヶ月分
            month_events = next_month_events[next_month_events['date'].str.startswith(month)]
            month_name = datetime.strptime(month + '-01', '%Y年%m-01').strftime('%Y年%m月')
            
            with st.expander(f"📅 {month_name} ({len(month_events)}件)"):
                for _, event in month_events.iterrows():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{event['title']}**")
                        if event['description']:
                            st.markdown(f"_{event['description']}_")
                    with col2:
                        st.markdown(f"📅 {event['date']}")
                        st.markdown(f"⏰ {event['time']}")
                    st.divider()

# ページ設定
st.set_page_config(
    page_title="日本大学第一中学・高等学校 学校説明会アンケート",
    page_icon="🏫",
    layout="wide"
)

# データクラス定義
@dataclass
class SurveyResponse:
    id: str
    timestamp: str
    grade: str
    gender: str
    area: str
    triggers: List[str]
    decision_factors: List[str]
    education_attractions: List[str]
    expectations: List[str]
    info_sources: List[str]
    venue: str = ""
    submitted: bool = False

# 本番環境設定
DEBUG_MODE = False  # 本番環境ではFalseに設定

# セッション状態の初期化
if 'survey_history' not in st.session_state:
    st.session_state.survey_history = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = -1
if 'editing_mode' not in st.session_state:
    st.session_state.editing_mode = False
if 'all_submissions' not in st.session_state:
    st.session_state.all_submissions = []

def create_new_survey():
    """新しいアンケートを作成"""
    # 現在編集中の空のアンケートがある場合は、新規作成せずにそれを使用
    if st.session_state.current_index >= 0:
        current_survey = st.session_state.survey_history[st.session_state.current_index]
        survey_dict = asdict(current_survey)
        is_valid, _ = is_survey_data_valid(survey_dict)
        
        # 現在のアンケートが未送信で空の場合は、新規作成しない
        if not current_survey.submitted and not is_valid:
            st.session_state.editing_mode = True
            return
    
    venue_name = get_venue_info()  # URLパラメータから会場を取得
    
    # ユーザーセッションIDがない場合は生成
    if 'user_session_id' not in st.session_state:
        st.session_state.user_session_id = str(uuid.uuid4())
    
    # ユーザーセッションIDの最初の8文字をIDに含める
    survey_id = f"{st.session_state.user_session_id[:8]}_{str(uuid.uuid4())[:8]}"
    
    new_survey = SurveyResponse(
        id=survey_id,
        timestamp="",  # 作成時は空にして、送信時にタイムスタンプを設定
        grade="",
        gender="",
        area="",
        triggers=[],
        decision_factors=[],
        education_attractions=[],
        expectations=[],
        info_sources=[],
        venue=venue_name,
        submitted=False
    )
    st.session_state.survey_history.append(new_survey)
    st.session_state.current_index = len(st.session_state.survey_history) - 1
    st.session_state.editing_mode = True

def save_current_survey(survey_data: Dict[str, Any]):
    """現在のアンケートを保存"""
    if st.session_state.current_index >= 0:
        current_survey = st.session_state.survey_history[st.session_state.current_index]
        for key, value in survey_data.items():
            setattr(current_survey, key, value)

def is_survey_data_valid(survey_data):
    """アンケートデータが有効かどうかを判定"""
    # 必須項目：学年、性別、地域
    if not survey_data.get("grade") or not survey_data.get("gender") or not survey_data.get("area"):
        return False, "基本情報（学年・性別・地域）が未入力です"
    
    # 少なくとも1つの質問項目に回答があるかチェック
    question_fields = ["triggers", "decision_factors", "education_attractions", "expectations", "info_sources"]
    has_answers = False
    
    for field in question_fields:
        if survey_data.get(field) and len(survey_data[field]) > 0:
            has_answers = True
            break
    
    if not has_answers:
        return False, "質問項目（1〜5番）に少なくとも1つは回答してください"
    
    return True, "データは有効です"

def submit_survey():
    """アンケートを確定して送信"""
    if st.session_state.current_index >= 0:
        current_survey = st.session_state.survey_history[st.session_state.current_index]
        
        # データの有効性をチェック
        survey_dict = asdict(current_survey)
        is_valid, message = is_survey_data_valid(survey_dict)
        
        if not is_valid:
            st.error(f"❌ 送信できません：{message}")
            return False
        
        current_survey.submitted = True
        current_survey.timestamp = get_jst_now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 全体の送信リストに追加
        st.session_state.all_submissions.append(asdict(current_survey))
        
        # CSVに保存（Streamlit Cloud対応）
        save_to_cloud_storage(asdict(current_survey))
        
        st.session_state.editing_mode = False
        return True

def update_existing_record_in_sheets(data: Dict[str, Any]):
    """既存レコードをGoogle Sheetsで更新"""
    try:
        # st.write(f"🔍 既存レコード更新開始: ID={data.get('id', 'N/A')}")
        
        # Google Sheets認証
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(credentials)
        
        # スプレッドシートを開く
        spreadsheet_name = st.secrets["google_sheets"]["spreadsheet_name"]
        sh = gc.open(spreadsheet_name)
        worksheet = sh.sheet1
        
        # 既存レコードを検索
        all_data = worksheet.get_all_values()
        target_id = data.get('id', '')
        
        for row_index, row in enumerate(all_data):
            if len(row) > 0 and row[0] == target_id:  # IDが一致
                # 行番号（1ベース）
                sheet_row = row_index + 1
                st.write(f"🔍 既存レコード発見: 行{sheet_row}")
                
                # データを整形
                row_data = [
                    data.get("id", ""),
                    data.get("timestamp", ""),
                    data.get("venue", ""),
                    data.get("grade", ""),
                    data.get("gender", ""),
                    data.get("area", ""),
                    ", ".join(data.get("triggers", [])),
                    ", ".join(data.get("decision_factors", [])),
                    ", ".join(data.get("education_attractions", [])),
                    ", ".join(data.get("expectations", [])),
                    ", ".join(data.get("info_sources", []))
                ]
                
                # 行を更新
                worksheet.update(f'A{sheet_row}:K{sheet_row}', [row_data])
                st.success(f"✅ 既存レコード（行{sheet_row}）を更新しました")
                return True
        
        # 既存レコードが見つからない場合
        st.warning("⚠️ 既存レコードが見つかりません。新規レコードとして追加します。")
        return False
        
    except Exception as e:
        st.error(f"❌ 既存レコード更新エラー: {e}")
        return False

def save_to_google_sheets(data: Dict[str, Any]):
    """Google Sheetsにデータを保存（新規/更新自動判別）"""
    try:
        # データの有効性チェック
        is_valid, validation_message = is_survey_data_valid(data)
        if not is_valid:
            st.warning(f"⚠️ Google Sheetsへの保存をスキップ：{validation_message}")
            return False
        
        # まず既存レコードの更新を試行
        if update_existing_record_in_sheets(data):
            return True  # 更新成功
        
        # 既存レコードがない場合は新規追加
        
        # Google Sheets認証
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(credentials)
        
        # スプレッドシートを開く
        spreadsheet_name = st.secrets["google_sheets"]["spreadsheet_name"]
        try:
            sh = gc.open(spreadsheet_name)
        except gspread.SpreadsheetNotFound:
            # スプレッドシートが存在しない場合は作成
            sh = gc.create(spreadsheet_name)
            # 共有設定（編集可能）
            sh.share(st.secrets["google_sheets"].get("share_email", ""), perm_type='user', role='writer')
        
        worksheet = sh.sheet1
        
        # ヘッダーを設定（エラー回避のため簡略化）
        try:
            # まずシートの状態を確認
            try:
                all_data = worksheet.get_all_records()
                
                if not all_data:  # データがない場合は新規作成
                    expected_headers = [
                        "ID", "送信日時", "会場", "学年", "性別", "地域",
                        "きっかけ", "決め手", "教育内容", "期待", "情報源"
                    ]
                    worksheet.insert_row(expected_headers, 1)
                    st.info("✅ Google Sheetsにヘッダーを作成しました")
                else:
                    # データがある場合は既存のヘッダーをチェック
                    first_row = worksheet.row_values(1)
                    
                    if first_row and "会場" not in first_row:
                        # 会場列がない場合の警告のみ（自動修正はスキップ）
                        st.warning("⚠️ 古いフォーマットのシートです。手動で「会場」列を追加することをお勧めします。")
            except Exception as header_error:
                # ヘッダー処理でエラーが発生した場合は詳細を表示
                st.error(f"❌ ヘッダー処理エラーの詳細: {str(header_error)}")
                st.error(f"❌ エラータイプ: {type(header_error)}")
                import traceback
                st.error(f"❌ スタックトレース: {traceback.format_exc()}")
                
        except Exception as e:
            # 全体的なエラーハンドリング
            st.error(f"❌ シート設定エラーの詳細: {str(e)}")
            st.error(f"❌ エラータイプ: {type(e)}")
            import traceback
            st.error(f"❌ スタックトレース: {traceback.format_exc()}")
            pass
        
        # データを整形
        row_data = [
            data.get("id", ""),
            data.get("timestamp", ""),
            data.get("venue", ""),
            data.get("grade", ""),
            data.get("gender", ""),
            data.get("area", ""),
            ", ".join(data.get("triggers", [])),
            ", ".join(data.get("decision_factors", [])),
            ", ".join(data.get("education_attractions", [])),
            ", ".join(data.get("expectations", [])),
            ", ".join(data.get("info_sources", []))
        ]
        
        # データを追加
        worksheet.append_row(row_data)
        return True
        
    except Exception as e:
        st.error(f"Google Sheetsへの保存エラー: {e}")
        return False

def save_to_cloud_storage(data: Dict[str, Any]):
    """データ保存の統合関数"""
    # セッション状態に保存（一時的）
    if 'saved_data' not in st.session_state:
        st.session_state.saved_data = []
    st.session_state.saved_data.append(data)
    
    # Google Sheetsに保存
    success = save_to_google_sheets(data)
    if success:
        st.success("✅ Google Sheetsに保存しました")
    else:
        st.error("❌ Google Sheetsへの保存に失敗しました")
        return False
    
    # ダウンロード用のデータを準備
    df = pd.DataFrame(st.session_state.saved_data)
    st.session_state.export_data = df
    return True

def get_valid_survey_indices():
    """有効なアンケートのインデックスリストを取得"""
    valid_indices = []
    for i, survey in enumerate(st.session_state.survey_history):
        survey_dict = asdict(survey)
        is_valid, _ = is_survey_data_valid(survey_dict)
        if survey.submitted or is_valid:
            valid_indices.append(i)
    return valid_indices

def navigate_previous():
    """前の有効なアンケートに戻る"""
    valid_indices = get_valid_survey_indices()
    if not valid_indices:
        return
    
    current_pos = None
    for i, idx in enumerate(valid_indices):
        if idx == st.session_state.current_index:
            current_pos = i
            break
    
    if current_pos is not None and current_pos > 0:
        st.session_state.current_index = valid_indices[current_pos - 1]
        st.session_state.editing_mode = True

def navigate_next():
    """次の有効なアンケートに進む"""
    valid_indices = get_valid_survey_indices()
    if not valid_indices:
        return
    
    current_pos = None
    for i, idx in enumerate(valid_indices):
        if idx == st.session_state.current_index:
            current_pos = i
            break
    
    if current_pos is not None and current_pos < len(valid_indices) - 1:
        st.session_state.current_index = valid_indices[current_pos + 1]
        st.session_state.editing_mode = True

def load_user_data_from_sheets():
    """Google Sheetsからすべてのアンケートデータを読み込む（デバッグ用）"""
    try:
        st.write("🔍 データ復旧: 開始")
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(credentials)
        spreadsheet_name = st.secrets["google_sheets"]["spreadsheet_name"]
        sh = gc.open(spreadsheet_name)
        worksheet = sh.sheet1
        st.write("🔍 データ復旧: Google Sheets接続完了")
        
        # シートからすべてのデータを取得
        all_data = worksheet.get_all_records()
        st.write(f"🔍 データ復旧: {len(all_data)}件のレコードを取得")
        
        if not all_data:
            st.info("Google Sheetsにデータが見つかりませんでした")
            return []
        
        # 最新のデータから最大5件を復旧対象とする
        user_data = []
        for i, row in enumerate(all_data[-5:]):  # 最新5件
            st.write(f"🔍 処理中のレコード{i+1}: {row}")
            try:
                # 空の値をフィルタリング
                triggers = [t for t in str(row.get('きっかけ', '')).split(', ') if t.strip()]
                decision_factors = [d for d in str(row.get('決め手', '')).split(', ') if d.strip()]
                education_attractions = [e for e in str(row.get('教育内容', '')).split(', ') if e.strip()]
                expectations = [ex for ex in str(row.get('期待', '')).split(', ') if ex.strip()]
                info_sources = [inf for inf in str(row.get('情報源', '')).split(', ') if inf.strip()]
                
                survey = SurveyResponse(
                    id=str(row.get('ID', f'restored_{i}')),
                    timestamp=str(row.get('送信日時', get_jst_now().strftime('%Y-%m-%d %H:%M:%S'))),
                    venue=str(row.get('会場', 'メイン会場')),
                    grade=str(row.get('学年', '')),
                    gender=str(row.get('性別', '')),
                    area=str(row.get('地域', '')),
                    triggers=triggers,
                    decision_factors=decision_factors,
                    education_attractions=education_attractions,
                    expectations=expectations,
                    info_sources=info_sources,
                    submitted=True
                )
                user_data.append(survey)
                st.write(f"✅ レコード{i+1}の変換完了")
            except Exception as row_error:
                st.warning(f"⚠️ レコード{i+1}の処理エラー: {row_error}")
                continue
        
        st.write(f"🔍 データ復旧: {len(user_data)}件のデータを変換完了")
        return user_data
        
    except Exception as e:
        st.error(f"❌ データ復旧エラー: {str(e)}")
        import traceback
        st.error(f"❌ スタックトレース: {traceback.format_exc()}")
        return []

def check_google_sheets_connection():
    """Google Sheets接続状態をチェック"""
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(credentials)
        spreadsheet_name = st.secrets["google_sheets"]["spreadsheet_name"]
        sh = gc.open(spreadsheet_name)
        return True, "✅ Google Sheets接続正常"
    except Exception as e:
        return False, f"❌ Google Sheets接続エラー: {str(e)[:100]}..."

def get_venue_info():
    """URLパラメータから会場情報を取得"""
    try:
        # Streamlit 1.32以降の新しいAPI
        params = st.query_params
        venue_code = params.get('venue', '')
        
        if venue_code == 'a':
            return "A会場"
        elif venue_code == 'b':
            return "B会場"
        else:
            return "メイン会場"
    except:
        return "メイン会場"

def recover_user_data():
    """ユーザーデータを復旧"""
    try:
        st.write("🔍 復旧開始: データ読み込み呼び出し")
        loaded_data = load_user_data_from_sheets()
        st.write(f"🔍 復旧: {len(loaded_data)}件のデータを受信")
        
        if loaded_data:
            # セッション状態を更新
            st.session_state.survey_history = loaded_data
            st.session_state.current_index = len(loaded_data) - 1
            
            # 送信データリストに追加
            for survey in loaded_data:
                st.session_state.all_submissions.append(asdict(survey))
            
            # 保存データリストに追加
            if 'saved_data' not in st.session_state:
                st.session_state.saved_data = []
            for survey in loaded_data:
                st.session_state.saved_data.append(asdict(survey))
            
            st.write(f"🔍 復旧完了: セッション状態を更新")
            st.write(f"🔍 survey_history件数: {len(st.session_state.survey_history)}")
            st.write(f"🔍 current_index: {st.session_state.current_index}")
            
            # 復旧完了フラグを設定
            st.session_state.recovery_completed = True
            st.session_state.show_recovery_option = False
            
            st.success(f"✅ {len(loaded_data)}件のアンケートデータを復旧しました")
            
            # ページを更新せず、フラグのみ設定
            # st.rerun()を削除して、main関数内で表示を制御
        else:
            st.info("復旧できるデータが見つかりませんでした")
            st.session_state.show_recovery_option = False
        
    except Exception as e:
        st.error(f"❌ データ復旧エラー: {e}")
        import traceback
        st.error(f"❌ スタックトレース: {traceback.format_exc()}")

def initialize_session():
    """セッション初期化"""
    # ユーザーセッションIDを設定（ブラウザセッション間で永続化）
    if 'user_session_id' not in st.session_state:
        st.session_state.user_session_id = str(uuid.uuid4())
    
    # 初期化フラグ
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        # Google Sheets接続確認とデータ復旧の案内
        connection_status, _ = check_google_sheets_connection()
        if connection_status:
            # アプリ上部に復旧オプションを表示
            st.session_state.show_recovery_option = True

def main():
    # セッション初期化
    initialize_session()
    
    # 募集要項ページの確認
    if 'show_admission_guide' in st.session_state and st.session_state.show_admission_guide:
        show_admission_guide_page()
        return
    
    # 合格最低点ページの確認
    if 'show_exam_results' in st.session_state and st.session_state.show_exam_results:
        show_exam_results_page()
        return
    
    # 受験生動向データページの確認
    if 'show_exam_data' in st.session_state and st.session_state.show_exam_data:
        show_exam_data_page()
        return
    
    # 会場情報を取得
    venue_name = get_venue_info()
    
    # ヘッダー
    st.title("🏫 日本大学第一中学・高等学校 学校説明会アンケート")
    if venue_name != "メイン会場":
        st.info(f"📍 会場：{venue_name}")
    st.markdown("日大一に興味をもっていただき、ありがとうございます。")
    
    # メインレイアウト：左側（アンケート）、右側（情報リンク）
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # データ復旧オプションの表示
        if hasattr(st.session_state, 'show_recovery_option') and st.session_state.show_recovery_option:
            if not st.session_state.survey_history:  # まだアンケートがない場合
                st.info("💡 以前のアンケートデータを復旧できます")
                col_recover, col_skip = st.columns(2)
                with col_recover:
                    if st.button("📥 データを復旧", use_container_width=True):
                        recover_user_data()
                with col_skip:
                    if st.button("🆕 新規開始", use_container_width=True):
                        st.session_state.show_recovery_option = False
                        st.rerun()
        
        # 復旧完了メッセージの表示
        if hasattr(st.session_state, 'recovery_completed') and st.session_state.recovery_completed:
            st.success(f"✅ {len(st.session_state.survey_history)}件のアンケートデータを復旧しました")
            # 復旧完了フラグをリセット
            st.session_state.recovery_completed = False
        
        # Google Sheets接続状態を表示
        with st.expander("🔗 データ保存状態", expanded=False):
            connection_status, message = check_google_sheets_connection()
            if connection_status:
                st.success(message)
            else:
                st.error(message)
                st.info("💡 データはセッション内に一時保存され、CSV出力は可能です")
        
        # ナビゲーションバー
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
    
        with col1:
            # 有効なアンケートの中での前のナビゲーション判定
            valid_indices = get_valid_survey_indices()
            current_pos_in_valid = None
            
            for i, idx in enumerate(valid_indices):
                if idx == st.session_state.current_index:
                    current_pos_in_valid = i
                    break
            
            prev_disabled = (current_pos_in_valid is None or current_pos_in_valid <= 0)
            
            if st.button("◀ 前へ", disabled=prev_disabled, use_container_width=True):
                navigate_previous()
        
        with col2:
            # 有効なアンケートの中での次のナビゲーション判定
            next_disabled = (current_pos_in_valid is None or current_pos_in_valid >= len(valid_indices) - 1)
            
            if st.button("次へ ▶", disabled=next_disabled, use_container_width=True):
                navigate_next()
        
        with col3:
            if st.session_state.survey_history:
                # 有効なアンケートのみをカウント
                valid_surveys = 0
                current_valid_index = 0
                
                for i, survey in enumerate(st.session_state.survey_history):
                    survey_dict = asdict(survey)
                    is_valid, _ = is_survey_data_valid(survey_dict)
                    
                    if survey.submitted or is_valid:
                        valid_surveys += 1
                        if i <= st.session_state.current_index:
                            current_valid_index = valid_surveys
                
                if valid_surveys > 0:
                    st.info(f"📝 アンケート {current_valid_index}/{valid_surveys}")
                else:
                    st.info("📝 新規アンケート")
            else:
                st.info("📝 新規アンケート")
        
        with col4:
            if st.button("🆕 新規作成", type="primary", use_container_width=True):
                create_new_survey()
        
        with col5:
            # 管理者用エクスポート
            if st.session_state.all_submissions:
                df = pd.DataFrame(st.session_state.all_submissions)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 データ出力",
                    data=csv.encode('utf-8-sig'),
                    file_name=f"survey_{get_jst_now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
    
        # アンケートフォーム
        if not st.session_state.survey_history:
            st.markdown("### 👆 上の「新規作成」ボタンをクリックしてアンケートを開始してください")
        else:
            render_survey_form()
    
    with right_col:
        render_info_sidebar()

def render_survey_form():
    """アンケートフォームを描画"""
    current_survey = st.session_state.survey_history[st.session_state.current_index]
    
    # 編集モードまたは未送信の場合
    if st.session_state.editing_mode or not current_survey.submitted:
        render_survey_input(current_survey)
    else:
        render_submitted_survey(current_survey)

def check_required_fields(survey_data):
    """必須項目のチェックと警告メッセージを生成"""
    missing_fields = []
    warnings = []
    
    # 基本情報の必須チェック
    if not survey_data.get("grade"):
        missing_fields.append("学年")
    if not survey_data.get("gender"):
        missing_fields.append("性別") 
    if not survey_data.get("area"):
        missing_fields.append("地域")
    
    # 質問項目の最低1つ回答チェック
    question_fields = ["triggers", "decision_factors", "education_attractions", "expectations", "info_sources"]
    has_answers = any(survey_data.get(field) and len(survey_data[field]) > 0 for field in question_fields)
    
    if not has_answers:
        missing_fields.append("質問項目（1〜5番）のうち最低1つ")
    
    return missing_fields, len(missing_fields) == 0

def render_survey_input(current_survey):
    """アンケート入力フォームを描画"""
    # 必須項目の説明を追加
    st.info("🔴 は必須項目です。質問項目（1〜5番）は最低1つの回答が必要です。")
    
    # 現在の入力状況を表示
    current_data = {
        "grade": current_survey.grade,
        "gender": current_survey.gender,
        "area": current_survey.area,
        "triggers": current_survey.triggers,
        "decision_factors": current_survey.decision_factors,
        "education_attractions": current_survey.education_attractions,
        "expectations": current_survey.expectations,
        "info_sources": current_survey.info_sources
    }
    missing_fields, is_complete = check_required_fields(current_data)
    
    if is_complete:
        st.success("✅ 必須項目はすべて入力済みです。送信可能な状態です。")
    elif missing_fields:
        with st.expander("⚠️ 未入力の必須項目があります", expanded=False):
            for field in missing_fields:
                st.write(f"• {field}")
    
    with st.form("survey_form"):
        st.markdown("### 🔴 基本情報（必須）")
        
        # 学年
        grade_options = [
            "小学1年生", "小学2年生", "小学3年生", "小学4年生", "小学5年生", "小学6年生",
            "中学1年生", "中学2年生", "中学3年生"
        ]
        grade_index = grade_options.index(current_survey.grade) if current_survey.grade in grade_options else 5  # 小学6年生をデフォルト
        grade = st.selectbox("🔴 学年（必須）", grade_options, index=grade_index)
        
        # 性別
        gender_options = ["男子", "女子", "回答しない"]
        gender_index = gender_options.index(current_survey.gender) if current_survey.gender in gender_options else 0
        gender = st.radio("🔴 性別（必須）", gender_options, index=gender_index)
        
        # 地域
        area_options = [
            "東京都 江東区", "東京都 江戸川区", "東京都 墨田区", "東京都 足立区", 
            "東京都 葛飾区", "東京都 中央区", "東京都 台東区", "東京都 荒川区",
            "東京都 その他23区", "千葉県 船橋市", "千葉県 市川市", "千葉県 浦安市",
            "千葉県 その他市町村", "埼玉県", "神奈川県", "その他"
        ]
        area_index = area_options.index(current_survey.area) if current_survey.area in area_options else 0
        area = st.selectbox("🔴 お住まいの地域（必須）", area_options, index=area_index)
        
        st.markdown("### 🔴 1. 学校を知ったきっかけ（複数選択可・1〜5番のうち最低1つ必須）")
        trigger_items = [
            "学校説明会・体験授業への参加",
            "文化祭（櫻墨祭）への来校",
            "YouTube・Instagram等のSNS配信",
            "在校生・卒業生からの紹介",
            "塾・学校の先生からの推薦",
            "家族・親戚が日大系列の出身",
            "友人・知人の子どもが在籍",
            "学校案内パンフレット",
            "通学途中で学校を見かけて",
            "その他（きっかけ）"
        ]
        triggers = []
        for item in trigger_items:
            if st.checkbox(item, value=item in current_survey.triggers, key=f"trigger_{item}"):
                triggers.append(item)
        
        st.markdown("### 2. 受験の決め手となった要因（複数選択可）")
        decision_factor_items = [
            "日本大学への内部進学率の高さ",
            "中高一貫教育（6年間）のカリキュラム",
            "先生と生徒の距離が近い校風",
            "通学の利便性（駅近・自宅から近い）",
            "大学付属校のメリット（受験に追われない学校生活）",
            "高大連携教育（大学の授業体験等）",
            "生徒の雰囲気・学校の活気",
            "部活動の充実（特定の部活動への入部希望）",
            "国際理解教育・語学研修プログラム",
            "進路指導・学習サポートの充実",
            "校訓「真・健・和」への共感",
            "文武両道の実現が可能",
            "その他（決め手）"
        ]
        decision_factors = []
        for item in decision_factor_items:
            if st.checkbox(item, value=item in current_survey.decision_factors, key=f"decision_{item}"):
                decision_factors.append(item)
        
        st.markdown("### 3. 特に魅力を感じた教育内容（複数選択可）")
        education_items = [
            "習熟度別クラス編成",
            "日本大学の各学部体験授業",
            "オーストラリア語学研修",
            "イングリッシュキャンプ",
            "探究型学習",
            "きめ細やかな個別指導",
            "基礎学力重視の教育方針",
            "自立した人間を育てる教育理念",
            "その他（教育内容）"
        ]
        education_attractions = []
        for item in education_items:
            if st.checkbox(item, value=item in current_survey.education_attractions, key=f"edu_{item}"):
                education_attractions.append(item)
        
        st.markdown("### 4. 入学後に期待すること（複数選択可）")
        expectation_items = [
            "希望の部活動での活動",
            "日本大学への進学",
            "他大学への進学準備",
            "充実した学校行事への参加",
            "友人との絆づくり",
            "将来の夢・目標の発見",
            "グローバルな視野の獲得",
            "学業と部活動の両立",
            "その他（期待）"
        ]
        expectations = []
        for item in expectation_items:
            if st.checkbox(item, value=item in current_survey.expectations, key=f"exp_{item}"):
                expectations.append(item)
        
        st.markdown("### 5. 情報収集で役立ったもの（複数選択可）")
        info_items = [
            "学校説明会ライブ配信（YouTube）",
            "Daily News（毎日の配信）",
            "Instagram投稿",
            "来校型学校体験会",
            "文化祭での在校生との交流",
            "個別相談・学校見学",
            "在校生・卒業生の話",
            "学校パンフレット・ホームページ",
            "その他（情報源）"
        ]
        info_sources = []
        for item in info_items:
            if st.checkbox(item, value=item in current_survey.info_sources, key=f"info_{item}"):
                info_sources.append(item)
        
        # ボタン
        col1, col2 = st.columns(2)
        with col1:
            save_button = st.form_submit_button("💾 一時保存", use_container_width=True)
        with col2:
            submit_button = st.form_submit_button("✅ 確定して送信", type="primary", use_container_width=True)
        
        if save_button or submit_button:
            # 会場情報を取得
            venue_name = get_venue_info()
            
            # データを保存
            survey_data = {
                "venue": venue_name,  # 会場情報を自動追加
                "grade": grade,
                "gender": gender,
                "area": area,
                "triggers": triggers,
                "decision_factors": decision_factors,
                "education_attractions": education_attractions,
                "expectations": expectations,
                "info_sources": info_sources
            }
            save_current_survey(survey_data)
            
            # 必須項目のチェック
            missing_fields, is_complete = check_required_fields(survey_data)
            
            if save_button:
                # 一時保存時に詳細な状態表示
                if is_complete:
                    st.success("💾 一時保存しました！データは送信可能な状態です。")
                else:
                    st.info("💾 一時保存しました。")
                    if missing_fields:
                        st.warning(f"⚠️ 送信には以下の項目が必要です：{', '.join(missing_fields)}")
            
            if submit_button:
                if not is_complete:
                    st.error("❌ 送信できません。以下の必須項目を入力してください：")
                    for field in missing_fields:
                        st.error(f"  • {field}")
                else:
                    # 既存データの再送信の場合、タイムスタンプを更新
                    if current_survey.submitted:
                        st.info("📝 既存データを更新して再送信します")
                        current_survey.timestamp = get_jst_now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    success = submit_survey()
                    if success:
                        st.success("✅ アンケートを送信しました！ご協力ありがとうございました。")
                        st.balloons()
                        # 少し待ってから画面をリフレッシュ
                        time.sleep(1)
            
            st.rerun()

def render_submitted_survey(current_survey):
    """送信済みアンケートの表示"""
    st.success(f"✅ このアンケートは送信済みです（送信日時: {current_survey.timestamp}）")
    
    # ID情報の表示（デバッグ用）
    if hasattr(current_survey, 'id'):
        st.caption(f"📄 アンケートID: {current_survey.id}")
    
    # 送信済みデータの表示
    with st.expander("📋 送信内容を確認", expanded=True):
        # 会場情報があれば表示
        if hasattr(current_survey, 'venue') and current_survey.venue:
            st.write(f"**会場:** {current_survey.venue}")
        st.write(f"**学年:** {current_survey.grade}")
        st.write(f"**性別:** {current_survey.gender}")
        st.write(f"**地域:** {current_survey.area}")
        st.write(f"**きっかけ:** {', '.join(current_survey.triggers)}")
        st.write(f"**決め手:** {', '.join(current_survey.decision_factors)}")
        st.write(f"**教育内容:** {', '.join(current_survey.education_attractions)}")
        st.write(f"**期待:** {', '.join(current_survey.expectations)}")
        st.write(f"**情報源:** {', '.join(current_survey.info_sources)}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 このアンケートを編集", use_container_width=True):
            st.session_state.editing_mode = True
            st.rerun()
    with col2:
        if st.button("🔄 Google Sheetsで確認", use_container_width=True):
            # Google Sheetsのリンクを表示（可能な場合）
            try:
                spreadsheet_name = st.secrets["google_sheets"]["spreadsheet_name"]
                st.info(f"📊 Google Sheets: {spreadsheet_name} で確認してください")
            except:
                st.info("📊 Google Sheetsで確認してください")

def render_info_sidebar():
    """右側の情報リンクサイドバーを描画"""
    st.markdown("### 📚 日大一FAQ")
    
    st.markdown("#### 🎓 入試について")
    if st.button("📄 昨年度の入試要項", use_container_width=True):
        st.session_state.show_admission_guide = True
        st.rerun()
    if st.button("📊 入試概要・合格最低点", use_container_width=True):
        st.session_state.show_exam_results = True
        st.rerun()
    if st.button("📈 受験生動向データ", use_container_width=True):
        st.session_state.show_exam_data = True
        st.rerun()
    
    st.markdown("#### 🏫 学校生活について")
    st.markdown("""
    <a href="https://ckdasd5e7s5fktfua5bgyy.streamlit.app/" target="_blank" style="text-decoration: none;">
        <div style="
            background-color: #ff4b4b;
            color: white;
            padding: 0.5rem 0.75rem;
            border-radius: 0.5rem;
            text-align: center;
            font-weight: 600;
            border: 1px solid transparent;
            cursor: pointer;
            transition: all 0.2s;
            margin: 0.25rem 0;
        " onmouseover="this.style.backgroundColor='#ff2b2b'" onmouseout="this.style.backgroundColor='#ff4b4b'">
            🏃 部活動一覧
        </div>
    </a>
    """, unsafe_allow_html=True)
    # カレンダー表示
    if st.button("📅 学校行事・年間予定を見る", key="calendar_button"):
        st.switch_page("calendar_page.py")
    
    # API有効化までの代替リンク
    st.markdown("📅 [学校行事・年間予定（外部リンク）](https://calendar.google.com/calendar/embed?src=nichidai1.haishin%40gmail.com&ctz=Asia%2FTokyo)", unsafe_allow_html=True)
    
    st.markdown("#### 📖 進路について")
    st.markdown("- [日本大学進学実績](placeholder)")
    st.markdown("- [他大学進学実績](placeholder)")
    
    st.markdown("#### 💰 学費について")
    st.markdown("- [1年次学費](placeholder)")
    st.markdown("- [学用品価格](placeholder)")
    
    st.markdown("#### 🚇 通学・アクセスについて")
    st.markdown("- [在校生最寄駅](placeholder)")
    st.markdown("- [在校生乗り換え回数](placeholder)")
    st.markdown("- [受験生通学区域](placeholder)")
    
    st.markdown("---")
    st.info("💡 各項目をクリックすると詳細ページが開きます（準備中）")

def show_admission_guide_page():
    """募集要項ページを表示"""
    from admission_guide_data import ADMISSION_GUIDE_HTML
    
    # ヘッダー
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📄 令和7年度 生徒募集要項")
    with col2:
        if st.button("⬅ アンケートに戻る", use_container_width=True):
            st.session_state.show_admission_guide = False
            st.rerun()
    
    # HTMLコンテンツを表示
    st.components.v1.html(ADMISSION_GUIDE_HTML, height=800, scrolling=True)

def show_exam_results_page():
    """合格最低点ページを表示"""
    from exam_results_data import EXAM_RESULTS_HTML
    
    # ヘッダー
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 2025年度 入試結果")
    with col2:
        if st.button("⬅ アンケートに戻る", use_container_width=True):
            st.session_state.show_exam_results = False
            st.rerun()
    
    # HTMLコンテンツを表示
    st.components.v1.html(EXAM_RESULTS_HTML, height=800, scrolling=True)

def show_exam_data_page():
    """受験生動向データページを表示"""
    from exam_data_analysis import EXAM_DATA_HTML
    
    # ヘッダー
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📈 2025年度 受験生動向データ")
    with col2:
        if st.button("⬅ アンケートに戻る", use_container_width=True):
            st.session_state.show_exam_data = False
            st.rerun()
    
    # HTMLコンテンツを表示
    st.components.v1.html(EXAM_DATA_HTML, height=800, scrolling=True)

if __name__ == "__main__":
    main()