# admission_guide_data.py
ADMISSION_GUIDE_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本大学第一中学校・高等学校 令和7年度 生徒募集要項</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: "Hiragino Kaku Gothic Pro", "ヒラギノ角ゴ Pro W3", "メイリオ", Meiryo, "MS ゴシック", sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            margin: 0;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #4a5568;
        }
        
        .header h1 {
            font-size: 2.4em;
            color: #4a5568;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .header .year {
            font-size: 1.4em;
            color: #4a5568;
            margin-bottom: 20px;
        }
        
        .school-info {
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #4a5568;
        }
        
        .school-tabs {
            display: flex;
            margin: 30px 0;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .tab-btn {
            flex: 1;
            padding: 20px;
            cursor: pointer;
            font-size: 1.2em;
            font-weight: bold;
            text-align: center;
            border: none;
            transition: all 0.3s ease;
        }
        
        .tab-btn.middle {
            background: #e97450;
            color: white;
        }
        
        .tab-btn.middle:hover {
            background: #dd6b20;
        }
        
        .tab-btn.middle.active {
            background: #c53030;
        }
        
        .tab-btn.high {
            background: #4299e1;
            color: white;
        }
        
        .tab-btn.high:hover {
            background: #3182ce;
        }
        
        .tab-btn.high.active {
            background: #2b6cb0;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        /* 中学校用スタイル */
        .middle-section {
            border-left: 4px solid #e97450;
        }
        
        .middle-section .section-title {
            background: #e97450;
            color: white;
            padding: 12px 20px;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        
        .middle-section .exam-table th {
            background: #fed7c7;
            color: #744210;
        }
        
        .middle-section .info-box {
            background: #fff5f0;
            border: 1px solid #fc8181;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        
        .middle-section .exam-type {
            background: #fff5f0;
            border: 2px solid #fc8181;
            border-radius: 10px;
            padding: 20px;
            margin: 30px 0;
        }
        
        .middle-section .exam-type h3 {
            color: #c53030;
            font-size: 1.4em;
            margin-bottom: 15px;
            text-align: center;
        }
        
        /* 高校用スタイル */
        .high-section {
            border-left: 4px solid #4299e1;
        }
        
        .high-section .section-title {
            background: #4299e1;
            color: white;
            padding: 12px 20px;
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        
        .high-section .exam-table th {
            background: #bee3f8;
            color: #2a4365;
        }
        
        .high-section .info-box {
            background: #ebf8ff;
            border: 1px solid #63b3ed;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        
        .high-section .exam-type {
            background: #ebf8ff;
            border: 2px solid #63b3ed;
            border-radius: 10px;
            padding: 20px;
            margin: 30px 0;
        }
        
        .high-section .exam-type h3 {
            color: #2b6cb0;
            font-size: 1.4em;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .high-section .qualification-box {
            background: #fefcbf;
            border: 1px solid #f6e05e;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        
        /* 共通スタイル */
        .section {
            margin: 30px 0;
            padding: 20px 0;
        }
        
        .exam-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .exam-table th,
        .exam-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
            vertical-align: top;
        }
        
        .exam-table th {
            font-weight: bold;
            text-align: center;
        }
        
        .fee-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        .fee-table th,
        .fee-table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }
        
        .fee-table th {
            background: #e2e8f0;
            font-weight: bold;
        }
        
        .fee-table .total-row {
            background: #f7fafc;
            font-weight: bold;
        }
        
        .fee-table .amount {
            text-align: right;
            font-weight: bold;
        }
        
        .schedule-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9em;
        }
        
        .schedule-table th,
        .schedule-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        
        .schedule-table th {
            background: #e2e8f0;
            font-weight: bold;
        }
        
        .notice {
            background: #fff5f5;
            border: 1px solid #feb2b2;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        
        .notice-title {
            color: #c53030;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .important {
            color: #c53030;
            font-weight: bold;
        }
        
        .highlight {
            background: #fef5e7;
            padding: 2px 4px;
            border-radius: 3px;
        }
        
        ul {
            margin: 15px 0 15px 30px;
        }
        
        li {
            margin: 8px 0;
        }
        
        .contact-info {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background: #f7fafc;
            border-radius: 8px;
        }
        
        .logo {
            font-size: 3em;
            font-weight: bold;
            color: #4a5568;
            margin: 20px 0;
            text-align: center;
        }
        
        .procedure-steps {
            background: #f8fafc;
            border: 1px solid #cbd5e0;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .step {
            margin: 15px 0;
            padding: 10px;
            border-left: 3px solid #4299e1;
            background: white;
        }
        
        .step-title {
            font-weight: bold;
            color: #2b6cb0;
            margin-bottom: 5px;
        }
        
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .comparison-table th {
            background: #4a5568;
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
        }
        
        .comparison-table .middle-header {
            background: #e97450;
        }
        
        .comparison-table .high-header {
            background: #4299e1;
        }
        
        .comparison-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
            vertical-align: top;
        }
        
        .comparison-table .middle-row {
            background: #fff5f0;
        }
        
        .comparison-table .high-row {
            background: #ebf8ff;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="year">令和7年度</div>
            <h1>生徒募集要項</h1>
            <h2>日本大学第一中学校・高等学校</h2>
        </div>

        <div class="school-info">
            <p><strong>〒130-0015 東京都墨田区横網1-5-2</strong></p>
            <p><strong>TEL:</strong> 03(3625)0026　<strong>FAX:</strong> 03(3625)5856</p>
            <p><strong>URL:</strong> <a href="https://www.nichidai-1.ed.jp/">https://www.nichidai-1.ed.jp/</a></p>
        </div>



        <div class="school-tabs">
            <button class="tab-btn middle active" onclick="showTab('middle')">中学校</button>
            <button class="tab-btn high" onclick="showTab('high')">高等学校</button>
        </div>

        <!-- 中学校タブ -->
        <div id="middle-content" class="tab-content active">
            <div class="middle-section">
                <div class="exam-type">
                    <h3>4科入試（第1回・第2回）</h3>
                    
                    <table class="exam-table">
                        <tr>
                            <th>入試区分</th>
                            <th>4科第1回</th>
                            <th>4科第2回</th>
                        </tr>
                        <tr>
                            <td><strong>募集人数</strong></td>
                            <td>110名（男・女）</td>
                            <td>50名（男・女）</td>
                        </tr>
                        <tr>
                            <td><strong>出願資格</strong></td>
                            <td colspan="2">令和7年3月 小学校を卒業見込みの者</td>
                        </tr>
                        <tr>
                            <td><strong>試験日</strong></td>
                            <td>令和7年2月1日（土）</td>
                            <td>令和7年2月2日（日）</td>
                        </tr>
                        <tr>
                            <td><strong>入学検定料</strong></td>
                            <td>20,000円</td>
                            <td>20,000円</td>
                        </tr>
                        <tr>
                            <td><strong>出願期間</strong></td>
                            <td>令和7年1月10日（金）〜令和7年1月31日（金）<br>出願最終日は午後1時まで</td>
                            <td>令和7年1月10日（金）〜令和7年2月1日（土）<br>出願最終日は午後1時まで</td>
                        </tr>
                        <tr>
                            <td><strong>合格発表</strong></td>
                            <td>令和7年2月1日（土）午後7時</td>
                            <td>令和7年2月2日（日）午後7時</td>
                        </tr>
                        <tr>
                            <td><strong>入学手続</strong></td>
                            <td>令和7年2月1日（土）午後7時〜2月5日（水）午後1時</td>
                            <td>令和7年2月2日（日）午後7時〜2月5日（水）午後1時</td>
                        </tr>
                    </table>

                    <div class="section-title">4科試験科目・時間割</div>
                    <table class="schedule-table">
                        <tr>
                            <th>集合</th>
                            <th>諸注意</th>
                            <th>国語<br>50分100点満点</th>
                            <th>算数<br>50分100点満点</th>
                            <th>社会<br>30分50点満点</th>
                            <th>理科<br>30分50点満点</th>
                        </tr>
                        <tr>
                            <td>8:00</td>
                            <td>8:15</td>
                            <td>8:30〜9:20</td>
                            <td>9:35〜10:25</td>
                            <td>10:40〜11:10</td>
                            <td>11:25〜11:55</td>
                        </tr>
                    </table>
                </div>

                <div class="exam-type">
                    <h3>2科入試（第1回・第2回）</h3>
                    
                    <table class="exam-table">
                        <tr>
                            <th>入試区分</th>
                            <th>2科第1回</th>
                            <th>2科第2回</th>
                        </tr>
                        <tr>
                            <td><strong>募集人数</strong></td>
                            <td>20名（男・女）</td>
                            <td>20名（男・女）</td>
                        </tr>
                        <tr>
                            <td><strong>出願資格</strong></td>
                            <td colspan="2">令和7年3月 小学校を卒業見込みの者</td>
                        </tr>
                        <tr>
                            <td><strong>試験日</strong></td>
                            <td>令和7年2月3日（月）</td>
                            <td>令和7年2月5日（水）</td>
                        </tr>
                        <tr>
                            <td><strong>入学検定料</strong></td>
                            <td>20,000円</td>
                            <td>20,000円</td>
                        </tr>
                        <tr>
                            <td><strong>出願期間</strong></td>
                            <td>令和7年1月10日（金）〜令和7年2月2日（日）<br>出願最終日は午後1時まで</td>
                            <td>令和7年1月10日（金）〜令和7年2月4日（火）<br>出願最終日は午後1時まで</td>
                        </tr>
                        <tr>
                            <td><strong>合格発表</strong></td>
                            <td>令和7年2月3日（月）午後7時</td>
                            <td>令和7年2月5日（水）午後7時</td>
                        </tr>
                        <tr>
                            <td><strong>入学手続</strong></td>
                            <td>令和7年2月3日（月）午後7時〜2月5日（水）午後1時</td>
                            <td>令和7年2月5日（水）午後7時〜2月7日（金）午後1時</td>
                        </tr>
                    </table>

                    <div class="section-title">2科試験科目・時間割</div>
                    <table class="schedule-table">
                        <tr>
                            <th>集合</th>
                            <th>諸注意</th>
                            <th>国語<br>50分100点満点</th>
                            <th>算数<br>50分100点満点</th>
                        </tr>
                        <tr>
                            <td>8:00</td>
                            <td>8:15</td>
                            <td>8:30〜9:20</td>
                            <td>9:35〜10:25</td>
                        </tr>
                    </table>
                </div>

                <div class="section">
                    <div class="section-title">中学校 出願方法</div>
                    <div class="info-box">
                        <h4>①受験生データ入力・入学検定料支払い</h4>
                        <p><strong>令和6年12月20日（金）午前0時〜</strong></p>
                        <p>本校ホームページ上のリンクから出願サイトへ移動し、入力と支払い</p>
                        
                        <h4>②受験票出力</h4>
                        <p><strong>令和7年1月10日（金）午前0時〜</strong></p>
                        <p>本校ホームページ上のリンクから出願サイトへ移動し、各自で印刷（A4サイズ）</p>
                        
                        <div class="notice">
                            <ul>
                                <li>上記の①と②をもって、出願完了となります</li>
                                <li>在籍小学校からの提出書類はありません</li>
                                <li>出願完了後、試験日まで来校していただく必要はありません</li>
                                <li class="important">顔写真データの登録が必須となります<br>
                                （受験生本人のみ／正面、上半身無帽、無背景／最近3か月以内に撮影、鮮明で影がない）</li>
                            </ul>
                        </div>

                        <div class="info-box">
                            <h4>同時出願について（中学受験のみ）</h4>
                            <ul>
                                <li>2回同時出願：30,000円</li>
                                <li>3回同時出願：40,000円</li>
                                <li>4回同時出願：50,000円</li>
                            </ul>
                            <p class="important">※出願サイトにて自動計算されます</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 高校タブ -->
        <div id="high-content" class="tab-content">
            <div class="high-section">
                <div class="exam-type">
                    <h3>推薦入試</h3>
                    
                    <table class="exam-table">
                        <tr>
                            <th>入試区分</th>
                            <th>推薦</th>
                        </tr>
                        <tr>
                            <td><strong>募集人数</strong></td>
                            <td>全日制普通科 75名（男・女）</td>
                        </tr>
                        <tr>
                            <td><strong>試験日</strong></td>
                            <td>令和7年1月22日（水）</td>
                        </tr>
                        <tr>
                            <td><strong>入学検定料</strong></td>
                            <td>20,000円</td>
                        </tr>
                        <tr>
                            <td><strong>合格発表</strong></td>
                            <td>令和7年1月22日（水）午後7時</td>
                        </tr>
                        <tr>
                            <td><strong>入学手続</strong></td>
                            <td>令和7年1月22日（水）午後7時〜1月24日（金）午後4時</td>
                        </tr>
                    </table>

                    <div class="qualification-box">
                        <h4>出願資格</h4>
                        <p>下記の①〜④の要件をすべて満たし、在籍する中学校長が推薦する者</p>
                        <ul>
                            <li><strong>①</strong> 令和7年3月中学校卒業見込みであること</li>
                            <li><strong>②</strong> 意欲的で他の生徒の模範となり、本校を単願で志望していること</li>
                            <li><strong>③</strong> 3カ年間評定に1がなく、かつ各学年の欠席日数が10日以内であること</li>
                            <li><strong>④</strong> 国語・社会・数学・理科・英語の5教科の評価合計が5段階評定で20以上であること</li>
                        </ul>
                        <p class="important">※評定は成績一覧表調査委員会提出用の「成績一覧表」による</p>
                    </div>

                    <div class="section-title">推薦入試 試験科目・時間割</div>
                    <table class="schedule-table">
                        <tr>
                            <th>集合</th>
                            <th>諸注意</th>
                            <th>適性検査／国語</th>
                            <th>適性検査／英語</th>
                            <th>適性検査／数学</th>
                            <th>面接（個別）</th>
                        </tr>
                        <tr>
                            <td>8:00</td>
                            <td>8:15</td>
                            <td>8:30〜9:00</td>
                            <td>9:15〜9:45</td>
                            <td>10:00〜10:30</td>
                            <td>11:00〜</td>
                        </tr>
                    </table>
                </div>

                <div class="exam-type">
                    <h3>一般入試</h3>
                    
                    <table class="exam-table">
                        <tr>
                            <th>入試区分</th>
                            <th>一般</th>
                        </tr>
                        <tr>
                            <td><strong>募集人数</strong></td>
                            <td>全日制普通科 75名（男・女）</td>
                        </tr>
                        <tr>
                            <td><strong>出願資格</strong></td>
                            <td>令和7年3月中学校卒業見込みの者 及び 中学校卒業者</td>
                        </tr>
                        <tr>
                            <td><strong>試験日</strong></td>
                            <td>令和7年2月10日（月）</td>
                        </tr>
                        <tr>
                            <td><strong>入学検定料</strong></td>
                            <td>20,000円</td>
                        </tr>
                        <tr>
                            <td><strong>合格発表</strong></td>
                            <td>令和7年2月10日（月）午後7時</td>
                        </tr>
                        <tr>
                            <td><strong>入学手続</strong></td>
                            <td>令和7年2月10日（月）午後7時〜2月12日（水）午後4時</td>
                        </tr>
                    </table>

                    <div class="info-box">
                        <h4>志望区分</h4>
                        <ul>
                            <li><strong>志望区分（A）：</strong>本校を第一志望とする者</li>
                            <li><strong>志望区分（B）：</strong>他校を第一志望とする者</li>
                        </ul>
                        <p class="important">※入学検定料支払い後に志望区分を変更することはできません</p>
                    </div>

                    <div class="section-title">一般入試 試験科目・時間割</div>
                    <table class="schedule-table">
                        <tr>
                            <th>集合</th>
                            <th>諸注意</th>
                            <th>国語</th>
                            <th>英語<br>（リスニングあり）</th>
                            <th>数学</th>
                            <th>面接<br>（グループ）</th>
                        </tr>
                        <tr>
                            <td>8:00</td>
                            <td>8:15</td>
                            <td>8:30〜9:20</td>
                            <td>9:35〜10:25</td>
                            <td>10:40〜11:30</td>
                            <td>11:45〜</td>
                        </tr>
                    </table>

                    <div class="info-box">
                        <h4>志望区分（B）の入学手続延期について</h4>
                        <p>公立高校を第一志望とする受験生は、出願時に入学手続延期を選択することにより、下記の日時に手続きをすることができます：</p>
                        <ul>
                            <li><strong>東京都：</strong>令和7年3月3日（月）午後4時まで</li>
                            <li><strong>千葉県：</strong>令和7年3月4日（火）午後4時まで</li>
                            <li><strong>埼玉県：</strong>令和7年3月6日（木）午後4時まで</li>
                            <li><strong>神奈川県：</strong>令和7年2月28日（金）午後4時まで</li>
                        </ul>
                    </div>
                </div>

                <div class="section">
                    <div class="section-title">高等学校 各種制度について</div>
                    
                    <div class="info-box">
                        <h4>東京都の入学支度金制度について</h4>
                        <p>私立高校入学者（保護者が都内在住）に対し、（公財）東京都私学財団より生徒1人あたり20万円（無利息3年以内で返済）を貸し付ける入学支度金制度があります。</p>
                        <p class="important">詳細は事務室までお電話にてお尋ねください。</p>
                    </div>

                    <div class="info-box">
                        <h4>日本大学第一学園奨学金制度について</h4>
                        <p>入学後、知・徳・体に優れ、学力優秀な生徒に対して、学園独自の奨学金が給付されます。</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- 共通セクション -->
        <div class="section">
            <div class="notice">
                <div class="notice-title">共通事項</div>
                <ul>
                    <li>顔写真データの登録が必須（受験生本人のみ／正面、上半身無帽、無背景／最近3か月以内に撮影、鮮明で影がない）</li>
                    <li class="important">持ち物：筆記用具、受験票（各自で印刷）※昼食・上履き不要</li>
                    <li>交通機関等の乱れにより試験開始時間を変更する場合は、本校ホームページと一斉メールにて案内（午前6時）</li>
                    <li>入学手続きのために来校していただく必要はありません</li>
                    <li>合格書類は合格発表サイトからダウンロード（本校からの郵送物はありません）</li>
                </ul>
            </div>
        </div>

        <div class="section">
            <div class="section-title">入学金・入学手続について</div>
            <div class="highlight" style="font-size: 1.2em; text-align: center; margin: 20px 0;">
                <strong>入学金：240,000円（中学・高校共通）</strong>
            </div>
            
            <div class="info-box">
                <h4>入学手続の流れ</h4>
                <ul>
                    <li>合格発表サイトから合格書類をダウンロード</li>
                    <li>入学金決済サイトから入学金の納入</li>
                    <li>入学手続き用データ入力サイトから「在学保証書・学籍簿」作成のためのデータ入力</li>
                    <li>入学金の納入方法：クレジットカード（即時支払完了）、コンビニエンスストア（入金後支払完了）</li>
                </ul>
                
                <div class="notice">
                    <div class="notice-title">重要事項</div>
                    <ul>
                        <li class="important">期間内に手続きを完了しない場合は、合格取り消しとなります</li>
                        <li>同時出願をして合格した場合には、それ以降の受験をすることができません</li>
                        <li>追加合格については個別連絡（お問い合わせには応じられません）</li>
                    </ul>
                </div>
            </div>
        </div>



        <div class="contact-info">
            <p style="font-size: 0.9em; color: #666;">
                本校の入学試験関連のデータ入力と書類提出にあたって、お知らせいただいた氏名、住所等の個人情報につきましては、<br>
                生徒募集に係る目的のみに使用し、取得目的を超えた利用及び第三者への提供はいたしません。
            </p>
        </div>
    </div>

    <script>
        function showTab(school) {
            // タブボタンの切り替え
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            if (school === 'middle') {
                document.querySelector('.tab-btn.middle').classList.add('active');
                document.getElementById('middle-content').classList.add('active');
            } else {
                document.querySelector('.tab-btn.high').classList.add('active');
                document.getElementById('high-content').classList.add('active');
            }
        }
    </script>
</body>
</html>"""