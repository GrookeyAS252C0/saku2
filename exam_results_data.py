# exam_results_data.py
EXAM_RESULTS_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本大学第一中学校・高等学校 2025年入試結果</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', 'Meiryo', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }

        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s ease-in-out infinite;
        }

        @keyframes shimmer {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(180deg); }
        }

        .school-name {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }

        .exam-info {
            font-size: 1.5rem;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }

        .nav-tabs {
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
        }

        .nav-tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            font-size: 1.2rem;
            font-weight: bold;
            transition: all 0.3s ease;
            border: none;
            background: transparent;
        }

        .nav-tab.middle-school {
            background: linear-gradient(135deg, #ff7b54 0%, #ff6b35 100%);
            color: white;
        }

        .nav-tab.high-school {
            background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
            color: white;
        }

        .nav-tab:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }

        .nav-tab.active {
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }

        .content {
            padding: 40px 30px;
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* 中学校用スタイル（オレンジ基調） */
        .middle-school-section .overview-section {
            background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 50px;
            box-shadow: 0 10px 30px rgba(255, 152, 0, 0.15);
        }

        .middle-school-section .section-title {
            color: #e65100;
        }

        .middle-school-section .section-title::after {
            background: linear-gradient(135deg, #ff7b54 0%, #ff6b35 100%);
        }

        .middle-school-section .overview-table th,
        .middle-school-section .score-table th {
            background: linear-gradient(135deg, #ff7b54 0%, #ff6b35 100%);
        }

        .middle-school-section .exam-title {
            color: #e65100;
            border-bottom-color: #ff7b54;
        }

        .middle-school-section .exam-title::after {
            background: #ff5722;
        }

        .middle-school-section .exam-section {
            background: #fff8f0;
            border: 1px solid #ffe0b2;
        }

        .middle-school-section .gender-male {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }

        .middle-school-section .gender-female {
            background-color: #fce4ec;
            border-left: 4px solid #e91e63;
        }

        .middle-school-section .category-header {
            background: linear-gradient(135deg, #ffcc80 0%, #ffb74d 100%);
            border-left: 4px solid #ff9800;
        }

        .middle-school-section .male-row {
            background-color: #e1f5fe;
            border-left: 4px solid #03a9f4;
        }

        .middle-school-section .female-row {
            background-color: #fce4ec;
            border-left: 4px solid #e91e63;
        }

        .middle-school-section .total-score {
            background: linear-gradient(135deg, #ffcc80 0%, #ffb74d 100%);
        }

        .middle-school-section .highlight-number {
            color: #e65100;
        }

        .middle-school-section .special-note {
            background: linear-gradient(135deg, #fff3c4 0%, #ffd54f 100%);
            color: #e65100;
        }

        /* 高校用スタイル（青基調） */
        .high-school-section .overview-section {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 50px;
            box-shadow: 0 10px 30px rgba(33, 150, 243, 0.15);
        }

        .high-school-section .section-title {
            color: #0d47a1;
        }

        .high-school-section .section-title::after {
            background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
        }

        .high-school-section .overview-table th,
        .high-school-section .score-table th {
            background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
        }

        .high-school-section .exam-title {
            color: #0d47a1;
            border-bottom-color: #4a90e2;
        }

        .high-school-section .exam-title::after {
            background: #2196f3;
        }

        .high-school-section .exam-section {
            background: #f0f8ff;
            border: 1px solid #bbdefb;
        }

        .high-school-section .gender-male {
            background-color: #e1f5fe;
            border-left: 4px solid #03a9f4;
        }

        .high-school-section .gender-female {
            background-color: #fce4ec;
            border-left: 4px solid #e91e63;
        }

        .high-school-section .category-header {
            background: linear-gradient(135deg, #90caf9 0%, #64b5f6 100%);
            border-left: 4px solid #2196f3;
        }

        .high-school-section .male-section {
            background-color: #e1f5fe;
            border-left: 4px solid #03a9f4;
        }

        .high-school-section .female-section {
            background-color: #fce4ec;
            border-left: 4px solid #e91e63;
        }

        .high-school-section .category-a {
            background-color: #e8f5e8;
            border-left: 4px solid #4caf50;
        }

        .high-school-section .category-b {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
        }

        .high-school-section .total-row {
            background: linear-gradient(135deg, #90caf9 0%, #64b5f6 100%);
            border-left: 4px solid #2196f3;
        }

        .high-school-section .total-score {
            background: linear-gradient(135deg, #90caf9 0%, #64b5f6 100%);
        }

        .high-school-section .highlight-number, .high-school-section .highlight-score {
            color: #0d47a1;
        }

        .high-school-section .summary-section {
            background: linear-gradient(135deg, #bbdefb 0%, #90caf9 100%);
            color: #0d47a1;
        }

        /* 共通スタイル */
        .overview-table, .score-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }

        .overview-table th, .overview-table td,
        .score-table th, .score-table td {
            padding: 15px 12px;
            text-align: center;
            border-bottom: 1px solid #e9ecef;
        }

        .overview-table th, .score-table th {
            color: white;
            font-weight: bold;
            font-size: 0.95rem;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }

        .overview-table td, .score-table td {
            font-size: 0.9rem;
            transition: background-color 0.3s ease;
        }

        .overview-table tbody tr:hover,
        .score-table tbody tr:hover {
            background-color: #f1f3ff;
        }

        .exam-section {
            margin-bottom: 40px;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .exam-section:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .exam-title {
            font-size: 1.4rem;
            font-weight: bold;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid;
            position: relative;
        }

        .exam-title::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 50px;
            height: 3px;
            border-radius: 2px;
        }

        .section-title {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            padding-bottom: 15px;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            border-radius: 2px;
        }

        .gender-label, .category-label {
            font-weight: bold;
            color: #333;
        }

        .na-cell {
            color: #999;
            font-style: italic;
        }

        .special-note, .summary-section {
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }

        .summary-title {
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .summary-content {
            font-size: 1rem;
            line-height: 1.6;
        }

        .footer {
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #666;
            font-size: 0.9rem;
        }

        @media (max-width: 768px) {
            .school-name {
                font-size: 2rem;
            }
            
            .exam-info {
                font-size: 1.2rem;
            }
            
            .nav-tab {
                padding: 15px 10px;
                font-size: 1rem;
            }
            
            .content {
                padding: 20px 15px;
            }
            
            .exam-section, .overview-section {
                padding: 20px 15px;
            }
            
            .overview-table th, .overview-table td,
            .score-table th, .score-table td {
                padding: 10px 8px;
                font-size: 0.85rem;
            }

            .section-title {
                font-size: 1.5rem;
            }

            .exam-title {
                font-size: 1.2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="school-name">日本大学第一中学校・高等学校</h1>
            <div class="exam-info">2025年度 入試結果</div>
        </div>

        <div class="nav-tabs">
            <button class="nav-tab middle-school active" onclick="showTab('middle-school')">
                中学入試結果
            </button>
            <button class="nav-tab high-school" onclick="showTab('high-school')">
                高校入試結果
            </button>
        </div>

        <div class="content">
            <!-- 中学入試タブ -->
            <div id="middle-school" class="tab-content active middle-school-section">
                <!-- 入試概要 -->
                <div class="overview-section">
                    <h2 class="section-title">中学入試概要（2025年度）</h2>
                    
                    <table class="overview-table">
                        <thead>
                            <tr>
                                <th>区分</th>
                                <th>①4科第1回</th>
                                <th>②4科第2回</th>
                                <th>③2科第1回</th>
                                <th>④2科第2回</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="category-header">
                                <td><strong>募集人員</strong></td>
                                <td class="highlight-number">110名</td>
                                <td class="highlight-number">50名</td>
                                <td class="highlight-number">20名</td>
                                <td class="highlight-number">20名</td>
                            </tr>
                            <tr>
                                <td><strong>出願者数</strong></td>
                                <td>246名</td>
                                <td>365名</td>
                                <td>275名</td>
                                <td>284名</td>
                            </tr>
                            <tr>
                                <td><strong>倍率</strong></td>
                                <td class="highlight-number">2.2倍</td>
                                <td class="highlight-number">7.3倍</td>
                                <td class="highlight-number">13.8倍</td>
                                <td class="highlight-number">14.2倍</td>
                            </tr>
                            <tr>
                                <td><strong>受験者数</strong></td>
                                <td>234名</td>
                                <td>193名</td>
                                <td>127名</td>
                                <td>137名</td>
                            </tr>
                            <tr>
                                <td><strong>合格者数</strong></td>
                                <td class="highlight-number">130名</td>
                                <td class="highlight-number">89名</td>
                                <td class="highlight-number">36名</td>
                                <td class="highlight-number">23名</td>
                            </tr>
                            <tr class="category-header">
                                <td><strong>実質倍率</strong></td>
                                <td class="highlight-number">1.8倍</td>
                                <td class="highlight-number">2.2倍</td>
                                <td class="highlight-number">3.5倍</td>
                                <td class="highlight-number">6.0倍</td>
                            </tr>
                        </tbody>
                    </table>

                    <table class="overview-table">
                        <thead>
                            <tr>
                                <th>男子データ</th>
                                <th>①4科第1回</th>
                                <th>②4科第2回</th>
                                <th>③2科第1回</th>
                                <th>④2科第2回</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="male-row">
                                <td><strong>出願者数</strong></td>
                                <td>158名</td>
                                <td>231名</td>
                                <td>151名</td>
                                <td>172名</td>
                            </tr>
                            <tr class="male-row">
                                <td><strong>欠席者数</strong></td>
                                <td>9名</td>
                                <td>116名</td>
                                <td>87名</td>
                                <td>86名</td>
                            </tr>
                            <tr class="male-row">
                                <td><strong>受験者数</strong></td>
                                <td>149名</td>
                                <td>115名</td>
                                <td>64名</td>
                                <td>86名</td>
                            </tr>
                            <tr class="male-row">
                                <td><strong>合格者数</strong></td>
                                <td class="highlight-number">88名</td>
                                <td class="highlight-number">60名</td>
                                <td class="highlight-number">15名</td>
                                <td class="highlight-number">13名</td>
                            </tr>
                            <tr class="male-row">
                                <td><strong>実質倍率</strong></td>
                                <td class="highlight-number">1.7倍</td>
                                <td class="highlight-number">1.9倍</td>
                                <td class="highlight-number">4.3倍</td>
                                <td class="highlight-number">6.6倍</td>
                            </tr>
                        </tbody>
                    </table>

                    <table class="overview-table">
                        <thead>
                            <tr>
                                <th>女子データ</th>
                                <th>①4科第1回</th>
                                <th>②4科第2回</th>
                                <th>③2科第1回</th>
                                <th>④2科第2回</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="female-row">
                                <td><strong>出願者数</strong></td>
                                <td>88名</td>
                                <td>134名</td>
                                <td>124名</td>
                                <td>112名</td>
                            </tr>
                            <tr class="female-row">
                                <td><strong>欠席者数</strong></td>
                                <td>3名</td>
                                <td>56名</td>
                                <td>61名</td>
                                <td>61名</td>
                            </tr>
                            <tr class="female-row">
                                <td><strong>受験者数</strong></td>
                                <td>85名</td>
                                <td>78名</td>
                                <td>63名</td>
                                <td>51名</td>
                            </tr>
                            <tr class="female-row">
                                <td><strong>合格者数</strong></td>
                                <td class="highlight-number">42名</td>
                                <td class="highlight-number">29名</td>
                                <td class="highlight-number">21名</td>
                                <td class="highlight-number">10名</td>
                            </tr>
                            <tr class="female-row">
                                <td><strong>実質倍率</strong></td>
                                <td class="highlight-number">2.0倍</td>
                                <td class="highlight-number">2.7倍</td>
                                <td class="highlight-number">3.0倍</td>
                                <td class="highlight-number">5.1倍</td>
                            </tr>
                        </tbody>
                    </table>

                    <div class="special-note">
                        <p>付属小学校からの入学者：7名（男子4名・女子3名）</p>
                    </div>
                </div>

                <!-- 合格者最低点 -->
                <div class="overview-section">
                    <h2 class="section-title">合格者最低点</h2>

                    <!-- 4科第1回 -->
                    <div class="exam-section">
                        <h3 class="exam-title">① 4科第1回</h3>
                        <table class="score-table">
                            <thead>
                                <tr>
                                    <th>性別</th>
                                    <th>国語</th>
                                    <th>算数</th>
                                    <th>社会</th>
                                    <th>理科</th>
                                    <th>総点</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="gender-male">
                                    <td class="gender-label">男</td>
                                    <td>38</td>
                                    <td>40</td>
                                    <td>14</td>
                                    <td>4</td>
                                    <td class="total-score">145</td>
                                </tr>
                                <tr class="gender-female">
                                    <td class="gender-label">女</td>
                                    <td>52</td>
                                    <td>40</td>
                                    <td>16</td>
                                    <td>7</td>
                                    <td class="total-score">149</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- 4科第2回 -->
                    <div class="exam-section">
                        <h3 class="exam-title">② 4科第2回</h3>
                        <table class="score-table">
                            <thead>
                                <tr>
                                    <th>性別</th>
                                    <th>国語</th>
                                    <th>算数</th>
                                    <th>社会</th>
                                    <th>理科</th>
                                    <th>総点</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="gender-male">
                                    <td class="gender-label">男</td>
                                    <td>43</td>
                                    <td>40</td>
                                    <td>12</td>
                                    <td>18</td>
                                    <td class="total-score">167</td>
                                </tr>
                                <tr class="gender-female">
                                    <td class="gender-label">女</td>
                                    <td>51</td>
                                    <td>35</td>
                                    <td>14</td>
                                    <td>13</td>
                                    <td class="total-score">165</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- 2科第1回 -->
                    <div class="exam-section">
                        <h3 class="exam-title">③ 2科第1回</h3>
                        <table class="score-table">
                            <thead>
                                <tr>
                                    <th>性別</th>
                                    <th>国語</th>
                                    <th>算数</th>
                                    <th>社会</th>
                                    <th>理科</th>
                                    <th>総点</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="gender-male">
                                    <td class="gender-label">男</td>
                                    <td>52</td>
                                    <td>35</td>
                                    <td class="na-cell">—</td>
                                    <td class="na-cell">—</td>
                                    <td class="total-score">104</td>
                                </tr>
                                <tr class="gender-female">
                                    <td class="gender-label">女</td>
                                    <td>48</td>
                                    <td>35</td>
                                    <td class="na-cell">—</td>
                                    <td class="na-cell">—</td>
                                    <td class="total-score">107</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- 2科第2回 -->
                    <div class="exam-section">
                        <h3 class="exam-title">④ 2科第2回</h3>
                        <table class="score-table">
                            <thead>
                                <tr>
                                    <th>性別</th>
                                    <th>国語</th>
                                    <th>算数</th>
                                    <th>社会</th>
                                    <th>理科</th>
                                    <th>総点</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="gender-male">
                                    <td class="gender-label">男</td>
                                    <td>49</td>
                                    <td>65</td>
                                    <td class="na-cell">—</td>
                                    <td class="na-cell">—</td>
                                    <td class="total-score">134</td>
                                </tr>
                                <tr class="gender-female">
                                    <td class="gender-label">女</td>
                                    <td>59</td>
                                    <td>60</td>
                                    <td class="na-cell">—</td>
                                    <td class="na-cell">—</td>
                                    <td class="total-score">134</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 高校入試タブ -->
            <div id="high-school" class="tab-content high-school-section">
                <!-- 入試概要 -->
                <div class="overview-section">
                    <h2 class="section-title">高校入試概要（2025年度）</h2>
                    
                    <table class="overview-table">
                        <thead>
                            <tr>
                                <th>項目</th>
                                <th>推薦</th>
                                <th>一般</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="category-header">
                                <td><strong>募集人員</strong></td>
                                <td class="highlight-number">75名</td>
                                <td class="highlight-number">75名</td>
                            </tr>
                            <tr>
                                <td><strong>出願者数</strong></td>
                                <td>88名</td>
                                <td>199名</td>
                            </tr>
                            <tr>
                                <td><strong>倍率</strong></td>
                                <td class="highlight-number">1.1倍</td>
                                <td class="highlight-number">2.6倍</td>
                            </tr>
                            <tr>
                                <td><strong>実質倍率</strong></td>
                                <td class="highlight-number">1.0倍</td>
                                <td class="highlight-number">1.3倍</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- 合格者最低点 -->
                <div class="overview-section">
                    <h2 class="section-title">合格者最低点</h2>

                    <div class="summary-section">
                        <div class="summary-title">一般入試 科目構成</div>
                        <div class="summary-content">
                            国語・英語・数学の3科目で実施<br>
                            A受験・B受験の2つの受験方式で募集
                        </div>
                    </div>

                    <!-- A受験 -->
                    <div class="exam-section">
                        <h3 class="exam-title">A受験</h3>
                        <table class="score-table">
                            <thead>
                                <tr>
                                    <th>性別</th>
                                    <th>国語</th>
                                    <th>英語</th>
                                    <th>数学</th>
                                    <th>総点</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="gender-male">
                                    <td class="gender-label">男子</td>
                                    <td class="highlight-score">44</td>
                                    <td class="highlight-score">62</td>
                                    <td class="highlight-score">20</td>
                                    <td class="total-score">171</td>
                                </tr>
                                <tr class="gender-female">
                                    <td class="gender-label">女子</td>
                                    <td class="highlight-score">40</td>
                                    <td class="highlight-score">71</td>
                                    <td class="highlight-score">38</td>
                                    <td class="total-score">170</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- B受験 -->
                    <div class="exam-section">
                        <h3 class="exam-title">B受験</h3>
                        <table class="score-table">
                            <thead>
                                <tr>
                                    <th>性別</th>
                                    <th>国語</th>
                                    <th>英語</th>
                                    <th>数学</th>
                                    <th>総点</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="gender-male">
                                    <td class="gender-label">男子</td>
                                    <td class="highlight-score">43</td>
                                    <td class="highlight-score">63</td>
                                    <td class="highlight-score">35</td>
                                    <td class="total-score">180</td>
                                </tr>
                                <tr class="gender-female">
                                    <td class="gender-label">女子</td>
                                    <td class="highlight-score">50</td>
                                    <td class="highlight-score">69</td>
                                    <td class="highlight-score">35</td>
                                    <td class="total-score">181</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- 総合結果 -->
                    <div class="exam-section">
                        <h3 class="exam-title">総合結果</h3>
                        <table class="score-table">
                            <thead>
                                <tr>
                                    <th>受験方式</th>
                                    <th>国語</th>
                                    <th>英語</th>
                                    <th>数学</th>
                                    <th>総点</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="category-a">
                                    <td class="category-label">A受験</td>
                                    <td class="highlight-score">40</td>
                                    <td class="highlight-score">62</td>
                                    <td class="highlight-score">20</td>
                                    <td class="total-score">170</td>
                                </tr>
                                <tr class="category-b">
                                    <td class="category-label">B受験</td>
                                    <td class="highlight-score">43</td>
                                    <td class="highlight-score">63</td>
                                    <td class="highlight-score">35</td>
                                    <td class="total-score">180</td>
                                </tr>
                                <tr class="total-row">
                                    <td class="category-label">全体最低点</td>
                                    <td class="highlight-score">40</td>
                                    <td class="highlight-score">62</td>
                                    <td class="highlight-score">20</td>
                                    <td class="total-score">170</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="summary-section">
                        <div class="summary-title">入試結果分析</div>
                        <div class="summary-content">
                            • 推薦入試は実質倍率1.0倍（全員合格）<br>
                            • 一般入試は実質倍率1.3倍と比較的合格しやすい<br>
                            • B受験の方がA受験より総点で約10点高い合格最低点<br>
                            • 数学の最低点に大きな差（A受験20点 vs B受験35点）
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>※ 上記は2025年度入試の実績データです</p>
            <p>日本大学第一中学校・高等学校 入試結果</p>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // すべてのタブコンテンツを非表示
            const allTabs = document.querySelectorAll('.tab-content');
            allTabs.forEach(tab => tab.classList.remove('active'));
            
            // すべてのナビタブからactiveクラスを削除
            const allNavTabs = document.querySelectorAll('.nav-tab');
            allNavTabs.forEach(tab => tab.classList.remove('active'));
            
            // 選択されたタブを表示
            document.getElementById(tabName).classList.add('active');
            
            // 選択されたナビタブにactiveクラスを追加
            const selectedNavTab = document.querySelector(`.nav-tab.${tabName.replace('-', '-')}`);
            selectedNavTab.classList.add('active');
        }
    </script>
</body>
</html>"""