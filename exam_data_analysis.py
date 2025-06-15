# exam_data_analysis.py
EXAM_DATA_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本大学第一中学校・高等学校 2025年度入試データ</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .main-header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
            backdrop-filter: blur(10px);
        }

        .main-header h1 {
            color: #2c3e50;
            font-size: 2.8rem;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .main-header .subtitle {
            color: #7f8c8d;
            font-size: 1.3rem;
            margin-bottom: 30px;
        }

        .tab-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }

        .tab-button {
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .tab-button.middle-school {
            background: linear-gradient(45deg, #f39c12, #e67e22);
            color: white;
        }

        .tab-button.middle-school.active {
            background: linear-gradient(45deg, #e67e22, #d35400);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(230, 126, 34, 0.4);
        }

        .tab-button.high-school {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
        }

        .tab-button.high-school.active {
            background: linear-gradient(45deg, #2980b9, #1f4e79);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(52, 152, 219, 0.4);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
            backdrop-filter: blur(10px);
        }

        .header h2 {
            font-size: 2.2rem;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .middle-school .header h2 {
            color: #e67e22;
        }

        .high-school .header h2 {
            color: #2980b9;
        }

        .header .subtitle {
            color: #7f8c8d;
            font-size: 1.1rem;
            margin-bottom: 20px;
        }

        .total-students {
            padding: 15px 30px;
            border-radius: 50px;
            display: inline-block;
            font-size: 1.3rem;
            font-weight: bold;
            color: white;
        }

        .middle-school .total-students {
            background: linear-gradient(45deg, #f39c12, #e67e22);
            box-shadow: 0 5px 15px rgba(243, 156, 18, 0.3);
        }

        .high-school .total-students {
            background: linear-gradient(45deg, #3498db, #2980b9);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }

        .exam-type {
            padding: 10px 20px;
            border-radius: 25px;
            display: inline-block;
            font-size: 1rem;
            margin-top: 10px;
            color: white;
        }

        .middle-school .exam-type {
            background: linear-gradient(45deg, #e67e22, #d35400);
        }

        .high-school .exam-type {
            background: linear-gradient(45deg, #2980b9, #1f4e79);
        }

        .section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .section h3 {
            font-size: 1.8rem;
            margin-bottom: 20px;
            padding-bottom: 10px;
            position: relative;
        }

        .middle-school .section h3 {
            color: #e67e22;
            border-bottom: 3px solid #f39c12;
        }

        .middle-school .section h3::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 50px;
            height: 3px;
            background: #e67e22;
        }

        .high-school .section h3 {
            color: #2980b9;
            border-bottom: 3px solid #3498db;
        }

        .high-school .section h3::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 50px;
            height: 3px;
            background: #2980b9;
        }

        .section h4 {
            color: #34495e;
            font-size: 1.3rem;
            margin: 25px 0 15px 0;
            padding-left: 15px;
        }

        .middle-school .section h4 {
            border-left: 4px solid #f39c12;
        }

        .high-school .section h4 {
            border-left: 4px solid #3498db;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .middle-school .stat-card {
            border-left: 5px solid #f39c12;
        }

        .high-school .stat-card {
            border-left: 5px solid #3498db;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 25px rgba(0, 0, 0, 0.1);
        }

        .stat-card .number {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }

        .stat-card .label {
            color: #7f8c8d;
            font-size: 1.1rem;
        }

        .ranking-list {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
        }

        .ranking-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #dee2e6;
            transition: background 0.3s ease;
        }

        .ranking-item:last-child {
            border-bottom: none;
        }

        .middle-school .ranking-item:hover {
            background: rgba(243, 156, 18, 0.1);
            border-radius: 5px;
        }

        .high-school .ranking-item:hover {
            background: rgba(52, 152, 219, 0.1);
            border-radius: 5px;
        }

        .rank {
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }

        .middle-school .rank {
            background: linear-gradient(45deg, #f39c12, #e67e22);
        }

        .middle-school .rank.top-3 {
            background: linear-gradient(45deg, #e67e22, #d35400);
        }

        .high-school .rank {
            background: linear-gradient(45deg, #3498db, #2980b9);
        }

        .high-school .rank.top-3 {
            background: linear-gradient(45deg, #2980b9, #1f4e79);
        }

        .school-name {
            flex: 1;
            font-weight: 500;
        }

        .count {
            font-weight: bold;
            color: #2c3e50;
            padding: 5px 10px;
            border-radius: 20px;
        }

        .middle-school .count {
            background: rgba(243, 156, 18, 0.1);
        }

        .high-school .count {
            background: rgba(52, 152, 219, 0.1);
        }

        .chart {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
        }

        .bar-chart {
            margin: 20px 0;
        }

        .bar-item {
            display: flex;
            align-items: center;
            margin: 10px 0;
        }

        .bar-label {
            width: 100px;
            font-size: 0.9rem;
            color: #666;
        }

        .bar {
            flex: 1;
            height: 25px;
            background: #ecf0f1;
            border-radius: 12px;
            overflow: hidden;
            margin: 0 10px;
            position: relative;
        }

        .bar-fill {
            height: 100%;
            transition: width 0.8s ease;
            border-radius: 12px;
        }

        .middle-school .bar-fill {
            background: linear-gradient(90deg, #f39c12, #e67e22);
        }

        .high-school .bar-fill {
            background: linear-gradient(90deg, #3498db, #2980b9);
        }

        .bar-text {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
            font-size: 0.8rem;
        }

        .highlight-box {
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }

        .middle-school .highlight-box {
            background: linear-gradient(135deg, #fef5e7, #fdeaa7);
            border-left: 5px solid #f39c12;
        }

        .high-school .highlight-box {
            background: linear-gradient(135deg, #e8f4f8, #d4f1f4);
            border-left: 5px solid #3498db;
        }

        .gender-stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }

        .gender-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
        }

        .middle-school .gender-card.male {
            border-top: 5px solid #f39c12;
        }

        .middle-school .gender-card.female {
            border-top: 5px solid #e67e22;
        }

        .high-school .gender-card.male {
            border-top: 5px solid #3498db;
        }

        .high-school .gender-card.female {
            border-top: 5px solid #2980b9;
        }

        .keyword-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .keyword-card {
            border-radius: 10px;
            padding: 15px;
            text-align: center;
        }

        .middle-school .keyword-card {
            background: linear-gradient(135deg, #fef9e7, #fef5e7);
            border-top: 3px solid #f39c12;
        }

        .high-school .keyword-card {
            background: linear-gradient(135deg, #e8f4f8, #e1f5fe);
            border-top: 3px solid #3498db;
        }

        .keyword-card .keyword {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .middle-school .keyword-card .keyword {
            color: #e67e22;
        }

        .high-school .keyword-card .keyword {
            color: #2980b9;
        }

        .keyword-card .stats {
            color: #7f8c8d;
            font-size: 0.9rem;
        }

        .trend-box {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }

        .trend-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 20px;
        }

        .middle-school .trend-card.tokyo {
            border-top: 5px solid #f39c12;
        }

        .middle-school .trend-card.chiba {
            border-top: 5px solid #e67e22;
        }

        .high-school .trend-card.tokyo {
            border-top: 5px solid #3498db;
        }

        .high-school .trend-card.chiba {
            border-top: 5px solid #2980b9;
        }

        .footer {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .data-note {
            border: 2px solid;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            text-align: center;
            font-weight: bold;
        }

        .middle-school .data-note {
            background: linear-gradient(135deg, #fef5e7, #fff8dc);
            border-color: #f39c12;
            color: #d68910;
        }

        .high-school .data-note {
            background: linear-gradient(135deg, #e8f4f8, #f0f8ff);
            border-color: #3498db;
            color: #1f4e79;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .main-header h1 {
                font-size: 2.2rem;
            }
            
            .tab-container {
                flex-direction: column;
                align-items: center;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .gender-stats {
                grid-template-columns: 1fr;
            }
            
            .trend-box {
                grid-template-columns: 1fr;
            }
            
            .ranking-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-header">
            <h1>日本大学第一中学校・高等学校</h1>
            <div class="subtitle">2025年度入試 受験生動向データ</div>
        </div>

        <div class="tab-container">
            <button class="tab-button middle-school active" onclick="showTab('middle-school')">
                🎓 中学入試データ（561名）
            </button>
            <button class="tab-button high-school" onclick="showTab('high-school')">
                🎯 高校入試データ（111名）
            </button>
        </div>

        <!-- 中学入試データ -->
        <div id="middle-school" class="tab-content middle-school active">
            <div class="header">
                <h2>中学入試 受験生動向データ</h2>
                <div class="subtitle">受験生・保護者の皆様へ</div>
                <div class="total-students">総受験生数: 561名</div>
            </div>

            <div class="section">
                <h3>📍 地域別受験生分布</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">443</div>
                        <div class="label">東京都（79.0%）</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">75</div>
                        <div class="label">千葉県（13.4%）</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">20</div>
                        <div class="label">埼玉県（3.6%）</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">20</div>
                        <div class="label">神奈川県（3.6%）</div>
                    </div>
                </div>
                
                <h4>東京都内で特に多い区（上位10区）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">江東区</div>
                        <div class="count">80名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">江戸川区</div>
                        <div class="count">44名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">墨田区</div>
                        <div class="count">33名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">4</div>
                        <div class="school-name">足立区</div>
                        <div class="count">24名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">5</div>
                        <div class="school-name">葛飾区</div>
                        <div class="count">24名</div>
                    </div>
                </div>

                <h4>千葉県内で特に多い市（上位5市）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">船橋市</div>
                        <div class="count">27名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">千葉市（各区合計）</div>
                        <div class="count">15名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">市川市</div>
                        <div class="count">11名</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>🚃 通学時間について</h3>
                <div class="highlight-box">
                    <strong>91.6%の受験生が通学時間60分以内</strong><br>
                    多くの方にとって無理のない通学範囲内にあることがわかります。
                </div>
                
                <div class="chart">
                    <div class="bar-chart">
                        <div class="bar-item">
                            <div class="bar-label">20分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 7.7%"></div>
                                <div class="bar-text">43名 (7.7%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">30分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 21.4%"></div>
                                <div class="bar-text">120名 (21.4%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">40分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 22.3%"></div>
                                <div class="bar-text">125名 (22.3%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">50分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 17.3%"></div>
                                <div class="bar-text">97名 (17.3%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">60分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 23.9%"></div>
                                <div class="bar-text">134名 (23.9%)</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>🏫 他校との併願状況</h3>
                
                <h4>一緒に受験されることの多い学校（上位10校）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">日本大学豊山中学校</div>
                        <div class="count">50名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">日本大学第二中学校</div>
                        <div class="count">30名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">東洋大学京北中学校</div>
                        <div class="count">21名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">4</div>
                        <div class="school-name">千葉日本大学第一中学校</div>
                        <div class="count">20名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">5</div>
                        <div class="school-name">安田学園中学校</div>
                        <div class="count">19名</div>
                    </div>
                </div>

                <div class="highlight-box">
                    <strong>日本大学系列校との併願について</strong><br>
                    127名（22.6%）の受験生が日本大学系列校を併願<br>
                    日本大学への進学を見据えて、複数の日大系列校を受験される方が多いことがわかります。
                </div>

                <h4>👦 男子受験生の併願傾向（主要5校）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">日本大学豊山中学校（男子校）</div>
                        <div class="count">50名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">日本大学第二中学校</div>
                        <div class="count">20名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">千葉日本大学第一中学校</div>
                        <div class="count">14名</div>
                    </div>
                </div>

                <h4>👧 女子受験生の併願傾向（主要5校）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">日本大学第二中学校</div>
                        <div class="count">10名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">東洋大学京北中学校</div>
                        <div class="count">8名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">淑徳巣鴨中学校</div>
                        <div class="count">8名</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>👦👧 男女別の特徴</h3>
                <div class="gender-stats">
                    <div class="gender-card male">
                        <h4>男子受験生</h4>
                        <div class="number">349名</div>
                        <div class="label">62.2%</div>
                    </div>
                    <div class="gender-card female">
                        <h4>女子受験生</h4>
                        <div class="number">212名</div>
                        <div class="label">37.8%</div>
                    </div>
                </div>

                <h4>受験パターンについて</h4>
                <div class="chart">
                    <div class="bar-chart">
                        <div class="bar-item">
                            <div class="bar-label">1回のみ</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 39.6%"></div>
                                <div class="bar-text">222名 (39.6%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">2回</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 29.9%"></div>
                                <div class="bar-text">168名 (29.9%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">3回</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 12.8%"></div>
                                <div class="bar-text">72名 (12.8%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">4回</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 17.6%"></div>
                                <div class="bar-text">99名 (17.6%)</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>✨ データから見える本校の特徴</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">91.6%</div>
                        <div class="label">通学時間60分以内<br>アクセスの良さ</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">22.6%</div>
                        <div class="label">日大系列校併願<br>ブランドの安心感</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">28%</div>
                        <div class="label">近隣3区からの受験<br>地域に根ざした信頼</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">6:4</div>
                        <div class="label">男女バランス<br>共学校としての魅力</div>
                    </div>
                </div>
            </div>

            <div class="data-note">
                このデータは2025年度入試受験生561名の実際のデータに基づいています（2025年実施）
            </div>
        </div>

        <!-- 高校入試データ -->
        <div id="high-school" class="tab-content high-school">
            <div class="header">
                <h2>高校入試 受験生実態調査</h2>
                <div class="subtitle">一般入試(B)【他校第一志望】</div>
                <div class="total-students">総受験生数: 111名</div>
                <div class="exam-type">公立高校との併願パターン</div>
            </div>

            <div class="section">
                <h3>📍 受験生の居住地域分析</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">62</div>
                        <div class="label">東京都（55.9%）</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">46</div>
                        <div class="label">千葉県（41.4%）</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">3</div>
                        <div class="label">その他（2.7%）</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">97.3%</div>
                        <div class="label">首都圏集中率</div>
                    </div>
                </div>
                
                <h4>東京都内（上位5エリア）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">江戸川区</div>
                        <div class="count">17名（27.4%）</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">江東区</div>
                        <div class="count">17名（27.4%）</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">墨田区</div>
                        <div class="count">5名（8.1%）</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">4</div>
                        <div class="school-name">中央区</div>
                        <div class="count">5名（8.1%）</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">5</div>
                        <div class="school-name">足立区・新宿区・台東区</div>
                        <div class="count">各3名（4.8%）</div>
                    </div>
                </div>

                <h4>千葉県内（上位5エリア）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">船橋市</div>
                        <div class="count">15名（32.6%）</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">市川市</div>
                        <div class="count">9名（19.6%）</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">千葉市美浜区</div>
                        <div class="count">5名（10.9%）</div>
                    </div>
                </div>

                <div class="highlight-box">
                    <strong>地域特性の分析</strong><br>
                    <strong>東京都：</strong>江戸川区・江東区に集中（学校立地の墨田区に隣接）<br>
                    <strong>千葉県：</strong>総武線・京葉線沿線からの受験が多い傾向<br>
                    <strong>通学圏：</strong>学校周辺30km圏内からの受験が大部分を占める
                </div>
            </div>

            <div class="section">
                <h3>🚃 通学時間と地域の関係性</h3>
                <div class="highlight-box">
                    <strong>87.4%の受験生が通学時間60分以内を希望</strong><br>
                    高校生にとって適切な通学時間内での学校選択が行われています。
                </div>
                
                <div class="chart">
                    <div class="bar-chart">
                        <div class="bar-item">
                            <div class="bar-label">30分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 18.9%"></div>
                                <div class="bar-text">21名 (18.9%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">40分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 21.6%"></div>
                                <div class="bar-text">24名 (21.6%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">50分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 18.0%"></div>
                                <div class="bar-text">20名 (18.0%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">60分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 22.5%"></div>
                                <div class="bar-text">25名 (22.5%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">70分以内</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 8.1%"></div>
                                <div class="bar-text">9名 (8.1%)</div>
                            </div>
                        </div>
                        <div class="bar-item">
                            <div class="bar-label">80分以上</div>
                            <div class="bar">
                                <div class="bar-fill" style="width: 10.9%"></div>
                                <div class="bar-text">12名 (10.9%)</div>
                            </div>
                        </div>
                    </div>
                </div>

                <h4>地域別通学時間の特徴</h4>
                <div class="trend-box">
                    <div class="trend-card tokyo">
                        <h4>東京都受験者</h4>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="number">30.6%</div>
                                <div class="label">30分以内</div>
                            </div>
                            <div class="stat-card">
                                <div class="number">29.0%</div>
                                <div class="label">40分以内</div>
                            </div>
                        </div>
                        <p><strong>短時間通学が可能：</strong>約6割が40分以内で通学可能</p>
                    </div>
                    <div class="trend-card chiba">
                        <h4>千葉県受験者</h4>
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="number">37.0%</div>
                                <div class="label">60分以内が最多</div>
                            </div>
                            <div class="stat-card">
                                <div class="number">19.6%</div>
                                <div class="label">70分以内</div>
                            </div>
                        </div>
                        <p><strong>中距離通学が中心：</strong>通学時間をかけても本校を選択</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>🏫 併願校（第一志望校）分析</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">91</div>
                        <div class="label">公立高校志望（82.0%）</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">20</div>
                        <div class="label">私立・その他志望（18.0%）</div>
                    </div>
                </div>

                <h4>主要併願校ランキング（全体上位8校）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">東京都立江戸川高等学校</div>
                        <div class="count">11名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">東京都立深川高等学校</div>
                        <div class="count">10名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">千葉県立幕張総合高等学校</div>
                        <div class="count">6名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">4</div>
                        <div class="school-name">千葉県立国府台高等学校</div>
                        <div class="count">6名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">5</div>
                        <div class="school-name">國學院高等学校</div>
                        <div class="count">5名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">6</div>
                        <div class="school-name">東京都立晴海総合高等学校</div>
                        <div class="count">5名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">7</div>
                        <div class="school-name">千葉県立国分高等学校</div>
                        <div class="count">4名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">8</div>
                        <div class="school-name">東京都立墨田川高等学校</div>
                        <div class="count">4名</div>
                    </div>
                </div>

                <h4>私立・その他志望者の詳細（20名・18.0%）</h4>
                <div class="ranking-list">
                    <div class="ranking-item">
                        <div class="rank top-3">1</div>
                        <div class="school-name">國學院高等学校</div>
                        <div class="count">5名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">2</div>
                        <div class="school-name">千葉日本大学第一高等学校</div>
                        <div class="count">2名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank top-3">3</div>
                        <div class="school-name">日本大学豊山高等学校</div>
                        <div class="count">2名</div>
                    </div>
                    <div class="ranking-item">
                        <div class="rank">4</div>
                        <div class="school-name">その他私立高校・高専</div>
                        <div class="count">11名</div>
                    </div>
                </div>

                <div class="highlight-box">
                    <strong>私立併願校の特徴</strong><br>
                    <strong>日本大学付属校系：</strong>6名（30%）が日大系列校を第一志望<br>
                    <strong>大学付属校：</strong>専修大学松戸、國學院なども含む<br>
                    <strong>学校タイプ：</strong>共学・別学校、進学校、高等専門学校と多様
                </div>
            </div>

            <div class="section">
                <h3>💭 志望理由の詳細分析</h3>
                <div class="keyword-grid">
                    <div class="keyword-card">
                        <div class="keyword">日本大学</div>
                        <div class="stats">23件（20.7%）</div>
                    </div>
                    <div class="keyword-card">
                        <div class="keyword">先生</div>
                        <div class="stats">19件（17.1%）</div>
                    </div>
                    <div class="keyword-card">
                        <div class="keyword">雰囲気</div>
                        <div class="stats">15件（13.5%）</div>
                    </div>
                    <div class="keyword-card">
                        <div class="keyword">日大</div>
                        <div class="stats">14件（12.6%）</div>
                    </div>
                    <div class="keyword-card">
                        <div class="keyword">塾</div>
                        <div class="stats">12件（10.8%）</div>
                    </div>
                    <div class="keyword-card">
                        <div class="keyword">親</div>
                        <div class="stats">12件（10.8%）</div>
                    </div>
                    <div class="keyword-card">
                        <div class="keyword">通学</div>
                        <div class="stats">9件（8.1%）</div>
                    </div>
                    <div class="keyword-card">
                        <div class="keyword">説明会</div>
                        <div class="stats">9件（8.1%）</div>
                    </div>
                </div>

                <h4>地域別の志望理由傾向</h4>
                <div class="trend-box">
                    <div class="trend-card tokyo">
                        <h4>東京都受験者</h4>
                        <p><strong>日本大学進学への言及：16.1%</strong></p>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>教育環境や学校の雰囲気を重視</li>
                            <li>通学利便性を活かした学校選択</li>
                            <li>教師との距離の近さを評価</li>
                        </ul>
                    </div>
                    <div class="trend-card chiba">
                        <h4>千葉県受験者</h4>
                        <p><strong>日本大学進学への言及：28.3%</strong></p>
                        <ul style="margin-top: 10px; padding-left: 20px;">
                            <li>日本大学進学への期待がより強い</li>
                            <li>通学時間をかけても通学したい動機</li>
                            <li>内部進学制度への関心</li>
                        </ul>
                    </div>
                </div>

                <h4>主要な志望動機（複数回答）</h4>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">30%</div>
                        <div class="label">大学進学重視</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">25%</div>
                        <div class="label">教育環境評価</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">20%</div>
                        <div class="label">立地・通学条件</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">15%</div>
                        <div class="label">外部からの推薦</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">10%</div>
                        <div class="label">学校見学・説明会</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <h3>✨ データ分析のまとめ</h3>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">87.4%</div>
                        <div class="label">通学時間60分以内<br>適切な通学範囲</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">82.0%</div>
                        <div class="label">公立高校が第一志望<br>安全志向の併願戦略</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">20.7%</div>
                        <div class="label">日本大学進学重視<br>明確な進路目標</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">97.3%</div>
                        <div class="label">首都圏集中<br>地域に根ざした選択</div>
                    </div>
                </div>

                <div class="highlight-box">
                    <strong>本校が適している可能性の高い受験生</strong><br>
                    ✅ 東京都・千葉県在住で通学時間1時間程度を許容できる方<br>
                    ✅ 日本大学進学に関心をお持ちの方<br>
                    ✅ 教師との距離が近い教育環境を求める方<br>
                    ✅ 学校の雰囲気を重視される方<br>
                    ✅ 公立高校との併願をお考えの方
                </div>
            </div>

            <div class="data-note">
                このデータは2025年度一般入試受験生111名の実際のデータに基づいています（2025年実施）
            </div>
        </div>

        <div class="footer">
            <p><strong>受験をご検討の皆様へ</strong></p>
            <p style="margin: 15px 0;">
                学校見学や説明会を通じて、実際の教育環境をご確認いただくことをお勧めいたします。<br>
                ご質問等がございましたら、お気軽に本校までお問い合わせください。
            </p>
            <p style="color: #7f8c8d;">
                日本大学第一中学校・高等学校 - 受験生・保護者の皆様へ
            </p>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // すべてのタブコンテンツを非表示
            const tabContents = document.querySelectorAll('.tab-content');
            tabContents.forEach(content => {
                content.classList.remove('active');
            });

            // すべてのタブボタンを非アクティブ
            const tabButtons = document.querySelectorAll('.tab-button');
            tabButtons.forEach(button => {
                button.classList.remove('active');
            });

            // 選択されたタブを表示
            document.getElementById(tabName).classList.add('active');
            
            // 対応するボタンをアクティブ
            const activeButton = document.querySelector(`.tab-button.${tabName.replace('-', '-')}`);
            if (activeButton) {
                activeButton.classList.add('active');
            }
        }

        // アニメーション効果の追加
        window.addEventListener('load', function() {
            const barFills = document.querySelectorAll('.bar-fill');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.transition = 'width 1s ease-in-out';
                    }
                });
            });

            barFills.forEach(bar => observer.observe(bar));
        });
    </script>
</body>
</html>"""