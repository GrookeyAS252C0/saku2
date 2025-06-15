import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import calendar as cal

# 日本時間（JST）の設定
JST = timezone(timedelta(hours=+9))

def get_jst_now():
    """現在の日本時間を取得"""
    return datetime.now(JST)

@st.cache_data(ttl=3600)  # 1時間キャッシュ
def get_calendar_events():
    """Google Calendarからイベントを取得"""
    try:
        # 認証情報の設定
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
            maxResults=100,
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
                date_str = start_jst.strftime('%Y-%m-%d')
                time_str = f"{start_jst.strftime('%H:%M')} - {end_jst.strftime('%H:%M')}"
                day_num = start_jst.day
                month_year = start_jst.strftime('%Y年%m月')
            else:  # 終日イベント
                start_dt = datetime.fromisoformat(start + 'T00:00:00')
                date_str = start_dt.strftime('%Y-%m-%d')
                time_str = "終日"
                day_num = start_dt.day
                month_year = start_dt.strftime('%Y年%m月')
            
            event_data.append({
                'title': event.get('summary', '無題'),
                'date': date_str,
                'time': time_str,
                'description': event.get('description', ''),
                'start_datetime': start_dt,
                'day': day_num,
                'month_year': month_year,
                'location': event.get('location', '')
            })
        
        return pd.DataFrame(event_data)
    
    except Exception as e:
        st.error(f"カレンダーの読み込みに失敗しました: {str(e)}")
        return pd.DataFrame()

def create_calendar_grid(events_df, year, month):
    """月間カレンダーグリッドを作成"""
    # 月の情報を取得
    month_calendar = cal.monthcalendar(year, month)
    month_name = f"{year}年{month:02d}月"
    
    # その月のイベントを取得
    month_events = events_df[events_df['month_year'] == month_name]
    
    # 日付ごとのイベントを辞書化
    events_by_day = {}
    for _, event in month_events.iterrows():
        day = event['day']
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(event)
    
    st.markdown(f"## 📅 {month_name}")
    
    # 曜日ヘッダー
    weekdays = ['月', '火', '水', '木', '金', '土', '日']
    cols = st.columns(7)
    for i, weekday in enumerate(weekdays):
        with cols[i]:
            st.markdown(f"**{weekday}**")
    
    # カレンダーグリッドを作成
    for week in month_calendar:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.markdown("")  # 空の日
                else:
                    # 日付表示
                    day_events = events_by_day.get(day, [])
                    
                    if day_events:
                        # イベントがある日は強調表示
                        st.markdown(f"**{day}**")
                        for event in day_events[:2]:  # 最大2つまで表示
                            event_title = event['title']
                            if len(event_title) > 8:
                                event_title = event_title[:8] + "..."
                            st.markdown(f"<small>🎯 {event_title}</small>", unsafe_allow_html=True)
                        if len(day_events) > 2:
                            st.markdown(f"<small>他{len(day_events)-2}件</small>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"{day}")

def display_monthly_events(events_df, year, month):
    """月間イベント詳細リストを表示"""
    month_name = f"{year}年{month:02d}月"
    month_events = events_df[events_df['month_year'] == month_name].sort_values('start_datetime')
    
    if not month_events.empty:
        st.markdown(f"### 📋 {month_name}の予定詳細")
        
        for _, event in month_events.iterrows():
            with st.expander(f"📅 {event['day']}日: {event['title']}"):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**イベント名:** {event['title']}")
                    if event['description']:
                        st.markdown(f"**詳細:** {event['description']}")
                    if event['location']:
                        st.markdown(f"**場所:** {event['location']}")
                with col2:
                    st.markdown(f"**日付:** {event['date']}")
                    st.markdown(f"**時間:** {event['time']}")
    else:
        st.info(f"{month_name}には予定されているイベントがありません。")

def main():
    """カレンダーページのメイン関数"""
    st.set_page_config(
        page_title="日本大学第一中学・高等学校 年間予定",
        page_icon="📅",
        layout="wide"
    )
    
    st.title("📅 日本大学第一中学・高等学校 年間予定")
    
    # データ取得
    events_df = get_calendar_events()
    
    if events_df.empty:
        st.error("カレンダーデータを取得できませんでした。")
        return
    
    # サイドバーで月選択
    with st.sidebar:
        st.markdown("## 📅 月選択")
        
        current_date = get_jst_now()
        
        # 年選択
        available_years = sorted(events_df['start_datetime'].dt.year.unique())
        if not available_years:
            available_years = [current_date.year]
        
        selected_year = st.selectbox(
            "年を選択",
            options=available_years,
            index=available_years.index(current_date.year) if current_date.year in available_years else 0
        )
        
        # 月選択
        selected_month = st.selectbox(
            "月を選択",
            options=list(range(1, 13)),
            index=current_date.month - 1,
            format_func=lambda x: f"{x}月"
        )
        
        # 表示モード選択
        display_mode = st.radio(
            "表示モード",
            ["カレンダー表示", "リスト表示", "両方表示"],
            index=2
        )
    
    # メインコンテンツ
    if display_mode in ["カレンダー表示", "両方表示"]:
        create_calendar_grid(events_df, selected_year, selected_month)
        
        if display_mode == "両方表示":
            st.divider()
    
    if display_mode in ["リスト表示", "両方表示"]:
        display_monthly_events(events_df, selected_year, selected_month)
    
    # 戻るボタン
    st.markdown("---")
    if st.button("🏠 メインページに戻る"):
        st.switch_page("app.py")

if __name__ == "__main__":
    main()