# station_analysis_data.py
STATION_ANALYSIS_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本大学第一中学校・高等学校 通学時間分析</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Hiragino Sans', 'Yu Gothic', 'Meiryo', sans-serif;
            line-height: 1.7;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .header h1 {
            font-size: 2.8rem;
            background: linear-gradient(45deg, #ff6b35, #2196f3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header .subtitle {
            font-size: 1.3rem;
            color: #666;
            margin-bottom: 20px;
        }

        .notice {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            font-size: 0.95rem;
            color: #856404;
        }

        .nav-tabs {
            display: flex;
            gap: 0;
            margin-bottom: 30px;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        .nav-tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            color: white;
            border: none;
        }

        .nav-tab.junior {
            background: linear-gradient(135deg, #ff6b35, #f7931e);
        }

        .nav-tab.senior {
            background: linear-gradient(135deg, #2196f3, #21cbf3);
        }

        .nav-tab:hover {
            transform: translateY(-2px);
        }

        .nav-tab.active {
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            transform: translateY(-3px);
        }

        .content-section {
            display: none;
        }

        .content-section.active {
            display: block;
        }

        /* Junior High School Styles (Orange) */
        .junior .stats-overview {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border-top: 5px solid #ff6b35;
        }

        .junior .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }

        .junior .stat-card {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #ff6b35, #f7931e);
            border-radius: 15px;
            color: white;
            transform: translateY(0);
            transition: transform 0.3s ease;
        }

        .junior .stat-card:hover {
            transform: translateY(-5px);
        }

        .junior .zone-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
            border-left: 5px solid #ff6b35;
            margin-bottom: 25px;
        }

        .junior .zone-0-20 .zone-icon { background: linear-gradient(135deg, #ff6b35, #ff8e53); }
        .junior .zone-21-40 .zone-icon { background: linear-gradient(135deg, #f7931e, #ffad33); }
        .junior .zone-41-60 .zone-icon { background: linear-gradient(135deg, #ff6347, #ff7f50); }
        .junior .zone-61plus .zone-icon { background: linear-gradient(135deg, #ff4500, #ff6347); }

        .junior .zone-percentage {
            background: linear-gradient(135deg, #ff6b35, #f7931e);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 0.9rem;
        }

        .junior .zone-stations {
            background: #fff5f0;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #ff6b35;
        }

        .junior .zone-stations h4 {
            color: #ff6b35;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .junior .merit-box {
            background: #fff5f0;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #ff6b35;
        }

        .junior .merit-box h4 {
            color: #ff6b35;
            margin-bottom: 10px;
        }

        .junior .student-type-box {
            background: #fff5f0;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #f7931e;
        }

        .junior .student-type-box h4 {
            color: #f7931e;
            margin-bottom: 10px;
        }

        .junior .advice-section, .junior .message-section {
            background: linear-gradient(135deg, #ff6b35, #f7931e);
            color: white;
            border-radius: 20px;
            padding: 40px;
            margin-top: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        /* Senior High School Styles (Blue) */
        .senior .intro-section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border-top: 5px solid #2196f3;
        }

        .senior .intro-section h2 {
            color: #2196f3;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }

        .senior .zone-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
            border-left: 5px solid #2196f3;
            margin-bottom: 25px;
        }

        .senior .zone-very-close .zone-icon { background: linear-gradient(135deg, #2196f3, #42a5f5); }
        .senior .zone-close .zone-icon { background: linear-gradient(135deg, #1976d2, #2196f3); }
        .senior .zone-average .zone-icon { background: linear-gradient(135deg, #1565c0, #1976d2); }
        .senior .zone-far .zone-icon { background: linear-gradient(135deg, #0d47a1, #1565c0); }
        .senior .zone-very-far .zone-icon { background: linear-gradient(135deg, #0277bd, #0288d1); }

        .senior .zone-time {
            background: linear-gradient(135deg, #2196f3, #1976d2);
            color: white;
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 0.9rem;
        }

        .senior .zone-stations {
            background: #f3f9ff;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #2196f3;
        }

        .senior .zone-stations h4 {
            color: #2196f3;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .senior .points-section, .senior .time-guide, .senior .summary-section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-top: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border-top: 5px solid #2196f3;
        }

        .senior .summary-section {
            background: linear-gradient(135deg, #2196f3, #1976d2);
            color: white;
            border-top: none;
        }

        .senior .point-card {
            background: #f3f9ff;
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #2196f3;
            margin-bottom: 20px;
        }

        .senior .point-card h3 {
            color: #2196f3;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }

        .senior .merit-box {
            background: #e8f4fd;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #2196f3;
            margin: 15px 0;
        }

        .senior .merit-box h4 {
            color: #2196f3;
            margin-bottom: 10px;
        }

        .senior .area-box {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #1976d2;
            margin: 15px 0;
        }

        .senior .area-box h4 {
            color: #1976d2;
            margin-bottom: 10px;
        }

        .senior .transport-box {
            background: #e1f5fe;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #0288d1;
            margin: 15px 0;
        }

        .senior .transport-box h4 {
            color: #0288d1;
            margin-bottom: 10px;
        }

        .senior .line-tag {
            background: #2196f3;
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            text-align: center;
            font-size: 0.9rem;
            font-weight: bold;
            margin: 5px;
            display: inline-block;
        }

        /* Common Styles */
        .zone-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }

        .zone-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-right: 20px;
            color: white;
            font-weight: bold;
        }

        .zone-title {
            flex: 1;
        }

        .zone-title h3 {
            font-size: 1.4rem;
            margin-bottom: 5px;
            color: #333;
        }

        .stations-list {
            color: #666;
            line-height: 1.6;
        }

        .zone-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }

        .stat-number {
            font-size: 3rem;
            font-weight: bold;
            display: block;
        }

        .stat-label {
            font-size: 1.1rem;
            margin-top: 10px;
        }

        .time-zones {
            display: grid;
            gap: 25px;
            margin-top: 30px;
        }

        .zone-card:hover {
            transform: translateY(-3px);
        }

        .advice-grid, .points-grid {
            display: grid;
            gap: 25px;
            margin-top: 25px;
        }

        .advice-card {
            background: rgba(255, 255, 255, 0.2);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid rgba(255, 255, 255, 0.5);
        }

        .advice-card h3 {
            color: white;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }

        .message-content {
            font-size: 1.1rem;
            line-height: 1.8;
            text-align: left;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            margin-top: 20px;
        }

        .time-guide-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .time-guide-item {
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: white;
        }

        .time-guide-45 {
            background: linear-gradient(135deg, #2196f3, #42a5f5);
        }

        .time-guide-60 {
            background: linear-gradient(135deg, #1976d2, #2196f3);
        }

        .time-guide-60plus {
            background: linear-gradient(135deg, #1565c0, #1976d2);
        }

        .summary-points {
            display: grid;
            gap: 15px;
            margin-top: 20px;
        }

        .summary-point {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid white;
        }

        .transport-lines {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }

        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .nav-tabs {
                flex-direction: column;
            }
            
            .zone-details {
                grid-template-columns: 1fr;
            }
            
            .time-guide-grid {
                grid-template-columns: 1fr;
            }
            
            .transport-lines {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>日本大学第一中学校・高等学校</h1>
            <div class="subtitle">新入生通学時間分析レポート</div>
            <div class="notice">
                ※以下の分析は入力内容に基づくものです。駅名が重複する部分がございます。
            </div>
        </div>

        <div class="nav-tabs">
            <button class="nav-tab junior active" onclick="showSection('junior')">🍊 中学校</button>
            <button class="nav-tab senior" onclick="showSection('senior')">🔵 高等学校</button>
        </div>

        <!-- Junior High School Section -->
        <div id="junior" class="content-section junior active">
            <div class="stats-overview">
                <h2>📊 通学時間の概要</h2>
                <p>当校生徒の通学時間は平均約44分、中央値40分となっています。多くのご家庭が「片道40分程度」の通学圏内から学校を選択されている実態が見えてきます。</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">44</span>
                        <div class="stat-label">平均通学時間（分）</div>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">40</span>
                        <div class="stat-label">中央値（分）</div>
                    </div>
                </div>
            </div>

            <div class="time-zones">
                <div class="zone-card zone-0-20">
                    <div class="zone-header">
                        <div class="zone-icon">🚶</div>
                        <div class="zone-title">
                            <h3>0〜20分：身近な選択</h3>
                        </div>
                        <div class="zone-percentage">10%</div>
                    </div>
                    <div class="zone-content">
                        <div class="zone-stations">
                            <h4>主な通学駅</h4>
                            <div class="stations-list">徒歩圏（8名）、浜町、亀戸、勝どきなど</div>
                        </div>
                        <div class="zone-details">
                            <div class="merit-box">
                                <h4>💡 メリット</h4>
                                <p>時間的余裕、体力温存、課外活動参加のしやすさ</p>
                            </div>
                            <div class="student-type-box">
                                <h4>👥 向いている生徒像</h4>
                                <p>部活動や放課後の学習に積極的に取り組みたい生徒</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="zone-card zone-21-40">
                    <div class="zone-header">
                        <div class="zone-icon">🚃</div>
                        <div class="zone-title">
                            <h3>21〜40分：バランスの良い選択</h3>
                        </div>
                        <div class="zone-percentage">42%</div>
                    </div>
                    <div class="zone-content">
                        <div class="zone-stations">
                            <h4>主な通学駅</h4>
                            <div class="stations-list">豊洲（3名）、新小岩（3名）、船橋（3名）、北千住、南砂町など</div>
                        </div>
                        <div class="zone-details">
                            <div class="merit-box">
                                <h4>💡 メリット</h4>
                                <p>適度な通学時間と学校選択の幅のバランスが取れている</p>
                            </div>
                            <div class="student-type-box">
                                <h4>👥 向いている生徒像</h4>
                                <p>通学時間と学校の教育内容を両立させたい生徒</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="zone-card zone-41-60">
                    <div class="zone-header">
                        <div class="zone-icon">🚄</div>
                        <div class="zone-title">
                            <h3>41〜60分：教育内容重視の選択</h3>
                        </div>
                        <div class="zone-percentage">37%</div>
                    </div>
                    <div class="zone-content">
                        <div class="zone-stations">
                            <h4>主な通学駅</h4>
                            <div class="stations-list">恵比寿（2名）、新小岩（2名）、綾瀬（2名）、船橋競馬場（2名）、南流山（2名）など</div>
                        </div>
                        <div class="zone-details">
                            <div class="merit-box">
                                <h4>💡 メリット</h4>
                                <p>学校の教育方針や特色を優先した選択が可能</p>
                            </div>
                            <div class="student-type-box">
                                <h4>👥 向いている生徒像</h4>
                                <p>通学時間より学校の特色・教育内容を重視する生徒</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="zone-card zone-61plus">
                    <div class="zone-header">
                        <div class="zone-icon">🚅</div>
                        <div class="zone-title">
                            <h3>61分以上：明確な志望理由を持つ長距離通学</h3>
                        </div>
                        <div class="zone-percentage">11%</div>
                    </div>
                    <div class="zone-content">
                        <div class="zone-stations">
                            <h4>主な通学駅</h4>
                            <div class="stations-list">海浜幕張、八幡宿、東所沢、京成臼井、上野毛（90分）など</div>
                        </div>
                        <div class="zone-details">
                            <div class="merit-box">
                                <h4>⚠️ 考慮点</h4>
                                <p>体力面・時間管理の負担大、明確な志望理由が必要</p>
                            </div>
                            <div class="student-type-box">
                                <h4>👥 向いている生徒像</h4>
                                <p>学校の特色に強い魅力を感じ、通学時間よりも教育内容を最優先する生徒</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="advice-section">
                <h2>🎯 学校選びにおける通学時間の考え方</h2>
                <div class="advice-grid">
                    <div class="advice-card">
                        <h3>通学時間と学習効率のバランス</h3>
                        <p>平均通学時間の44分は、多くのご家庭が「通学負担」と「学校選択の幅」のバランスを取った結果と言えます。一般的に、片道60分以内であれば、学習時間・睡眠時間の確保が比較的容易です。</p>
                    </div>
                    <div class="advice-card">
                        <h3>長距離通学を選ぶ場合の考慮点</h3>
                        <p>千葉県や埼玉県の遠方から通学する生徒も一定数存在します。片道70分を超える通学を選択する場合は、以下の点を特に考慮されることをお勧めします：</p>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>本人の体力と時間管理能力</li>
                            <li>通学時間を学習時間として活用できるか</li>
                            <li>教育方針・特色が本人の希望と強く合致しているか</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="message-section">
                <h2>📢 受験生・保護者の皆様へのメッセージ</h2>
                <div class="message-content">
                    <p><strong>複数の学校を比較検討する際は、教育内容だけでなく通学時間も重要な判断材料に</strong>、実際に通学経路を試し、朝の混雑状況や所要時間を体感してみることをお勧めします。</p>
                    
                    <p style="margin-top: 20px;"><strong>長距離通学を検討している場合は</strong>、オープンスクールなどで在校生の体験談を聞くことも参考になります。</p>
                    
                    <p style="margin-top: 20px;">学校選びは、学力や進学実績だけでなく、<strong>6年間の中高一貫教育生活の質を左右する通学環境も重要な要素</strong>です。このデータが皆様の学校選択の一助となれば幸いです。</p>
                </div>
            </div>
        </div>

        <!-- Senior High School Section -->
        <div id="senior" class="content-section senior">
            <div class="intro-section">
                <h2>📍 はじめに</h2>
                <p>日本大学第一高等学校（墨田区）への通学状況を分析したところ、墨田区内の徒歩圏内から千葉県や埼玉県からの長距離通学まで、幅広い地域から生徒が通学していることがわかりました。このレポートでは、通学時間に基づいた地域別の分析と、学校選びのポイントについてまとめました。</p>
            </div>

            <div class="time-zones">
                <div class="zone-card zone-very-close">
                    <div class="zone-header">
                        <div class="zone-icon">🚶</div>
                        <div class="zone-title">
                            <h3>20分以内（非常に近い）</h3>
                        </div>
                        <div class="zone-time">0-20分</div>
                    </div>
                    <div class="zone-stations">
                        <h4>通学可能エリア</h4>
                        <div class="stations-list">
                            <strong>墨田区内：</strong>徒歩10-20分で通学可能<br>
                            <strong>近隣駅：</strong>水天宮前駅（中央区）、錦糸町駅（墨田区）、蔵前駅（台東区）、本所吾妻橋（墨田区）からは20分以内
                        </div>
                    </div>
                </div>

                <div class="zone-card zone-close">
                    <div class="zone-header">
                        <div class="zone-icon">🚃</div>
                        <div class="zone-title">
                            <h3>21-30分（近い）</h3>
                        </div>
                        <div class="zone-time">21-30分</div>
                    </div>
                    <div class="zone-stations">
                        <h4>主な通学駅</h4>
                        <div class="stations-list">
                            豊洲駅、亀戸駅（江東区）、押上駅（墨田区）、清澄白河（江東区）<br>
                            勝どき（中央区）、門前仲町（江東区）、船堀駅（江戸川区）
                        </div>
                    </div>
                </div>

                <div class="zone-card zone-average">
                    <div class="zone-header">
                        <div class="zone-icon">🚄</div>
                        <div class="zone-title">
                            <h3>31-45分（平均的）</h3>
                        </div>
                        <div class="zone-time">31-45分</div>
                    </div>
                    <div class="zone-stations">
                        <h4>主な通学駅</h4>
                        <div class="stations-list">
                            <strong>江戸川区：</strong>小岩駅（35-40分）、瑞江駅（40分）<br>
                            <strong>千葉県市川市：</strong>南行徳駅、市川駅、本八幡（35-45分）<br>
                            <strong>江東区：</strong>南砂町、東大島（30-40分）
                        </div>
                    </div>
                </div>

                <div class="zone-card zone-far">
                    <div class="zone-header">
                        <div class="zone-icon">🚅</div>
                        <div class="zone-title">
                            <h3>46-60分（やや遠い）</h3>
                        </div>
                        <div class="zone-time">46-60分</div>
                    </div>
                    <div class="zone-stations">
                        <h4>主な通学駅</h4>
                        <div class="stations-list">
                            <strong>千葉県：</strong>船橋駅、津田沼駅（船橋市）50-60分、新浦安駅（浦安市）60分、幕張本郷駅（千葉市）60分<br>
                            <strong>埼玉県：</strong>八潮駅（八潮市）、三郷中央駅（三郷市）、川口駅（川口市）45-50分
                        </div>
                    </div>
                </div>

                <div class="zone-card zone-very-far">
                    <div class="zone-header">
                        <div class="zone-icon">🚈</div>
                        <div class="zone-title">
                            <h3>61分以上（遠い）</h3>
                        </div>
                        <div class="zone-time">61分+</div>
                    </div>
                    <div class="zone-stations">
                        <h4>主な通学駅</h4>
                        <div class="stations-list">
                            <strong>千葉県船橋市：</strong>船橋日大前、北習志野（70分）<br>
                            <strong>千葉県千葉市：</strong>検見川浜、西千葉、海浜幕張（65-70分）<br>
                            <strong>その他：</strong>おおたかの森（流山市）60分、戸田公園（埼玉県戸田市）55分
                        </div>
                    </div>
                </div>
            </div>

            <div class="points-section">
                <h2>🎯 学校選びのポイント</h2>
                <div class="points-grid">
                    <div class="point-card">
                        <h3>1. 通学時間を重視する場合</h3>
                        <div class="merit-box">
                            <h4>💡 メリット</h4>
                            <p>通学時間が短いと、学習や部活動、睡眠時間の確保がしやすくなります。疲労が少なく、体調管理が容易になります。放課後の自由時間が増え、予習・復習に充てる時間が確保できます。</p>
                        </div>
                        <div class="area-box">
                            <h4>🏢 検討すべき地域</h4>
                            <p><strong>最適：</strong>墨田区、中央区、台東区、江東区内（30分以内）<br>
                            <strong>現実的：</strong>江戸川区西部、市川市西部も45分以内で通学可能</p>
                        </div>
                    </div>

                    <div class="point-card">
                        <h3>2. 学校の教育内容や特色を重視する場合</h3>
                        <p>日本大学第一高校の特色を活かすなら、60分以内の通学圏内が現実的です。千葉県や埼玉県から通う生徒も多いことから、学校の教育内容や大学進学実績に魅力を感じて通学距離よりも教育環境を重視している傾向が見られます。</p>
                    </div>

                    <div class="point-card">
                        <h3>3. 交通手段と路線の検討</h3>
                        <div class="transport-box">
                            <h4>🚇 主要通学路線</h4>
                            <div class="transport-lines">
                                <div class="line-tag">東京メトロ東西線</div>
                                <div class="line-tag">東京メトロ半蔵門線</div>
                                <div class="line-tag">都営浅草線</div>
                                <div class="line-tag">JR総武線</div>
                                <div class="line-tag">JR京葉線</div>
                            </div>
                            <p style="margin-top: 15px;">これらの路線沿いは通学の利便性が高く、乗り換えの少ない経路を選ぶことで通学負担を軽減できます。</p>
                        </div>
                    </div>

                    <div class="point-card">
                        <h3>4. 長距離通学の現実</h3>
                        <p>千葉県（船橋市、千葉市など）や埼玉県からの通学者も多数いることから、学校の魅力が通学時間のデメリットを上回ると判断している家庭が相当数あることがわかります。ただし、片道60分以上の通学は体力面での負担も考慮する必要があります。</p>
                    </div>
                </div>
            </div>

            <div class="time-guide">
                <h2>⏰ 通学時間別ガイド</h2>
                <div class="time-guide-grid">
                    <div class="time-guide-item time-guide-45">
                        <h3>45分以内</h3>
                        <p>比較的負担は少なく、学習・部活動・休息のバランスが取りやすい</p>
                    </div>
                    <div class="time-guide-item time-guide-60">
                        <h3>45-60分</h3>
                        <p>多少の負担を覚悟する必要があり、時間管理がより重要になる</p>
                    </div>
                    <div class="time-guide-item time-guide-60plus">
                        <h3>60分以上</h3>
                        <p>学校の特色や教育内容に強い魅力を感じることが選択の重要な要素</p>
                    </div>
                </div>
            </div>

            <div class="summary-section">
                <h2>📢 まとめ</h2>
                <div class="message-content">
                    <p style="font-size: 1.1rem; text-align: center; margin-bottom: 30px;">
                        日本大学第一高校を検討する際は、以下のポイントを総合的に判断することが大切です
                    </p>
                    
                    <div class="summary-points">
                        <div class="summary-point">
                            <strong>🏃‍♂️ 体力・時間管理</strong><br>
                            受験生の方の通学に対する体力や時間管理能力
                        </div>
                        <div class="summary-point">
                            <strong>⚖️ バランス重視</strong><br>
                            学校の教育内容や進学実績と通学負担のバランス
                        </div>
                        <div class="summary-point">
                            <strong>🚇 交通アクセス</strong><br>
                            自宅から学校までの交通アクセスの便利さ
                        </div>
                        <div class="summary-point">
                            <strong>🏀 課外活動</strong><br>
                            部活動など放課後の活動への参加意欲
                        </div>
                    </div>

                    <p style="margin-top: 30px; font-size: 1.1rem; line-height: 1.8;">
                        学校選びは、学力や進学実績だけでなく、<strong>3年間の高校生活の質を左右する通学環境も重要な要素</strong>です。このデータが皆様の学校選択の一助となれば幸いです。
                    </p>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showSection(section) {
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(sec => {
                sec.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected section
            document.getElementById(section).classList.add('active');
            
            // Add active class to selected tab
            document.querySelector(`.nav-tab.${section}`).classList.add('active');
        }
    </script>
</body>
</html>"""