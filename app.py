import streamlit as st
import pandas as pd
from datetime import datetime
import json
import uuid
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import gspread
from google.oauth2.service_account import Credentials
import time

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
    venue_name = get_venue_info()  # URLパラメータから会場を取得
    
    new_survey = SurveyResponse(
        id=str(uuid.uuid4()),
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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

def submit_survey():
    """アンケートを確定して送信"""
    if st.session_state.current_index >= 0:
        current_survey = st.session_state.survey_history[st.session_state.current_index]
        current_survey.submitted = True
        current_survey.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 全体の送信リストに追加
        st.session_state.all_submissions.append(asdict(current_survey))
        
        # CSVに保存（Streamlit Cloud対応）
        save_to_cloud_storage(asdict(current_survey))
        
        st.session_state.editing_mode = False

def save_to_google_sheets(data: Dict[str, Any]):
    """Google Sheetsにデータを保存"""
    try:
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
        
        # ヘッダーを設定（初回のみ、または古いフォーマットの場合は更新）
        try:
            headers = worksheet.row_values(1)
            expected_headers = [
                "ID", "送信日時", "会場", "学年", "性別", "地域",
                "きっかけ", "決め手", "教育内容", "期待", "情報源"
            ]
            
            # ヘッダーがない場合は新規作成
            if not headers:
                worksheet.insert_row(expected_headers, 1)
                st.info("✅ Google Sheetsにヘッダーを作成しました")
            
            # 古いフォーマット（会場列がない）の場合は「会場」列を挿入
            elif "会場" not in headers:
                # 「送信日時」の後（3列目）に「会場」を挿入
                worksheet.insert_cols(3, 1)
                worksheet.update_cell(1, 3, "会場")
                st.info("✅ Google Sheetsに「会場」列を追加しました")
                
                # 既存データには「メイン会場」を設定
                if len(worksheet.get_all_values()) > 1:  # データがある場合
                    data_rows = len(worksheet.get_all_values())
                    for row in range(2, data_rows + 1):  # 2行目以降（データ行）
                        if not worksheet.cell(row, 3).value:  # 会場列が空の場合
                            worksheet.update_cell(row, 3, "メイン会場")
                    st.info("✅ 既存データに「メイン会場」を設定しました")
                    
        except Exception as e:
            st.error(f"ヘッダー設定エラー: {e}")
            return False
        
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
    
    # ダウンロード用のデータを準備
    df = pd.DataFrame(st.session_state.saved_data)
    st.session_state.export_data = df

def navigate_previous():
    """前のアンケートに戻る"""
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1
        st.session_state.editing_mode = True

def navigate_next():
    """次のアンケートに進む"""
    if st.session_state.current_index < len(st.session_state.survey_history) - 1:
        st.session_state.current_index += 1
        st.session_state.editing_mode = True

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

def main():
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
            if st.button("◀ 前へ", disabled=st.session_state.current_index <= 0, use_container_width=True):
                navigate_previous()
        
        with col2:
            if st.button("次へ ▶", disabled=st.session_state.current_index >= len(st.session_state.survey_history) - 1, use_container_width=True):
                navigate_next()
        
        with col3:
            if st.session_state.survey_history:
                current = st.session_state.current_index + 1
                total = len(st.session_state.survey_history)
                st.info(f"📝 アンケート {current}/{total}")
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
                    file_name=f"survey_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
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

def render_survey_input(current_survey):
    """アンケート入力フォームを描画"""
    with st.form("survey_form"):
        st.markdown("### 基本情報")
        
        # 学年
        grade_options = [
            "小学1年生", "小学2年生", "小学3年生", "小学4年生", "小学5年生", "小学6年生",
            "中学1年生", "中学2年生", "中学3年生"
        ]
        grade_index = grade_options.index(current_survey.grade) if current_survey.grade in grade_options else 5  # 小学6年生をデフォルト
        grade = st.selectbox("学年", grade_options, index=grade_index)
        
        # 性別
        gender_options = ["男子", "女子", "回答しない"]
        gender_index = gender_options.index(current_survey.gender) if current_survey.gender in gender_options else 0
        gender = st.radio("性別", gender_options, index=gender_index)
        
        # 地域
        area_options = [
            "東京都 江東区", "東京都 江戸川区", "東京都 墨田区", "東京都 足立区", 
            "東京都 葛飾区", "東京都 中央区", "東京都 台東区", "東京都 荒川区",
            "東京都 その他23区", "千葉県 船橋市", "千葉県 市川市", "千葉県 浦安市",
            "千葉県 その他市町村", "埼玉県", "神奈川県", "その他"
        ]
        area_index = area_options.index(current_survey.area) if current_survey.area in area_options else 0
        area = st.selectbox("お住まいの地域", area_options, index=area_index)
        
        st.markdown("### 1. 学校を知ったきっかけ（複数選択可）")
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
            
            if submit_button:
                submit_survey()
                st.balloons()
                # 少し待ってから画面をリフレッシュ
                time.sleep(1)
            else:
                st.success("💾 一時保存しました")
            
            st.rerun()

def render_submitted_survey(current_survey):
    """送信済みアンケートの表示"""
    st.success(f"✅ このアンケートは送信済みです（送信日時: {current_survey.timestamp}）")
    
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
    
    if st.button("📝 このアンケートを編集", use_container_width=True):
        st.session_state.editing_mode = True
        st.rerun()

def render_info_sidebar():
    """右側の情報リンクサイドバーを描画"""
    st.markdown("### 📚 よくある質問・学校情報")
    
    # よくある質問のカテゴリ
    st.markdown("#### 🎓 入試・受験について")
    st.markdown("- [入試要項・日程](placeholder)")
    st.markdown("- [偏差値・合格ライン](placeholder)")
    st.markdown("- [過去問・入試対策](placeholder)")
    st.markdown("- [特待生制度](placeholder)")
    
    st.markdown("#### 🏫 学校生活について")
    st.markdown("- [制服・校則](placeholder)")
    st.markdown("- [部活動一覧](placeholder)")
    st.markdown("- [学校行事・年間予定](placeholder)")
    st.markdown("- [1日のスケジュール](placeholder)")
    
    st.markdown("#### 📖 カリキュラム・進路")
    st.markdown("- [中高一貫カリキュラム](placeholder)")
    st.markdown("- [日本大学進学実績](placeholder)")
    st.markdown("- [他大学進学実績](placeholder)")
    st.markdown("- [進路指導・サポート](placeholder)")
    
    st.markdown("#### 🌏 国際教育・語学")
    st.markdown("- [オーストラリア語学研修](placeholder)")
    st.markdown("- [イングリッシュキャンプ](placeholder)")
    st.markdown("- [英語教育の特色](placeholder)")
    st.markdown("- [海外大学進学サポート](placeholder)")
    
    st.markdown("#### 💰 学費・奨学金")
    st.markdown("- [学費一覧](placeholder)")
    st.markdown("- [奨学金制度](placeholder)")
    st.markdown("- [就学支援金](placeholder)")
    st.markdown("- [その他費用](placeholder)")
    
    st.markdown("#### 🚇 通学・アクセス")
    st.markdown("- [アクセス・最寄り駅](placeholder)")
    st.markdown("- [スクールバス](placeholder)")
    st.markdown("- [自転車通学](placeholder)")
    st.markdown("- [周辺環境](placeholder)")
    
    st.markdown("---")
    st.info("💡 各項目をクリックすると詳細ページが開きます（準備中）")

if __name__ == "__main__":
    main()