import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import io
import gspread
from google.oauth2.service_account import Credentials

# ページ設定
st.set_page_config(
    page_title="アンケート管理画面",
    page_icon="📊",
    layout="wide"
)

def authenticate_admin():
    """管理者認証"""
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        password = st.text_input("管理者パスワードを入力してください", type="password")
        if st.button("ログイン"):
            # Streamlit Cloudのシークレットから読み込み
            try:
                correct_password = st.secrets["admin"]["password"]
            except:
                correct_password = "admin123"  # ローカル開発用
            
            if password == correct_password:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("パスワードが正しくありません")
        return False
    return True

def load_data_from_google_sheets():
    """Google Sheetsからデータを読み込む（Streamlit Cloud対応）"""
    try:
        # Streamlit CloudのシークレットからGoogle Sheets認証情報を取得
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(credentials)
        
        # スプレッドシートを開く
        sh = gc.open(st.secrets["google_sheets"]["spreadsheet_name"])
        worksheet = sh.sheet1
        
        # データを取得
        data = worksheet.get_all_records()
        if data:
            return pd.DataFrame(data)
    except:
        pass
    
    return pd.DataFrame()

def load_session_data():
    """セッションデータを読み込む"""
    if 'saved_data' in st.session_state and st.session_state.saved_data:
        return pd.DataFrame(st.session_state.saved_data)
    elif 'all_submissions' in st.session_state and st.session_state.all_submissions:
        return pd.DataFrame(st.session_state.all_submissions)
    else:
        return pd.DataFrame()

def main():
    st.title("📊 アンケート管理画面")
    
    # 認証チェック
    if not authenticate_admin():
        return
    
    # データソース選択
    data_source = st.sidebar.radio(
        "データソース",
        ["セッションデータ", "Google Sheets", "CSVアップロード"]
    )
    
    df = pd.DataFrame()
    
    if data_source == "セッションデータ":
        df = load_session_data()
    elif data_source == "Google Sheets":
        df = load_data_from_google_sheets()
    else:  # CSVアップロード
        uploaded_file = st.file_uploader("CSVファイルをアップロード", type=['csv'])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    
    if df.empty:
        st.warning("データがありません。アンケートアプリでデータを収集するか、CSVファイルをアップロードしてください。")
        return
    
    # データ前処理
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # サイドバーフィルタ
    st.sidebar.header("フィルタリング")
    
    # 日付フィルタ
    if 'timestamp' in df.columns and not df['timestamp'].isna().all():
        date_range = st.sidebar.date_input(
            "期間",
            value=(df['timestamp'].min().date(), df['timestamp'].max().date()),
            max_value=datetime.now().date()
        )
        if len(date_range) == 2:
            mask = (df['timestamp'].dt.date >= date_range[0]) & (df['timestamp'].dt.date <= date_range[1])
            df = df[mask]
    
    # 学年フィルタ
    if 'grade' in df.columns:
        unique_grades = df['grade'].dropna().unique()
        selected_grades = st.sidebar.multiselect("学年", unique_grades)
        if selected_grades:
            df = df[df['grade'].isin(selected_grades)]
    
    # 地域フィルタ
    if 'area' in df.columns:
        unique_areas = df['area'].dropna().unique()
        selected_areas = st.sidebar.multiselect("地域", unique_areas)
        if selected_areas:
            df = df[df['area'].isin(selected_areas)]
    
    # 基本統計
    st.header("📈 基本統計")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("総回答数", len(df))
    
    with col2:
        if 'gender' in df.columns:
            male_count = len(df[df['gender'] == '男子'])
            st.metric("男子", male_count)
    
    with col3:
        if 'gender' in df.columns:
            female_count = len(df[df['gender'] == '女子'])
            st.metric("女子", female_count)
    
    with col4:
        if 'timestamp' in df.columns and not df['timestamp'].isna().all():
            latest = df['timestamp'].max()
            if pd.notna(latest):
                st.metric("最新回答", latest.strftime('%m/%d %H:%M'))
    
    # タブ表示
    st.header("📊 詳細分析")
    tabs = st.tabs(["基本情報", "きっかけ", "決め手", "生データ"])
    
    with tabs[0]:  # 基本情報
        col1, col2 = st.columns(2)
        
        with col1:
            if 'grade' in df.columns:
                grade_counts = df['grade'].value_counts()
                fig = px.bar(
                    x=grade_counts.values, 
                    y=grade_counts.index, 
                    orientation='h',
                    title="学年分布",
                    labels={'x': '人数', 'y': '学年'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'area' in df.columns:
                area_counts = df['area'].value_counts().head(10)
                fig = px.pie(
                    values=area_counts.values, 
                    names=area_counts.index, 
                    title="地域分布（上位10地域）"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        if 'gender' in df.columns:
            gender_counts = df['gender'].value_counts()
            fig = px.pie(
                values=gender_counts.values,
                names=gender_counts.index,
                title="性別分布",
                color_discrete_map={'男子': '#3498db', '女子': '#e74c3c', '回答しない': '#95a5a6'}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 複数選択項目の分析関数
    def analyze_multiple_choice(column_name, title):
        if column_name in df.columns:
            items = []
            for value in df[column_name]:
                if isinstance(value, str):
                    try:
                        parsed = eval(value)
                        if isinstance(parsed, list):
                            items.extend(parsed)
                    except:
                        items.append(value)
                elif isinstance(value, list):
                    items.extend(value)
            
            if items:
                item_counts = pd.Series(items).value_counts()
                fig = px.bar(
                    x=item_counts.values,
                    y=item_counts.index,
                    orientation='h',
                    title=title,
                    labels={'x': '回答数', 'y': ''}
                )
                fig.update_layout(height=max(400, len(item_counts) * 40))
                st.plotly_chart(fig, use_container_width=True)
    
    with tabs[1]:  # きっかけ
        analyze_multiple_choice('triggers', '学校を知ったきっかけ')
    
    with tabs[2]:  # 決め手
        analyze_multiple_choice('decision_factors', '受験の決め手')
    
    with tabs[3]:  # 生データ
        st.subheader("アンケート回答一覧")
        
        # データ表示用に整形
        display_df = df.copy()
        
        # リスト型のカラムを文字列に変換
        list_columns = ['triggers', 'decision_factors', 'education_attractions', 'expectations', 'info_sources']
        for col in list_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(
                    lambda x: ', '.join(x) if isinstance(x, list) else str(x)
                )
        
        # タイムスタンプを文字列に変換
        if 'timestamp' in display_df.columns:
            display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(display_df, use_container_width=True, height=400)
    
    # エクスポート機能
    st.header("📥 データエクスポート")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV形式
        csv = display_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📄 CSVダウンロード",
            data=csv.encode('utf-8-sig'),
            file_name=f"survey_results_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Excel形式
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            display_df.to_excel(writer, sheet_name='アンケート結果', index=False)
            
            # 基本統計シート
            stats_df = pd.DataFrame({
                '項目': ['総回答数', '男子', '女子', '回答しない'],
                '人数': [
                    len(df),
                    len(df[df['gender'] == '男子']) if 'gender' in df.columns else 0,
                    len(df[df['gender'] == '女子']) if 'gender' in df.columns else 0,
                    len(df[df['gender'] == '回答しない']) if 'gender' in df.columns else 0
                ]
            })
            stats_df.to_excel(writer, sheet_name='基本統計', index=False)
        
        st.download_button(
            label="📊 Excelダウンロード",
            data=buffer.getvalue(),
            file_name=f"survey_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        # ログアウト
        if st.button("🚪 ログアウト", type="secondary"):
            st.session_state.admin_authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()