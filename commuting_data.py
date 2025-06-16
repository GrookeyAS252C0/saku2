# commuting_data.py
COMMUTING_DATA_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本大学第一中学・高等学校 新入生通学状況レポート 2025</title>
    <style>
        body {
            font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Yu Gothic Medium', 'Meiryo', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.2rem;
            margin: 0 0 10px 0;
            font-weight: bold;
        }
        
        .header .subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin: 0;
        }
        
        .content {
            padding: 40px;
        }
        
        .intro {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        
        .intro h2 {
            margin: 0 0 15px 0;
            font-size: 1.3rem;
        }
        
        .school-section {
            margin-bottom: 50px;
        }
        
        /* 中学用オレンジテーマ */
        .middle-school .section {
            margin-bottom: 40px;
            padding: 25px;
            border-radius: 10px;
            background: #fff8f0;
            border-left: 5px solid #ff8c42;
        }
        
        .middle-school .section h2 {
            color: #d2691e;
            font-size: 1.4rem;
            margin: 0 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #ffe4d1;
        }
        
        .middle-school .section h3 {
            color: #ff6b35;
            font-size: 1.2rem;
            margin: 25px 0 15px 0;
        }
        
        .middle-school .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 2px solid #ffe4d1;
        }
        
        .middle-school .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #ff8c42;
            margin-bottom: 5px;
        }
        
        .middle-school .data-table th {
            background: #ff8c42;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: bold;
        }
        
        .middle-school .data-table tr:nth-child(even) {
            background: #fff8f0;
        }
        
        .middle-school .highlight-box {
            background: linear-gradient(135deg, #ffe4d1 0%, #ffb084 100%);
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #ff6b35;
        }
        
        .middle-school .key-points {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #ff8c42;
        }
        
        .middle-school .conclusion {
            background: linear-gradient(135deg, #ffe4d1 0%, #ffc4a3 100%);
            padding: 30px;
            border-radius: 10px;
            margin-top: 30px;
        }
        
        /* 高校用青テーマ */
        .high-school .section {
            margin-bottom: 40px;
            padding: 25px;
            border-radius: 10px;
            background: #f0f8ff;
            border-left: 5px solid #4169e1;
        }
        
        .high-school .section h2 {
            color: #1e3c72;
            font-size: 1.4rem;
            margin: 0 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e6ff;
        }
        
        .high-school .section h3 {
            color: #2a5298;
            font-size: 1.2rem;
            margin: 25px 0 15px 0;
        }
        
        .high-school .stat-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 2px solid #e0e6ff;
        }
        
        .high-school .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .high-school .data-table th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: bold;
        }
        
        .high-school .data-table tr:nth-child(even) {
            background: #f8f9ff;
        }
        
        .high-school .highlight-box {
            background: linear-gradient(135deg, #e0e6ff 0%, #b8c5ff 100%);
            padding: 20px;
            border-radius: 8px;
            margin: 15px 0;
            border-left: 4px solid #4169e1;
        }
        
        .high-school .key-points {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #667eea;
        }
        
        .high-school .conclusion {
            background: linear-gradient(135deg, #e0e6ff 0%, #c4d1ff 100%);
            padding: 30px;
            border-radius: 10px;
            margin-top: 30px;
        }
        
        /* 共通スタイル */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .data-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }
        
        .percentage {
            font-weight: bold;
            color: #f093fb;
        }
        
        .key-points ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .key-points li {
            margin-bottom: 8px;
            color: #333;
        }
        
        .school-header {
            text-align: center;
            padding: 30px;
            margin: 40px 0 30px 0;
            border-radius: 15px;
            color: white;
            font-size: 1.8rem;
            font-weight: bold;
        }
        
        .middle-school-header {
            background: linear-gradient(135deg, #ff8c42 0%, #ff6b35 100%);
        }
        
        .high-school-header {
            background: linear-gradient(135deg, #667eea 0%, #4169e1 100%);
        }
        
        .conclusion h2 {
            color: #1e3c72;
            margin: 0 0 20px 0;
        }
        
        .comparison-section {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin: 40px 0;
        }
        
        .comparison-table {
            background: white;
            color: #333;
            border-radius: 8px;
            overflow: hidden;
            margin-top: 20px;
        }
        
        .comparison-table th {
            background: #f093fb;
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
        }
        
        .comparison-table td {
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }
        
        @media (max-width: 768px) {
            .container {
                margin: 10px;
                border-radius: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 1.5rem;
            }
            
            .content {
                padding: 20px;
            }
            
            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>日本大学第一中学・高等学校</h1>
            <p class="subtitle">2025年度新入生通学状況総合レポート</p>
        </div>
        
        <div class="content">
            <div class="intro">
                <h2>はじめに</h2>
                <p>本レポートは、2025年4月に日本大学第一中学・高等学校に入学した新入生の通学データを詳細に分析し、本校への通学の実態を明らかにするものです。受験をご検討の皆様の参考となるよう、客観的なデータに基づいて報告いたします。</p>
            </div>
            
            <!-- 中学校データ -->
            <div class="school-section middle-school">
                <div class="school-header middle-school-header">
                    日本大学第一中学校 通学状況
                </div>
                
                <div class="section">
                    <h2>1. 新入生の概要</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">206</div>
                            <div class="stat-label">総生徒数</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">125</div>
                            <div class="stat-label">男子（60.7%）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">81</div>
                            <div class="stat-label">女子（39.3%）</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>2. 通学時間の詳細分析</h2>
                    
                    <h3>2.1 通学時間の分布状況</h3>
                    <div class="highlight-box">
                        <strong>通学時間別の人数分布（上位5項目）</strong>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>通学時間</th>
                                    <th>人数</th>
                                    <th>割合</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>40分</td>
                                    <td>36名</td>
                                    <td class="percentage">17.5%</td>
                                </tr>
                                <tr>
                                    <td>30分</td>
                                    <td>31名</td>
                                    <td class="percentage">15.0%</td>
                                </tr>
                                <tr>
                                    <td>50分</td>
                                    <td>28名</td>
                                    <td class="percentage">13.6%</td>
                                </tr>
                                <tr>
                                    <td>60分</td>
                                    <td>28名</td>
                                    <td class="percentage">13.6%</td>
                                </tr>
                                <tr>
                                    <td>20分</td>
                                    <td>12名</td>
                                    <td class="percentage">5.8%</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">58</div>
                            <div class="stat-label">30分以下（28.2%）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">125</div>
                            <div class="stat-label">31-60分（60.7%）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">23</div>
                            <div class="stat-label">61-90分（11.2%）</div>
                        </div>
                    </div>
                    
                    <div class="highlight-box">
                        <strong>特筆すべきは、全体の約89%が60分以内で通学していることです。</strong>
                    </div>
                </div>
                
                <div class="section">
                    <h2>3. 交通機関利用状況の詳細</h2>
                    
                    <h3>3.1 乗り換え回数の実態</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">127</div>
                            <div class="stat-label">1回（61.7%）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">67</div>
                            <div class="stat-label">2回（32.5%）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">9</div>
                            <div class="stat-label">3回（4.4%）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">3</div>
                            <div class="stat-label">4回（1.5%）</div>
                        </div>
                    </div>
                </div>
                
                <div class="conclusion">
                    <h2>中学校まとめ</h2>
                    <div class="key-points">
                        <ul>
                            <li>全体の<strong>61.7%が乗り換え1回</strong>で通学</li>
                            <li><strong>89%が60分以内</strong>で通学可能</li>
                            <li>30分以内で通学できる生徒が<strong>28.2%</strong>存在</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- 高校データ -->
            <div class="school-section high-school">
                <div class="school-header high-school-header">
                    日本大学第一高等学校 通学状況
                </div>
                
                <div class="section">
                    <h2>1. 新入生の概要</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">351</div>
                            <div class="stat-label">総生徒数</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">230</div>
                            <div class="stat-label">男子（65.5%）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">121</div>
                            <div class="stat-label">女子（34.5%）</div>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>2. 通学における乗り換え回数の全体像</h2>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>乗り換え回数</th>
                                <th>人数</th>
                                <th>割合</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>0回（乗り換えなし）</td>
                                <td>241人</td>
                                <td class="percentage">68.7%</td>
                            </tr>
                            <tr>
                                <td>1回</td>
                                <td>85人</td>
                                <td class="percentage">24.2%</td>
                            </tr>
                            <tr>
                                <td>2回</td>
                                <td>21人</td>
                                <td class="percentage">6.0%</td>
                            </tr>
                            <tr>
                                <td>3回</td>
                                <td>3人</td>
                                <td class="percentage">0.9%</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <div class="highlight-box">
                        <strong>約7割の生徒が乗り換えなしで通学できており、交通の便が良い立地であることがわかります。</strong>
                    </div>
                </div>
                
                <div class="section">
                    <h2>3. 主要居住地域（乗り換えなし）</h2>
                    <div class="highlight-box">
                        <strong>最も多い居住地トップ5</strong>
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>居住地</th>
                                    <th>人数</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>東京都江東区</td>
                                    <td>35人</td>
                                </tr>
                                <tr>
                                    <td>東京都江戸川区</td>
                                    <td>30人</td>
                                </tr>
                                <tr>
                                    <td>千葉県船橋市</td>
                                    <td>21人</td>
                                </tr>
                                <tr>
                                    <td>千葉県市川市</td>
                                    <td>18人</td>
                                </tr>
                                <tr>
                                    <td>東京都墨田区</td>
                                    <td>16人</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div class="section">
                    <h2>4. 入学カテゴリ別の特徴</h2>
                    
                    <h3>4.1 第一希望で入学した生徒（148人）</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">46.4</div>
                            <div class="stat-label">平均通学時間（分）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">64.9%</div>
                            <div class="stat-label">乗り換えなし</div>
                        </div>
                    </div>
                    
                    <h3>4.2 併願で入学した生徒（32人）</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">43.4</div>
                            <div class="stat-label">平均通学時間（分）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">84.4%</div>
                            <div class="stat-label">乗り換えなし</div>
                        </div>
                    </div>
                    
                    <h3>4.3 内部進学生（171人）</h3>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">46.3</div>
                            <div class="stat-label">平均通学時間（分）</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">69.0%</div>
                            <div class="stat-label">乗り換えなし</div>
                        </div>
                    </div>
                </div>
                
                <div class="conclusion">
                    <h2>高校まとめ</h2>
                    <div class="key-points">
                        <ul>
                            <li>全体の<strong>68.7%が乗り換えなし</strong>で通学</li>
                            <li><strong>92.9%が1回以下の乗り換え</strong>で通学可能</li>
                            <li>併願生は乗り換えなしの割合が特に高い（<strong>84.4%</strong>）</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- 比較セクション -->
            <div class="comparison-section">
                <h2>中学・高校 通学状況比較</h2>
                <table class="comparison-table data-table">
                    <thead>
                        <tr>
                            <th>項目</th>
                            <th>中学</th>
                            <th>高校</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>総生徒数</td>
                            <td>206名</td>
                            <td>351名</td>
                        </tr>
                        <tr>
                            <td>男女比</td>
                            <td>男子60.7% / 女子39.3%</td>
                            <td>男子65.5% / 女子34.5%</td>
                        </tr>
                        <tr>
                            <td>60分以内通学</td>
                            <td>89%</td>
                            <td>92.9%（1回以下乗り換え）</td>
                        </tr>
                        <tr>
                            <td>主要通学手段</td>
                            <td>乗り換え1回（61.7%）</td>
                            <td>乗り換えなし（68.7%）</td>
                        </tr>
                        <tr>
                            <td>平均通学時間</td>
                            <td>約46分（推定）</td>
                            <td>46.1分</td>
                        </tr>
                    </tbody>
                </table>
                
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; margin-top: 20px;">
                    <h3>総合分析</h3>
                    <p>中学・高校ともに優れた立地にあり、多くの生徒が1時間以内で通学できる環境です。高校の方が乗り換えなしで通学できる生徒の割合が高く、より広域からアクセスしやすい特徴があります。</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""