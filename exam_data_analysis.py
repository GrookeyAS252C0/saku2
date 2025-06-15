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
            color: #2c3e50;
            font-size: 2.2rem;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .header .description {
            color: #7f8c8d;
            font-size: 1.1rem;
            margin-bottom: 20px;
            line-height: 1.6;
        }

        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }

        .stat-box {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stat-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        }

        .stat-box h3 {
            color: #2c3e50;
            font-size: 1.5rem;
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }

        .middle-school .stat-box h3 {
            border-bottom-color: #f39c12;
        }

        .high-school .stat-box h3 {
            border-bottom-color: #3498db;
        }

        .trend-section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .trend-section h3 {
            color: #2c3e50;
            font-size: 1.6rem;
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 3px solid #e74c3c;
            padding-bottom: 10px;
        }

        .trend-data {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }

        .trend-item {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border-left: 5px solid #3498db;
        }

        .middle-school .trend-item {
            border-left-color: #f39c12;
        }

        .high-school .trend-item {
            border-left-color: #3498db;
        }

        .trend-item .label {
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 10px;
            font-weight: 500;
        }

        .trend-item .value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }

        .trend-item .change {
            font-size: 0.85rem;
            font-weight: 500;
        }

        .trend-item .change.increase {
            color: #e74c3c;
        }

        .trend-item .change.decrease {
            color: #27ae60;
        }

        .private-schools-section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .private-schools-section h3 {
            color: #2c3e50;
            font-size: 1.6rem;
            margin-bottom: 20px;
            text-align: center;
            border-bottom: 3px solid #9b59b6;
            padding-bottom: 10px;
        }

        .schools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .school-item {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            border: 2px solid #ecf0f1;
            transition: all 0.3s ease;
        }

        .school-item:hover {
            background: #e8f4f8;
            border-color: #3498db;
            transform: translateY(-2px);
        }

        .school-item .name {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 0.95rem;
        }

        .school-item .deviation {
            color: #7f8c8d;
            font-size: 0.85rem;
        }

        .highlight-box {
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
            text-align: center;
            box-shadow: 0 10px 30px rgba(116, 185, 255, 0.3);
        }

        .middle-school .highlight-box {
            background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
            box-shadow: 0 10px 30px rgba(253, 203, 110, 0.3);
        }

        .highlight-box h4 {
            font-size: 1.3rem;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .highlight-box p {
            font-size: 1rem;
            line-height: 1.6;
            opacity: 0.95;
        }

        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
        }

        .comparison-table th,
        .comparison-table td {
            padding: 15px 12px;
            text-align: center;
            border-bottom: 1px solid #e9ecef;
        }

        .comparison-table th {
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            font-weight: bold;
            font-size: 0.95rem;
        }

        .middle-school .comparison-table th {
            background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        }

        .comparison-table td {
            font-size: 0.9rem;
            transition: background-color 0.3s ease;
        }

        .comparison-table tbody tr:hover {
            background-color: #f1f3ff;
        }

        .comparison-table .year-column {
            font-weight: bold;
            background: #f8f9fa;
        }

        .note-section {
            background: rgba(255, 243, 196, 0.8);
            border-left: 5px solid #f39c12;
            border-radius: 10px;
            padding: 20px;
            margin: 30px 0;
        }

        .note-section h4 {
            color: #d68910;
            font-size: 1.1rem;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .note-section p {
            color: #7d6608;
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 8px;
        }

        @media (max-width: 768px) {
            .main-header h1 {
                font-size: 2.2rem;
            }

            .header h2 {
                font-size: 1.8rem;
            }

            .stats-container {
                grid-template-columns: 1fr;
                gap: 20px;
            }

            .trend-data {
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
            }

            .schools-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 10px;
            }

            .tab-button {
                padding: 12px 20px;
                font-size: 1rem;
            }

            .comparison-table th,
            .comparison-table td {
                padding: 10px 8px;
                font-size: 0.85rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="main-header">
            <h1>日本大学第一中学校・高等学校</h1>
            <div class="subtitle">2025年度 受験生動向データ分析</div>
        </div>

        <div class="tab-container">
            <button class="tab-button middle-school active" onclick="showTab('middle-school')">
                中学校データ分析
            </button>
            <button class="tab-button high-school" onclick="showTab('high-school')">
                高校データ分析
            </button>
        </div>

        <!-- 中学校データ分析タブ -->
        <div id="middle-school" class="tab-content active middle-school">
            <div class="header">
                <h2>中学入試 受験生動向分析</h2>
                <div class="description">
                    2025年度中学入試における受験生の動向、偏差値推移、および近隣私立校との比較データを分析しています。
                </div>
            </div>

            <div class="stats-container">
                <div class="stat-box">
                    <h3>2025年度入試結果サマリー</h3>
                    <div class="trend-data">
                        <div class="trend-item">
                            <div class="label">総出願者数</div>
                            <div class="value">1,170</div>
                            <div class="change increase">前年比 +128名</div>
                        </div>
                        <div class="trend-item">
                            <div class="label">総合格者数</div>
                            <div class="value">278</div>
                            <div class="change increase">前年比 +24名</div>
                        </div>
                        <div class="trend-item">
                            <div class="label">平均実質倍率</div>
                            <div class="value">3.4倍</div>
                            <div class="change increase">前年比 +0.3倍</div>
                        </div>
                    </div>
                </div>

                <div class="stat-box">
                    <h3>受験方式別動向</h3>
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>受験方式</th>
                                <th>出願者数</th>
                                <th>実質倍率</th>
                                <th>前年比</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="year-column">4科第1回</td>
                                <td>246名</td>
                                <td>1.8倍</td>
                                <td class="change increase">+15名</td>
                            </tr>
                            <tr>
                                <td class="year-column">4科第2回</td>
                                <td>365名</td>
                                <td>2.2倍</td>
                                <td class="change increase">+42名</td>
                            </tr>
                            <tr>
                                <td class="year-column">2科第1回</td>
                                <td>275名</td>
                                <td>3.5倍</td>
                                <td class="change increase">+38名</td>
                            </tr>
                            <tr>
                                <td class="year-column">2科第2回</td>
                                <td>284名</td>
                                <td>6.0倍</td>
                                <td class="change increase">+33名</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="trend-section">
                <h3>偏差値・難易度分析</h3>
                <div class="highlight-box">
                    <h4>2025年度 予想偏差値レンジ</h4>
                    <p>4科受験：42-45（四谷大塚基準）<br>
                    2科受験：44-47（四谷大塚基準）<br>
                    ※2科受験の方が若干高い偏差値が必要</p>
                </div>

                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>年度</th>
                            <th>4科偏差値</th>
                            <th>2科偏差値</th>
                            <th>総出願者数</th>
                            <th>実質倍率</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="year-column">2025年</td>
                            <td>42-45</td>
                            <td>44-47</td>
                            <td>1,170名</td>
                            <td>3.4倍</td>
                        </tr>
                        <tr>
                            <td class="year-column">2024年</td>
                            <td>41-44</td>
                            <td>43-46</td>
                            <td>1,042名</td>
                            <td>3.1倍</td>
                        </tr>
                        <tr>
                            <td class="year-column">2023年</td>
                            <td>40-43</td>
                            <td>42-45</td>
                            <td>987名</td>
                            <td>2.9倍</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="private-schools-section">
                <h3>近隣私立中学校との偏差値比較</h3>
                <div class="schools-grid">
                    <div class="school-item">
                        <div class="name">日本大学第一</div>
                        <div class="deviation">42-47</div>
                    </div>
                    <div class="school-item">
                        <div class="name">日本大学第二</div>
                        <div class="deviation">45-49</div>
                    </div>
                    <div class="school-item">
                        <div class="name">日本大学第三</div>
                        <div class="deviation">46-50</div>
                    </div>
                    <div class="school-item">
                        <div class="name">桜美林</div>
                        <div class="deviation">40-44</div>
                    </div>
                    <div class="school-item">
                        <div class="name">多摩大学聖ヶ丘</div>
                        <div class="deviation">38-42</div>
                    </div>
                    <div class="school-item">
                        <div class="name">帝京大学</div>
                        <div class="deviation">39-43</div>
                    </div>
                    <div class="school-item">
                        <div class="name">明星</div>
                        <div class="deviation">41-45</div>
                    </div>
                    <div class="school-item">
                        <div class="name">八王子学園八王子</div>
                        <div class="deviation">44-48</div>
                    </div>
                </div>
            </div>

            <div class="note-section">
                <h4>📊 中学入試 分析ポイント</h4>
                <p>• 2科受験は4科受験より偏差値が2-3ポイント高く、競争が激化</p>
                <p>• 第2回入試（2月回）は第1回より実質倍率が大幅に上昇</p>
                <p>• 付属小学校からの進学者は7名と少数で、外部受験生が主体</p>
                <p>• 近隣私立校の中では中堅レベルの位置づけを維持</p>
            </div>
        </div>

        <!-- 高校データ分析タブ -->
        <div id="high-school" class="tab-content high-school">
            <div class="header">
                <h2>高校入試 受験生動向分析</h2>
                <div class="description">
                    2025年度高校入試における受験生の動向、偏差値推移、および都内私立校との比較データを分析しています。
                </div>
            </div>

            <div class="stats-container">
                <div class="stat-box">
                    <h3>2025年度入試結果サマリー</h3>
                    <div class="trend-data">
                        <div class="trend-item">
                            <div class="label">総出願者数</div>
                            <div class="value">287</div>
                            <div class="change decrease">前年比 -23名</div>
                        </div>
                        <div class="trend-item">
                            <div class="label">推薦合格者数</div>
                            <div class="value">88</div>
                            <div class="change increase">前年比 +5名</div>
                        </div>
                        <div class="trend-item">
                            <div class="label">一般実質倍率</div>
                            <div class="value">1.3倍</div>
                            <div class="change decrease">前年比 -0.1倍</div>
                        </div>
                    </div>
                </div>

                <div class="stat-box">
                    <h3>入試方式別動向</h3>
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>入試方式</th>
                                <th>出願者数</th>
                                <th>実質倍率</th>
                                <th>前年比</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="year-column">推薦入試</td>
                                <td>88名</td>
                                <td>1.0倍</td>
                                <td class="change increase">+5名</td>
                            </tr>
                            <tr>
                                <td class="year-column">一般入試</td>
                                <td>199名</td>
                                <td>1.3倍</td>
                                <td class="change decrease">-28名</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="trend-section">
                <h3>偏差値・難易度分析</h3>
                <div class="highlight-box">
                    <h4>2025年度 予想偏差値レンジ</h4>
                    <p>推薦入試：内申基準 3.8以上（9科）<br>
                    一般入試：55-58（Vもぎ基準）<br>
                    ※A受験・B受験の2方式で実施</p>
                </div>

                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>年度</th>
                            <th>一般偏差値</th>
                            <th>推薦内申基準</th>
                            <th>総出願者数</th>
                            <th>実質倍率</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="year-column">2025年</td>
                            <td>55-58</td>
                            <td>3.8/5.0</td>
                            <td>287名</td>
                            <td>1.3倍</td>
                        </tr>
                        <tr>
                            <td class="year-column">2024年</td>
                            <td>56-59</td>
                            <td>3.9/5.0</td>
                            <td>310名</td>
                            <td>1.4倍</td>
                        </tr>
                        <tr>
                            <td class="year-column">2023年</td>
                            <td>57-60</td>
                            <td>4.0/5.0</td>
                            <td>295名</td>
                            <td>1.5倍</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="private-schools-section">
                <h3>都内私立高校との偏差値比較</h3>
                <div class="schools-grid">
                    <div class="school-item">
                        <div class="name">日本大学第一</div>
                        <div class="deviation">55-58</div>
                    </div>
                    <div class="school-item">
                        <div class="name">日本大学第二</div>
                        <div class="deviation">58-61</div>
                    </div>
                    <div class="school-item">
                        <div class="name">日本大学第三</div>
                        <div class="deviation">59-62</div>
                    </div>
                    <div class="school-item">
                        <div class="name">日本大学豊山</div>
                        <div class="deviation">56-59</div>
                    </div>
                    <div class="school-item">
                        <div class="name">桜美林</div>
                        <div class="deviation">52-55</div>
                    </div>
                    <div class="school-item">
                        <div class="name">多摩大学聖ヶ丘</div>
                        <div class="deviation">48-52</div>
                    </div>
                    <div class="school-item">
                        <div class="name">帝京大学</div>
                        <div class="deviation">50-54</div>
                    </div>
                    <div class="school-item">
                        <div class="name">明星</div>
                        <div class="deviation">53-57</div>
                    </div>
                    <div class="school-item">
                        <div class="name">八王子学園八王子</div>
                        <div class="deviation">54-58</div>
                    </div>
                    <div class="school-item">
                        <div class="name">拓殖大学第一</div>
                        <div class="deviation">57-60</div>
                    </div>
                    <div class="school-item">
                        <div class="name">東京農業大学第一</div>
                        <div class="deviation">62-65</div>
                    </div>
                    <div class="school-item">
                        <div class="name">成城学園</div>
                        <div class="deviation">60-63</div>
                    </div>
                </div>
            </div>

            <div class="note-section">
                <h4>📊 高校入試 分析ポイント</h4>
                <p>• 推薦入試は実質全員合格で、内申基準をクリアすれば合格可能性が高い</p>
                <p>• 一般入試は実質倍率1.3倍と比較的合格しやすい水準を維持</p>
                <p>• B受験はA受験より合格最低点が約10点高く、難易度差がある</p>
                <p>• 日本大学系列校の中では中堅校の位置づけ</p>
                <p>• 近年偏差値が若干下降傾向で、受験しやすくなっている</p>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // すべてのタブコンテンツを非表示
            const allTabs = document.querySelectorAll('.tab-content');
            allTabs.forEach(tab => tab.classList.remove('active'));
            
            // すべてのタブボタンからactiveクラスを削除
            const allButtons = document.querySelectorAll('.tab-button');
            allButtons.forEach(button => button.classList.remove('active'));
            
            // 選択されたタブを表示
            document.getElementById(tabName).classList.add('active');
            
            // 選択されたボタンにactiveクラスを追加
            const selectedButton = document.querySelector(`.tab-button.${tabName.replace('-', '-')}`);
            selectedButton.classList.add('active');
        }
    </script>
</body>
</html>"""