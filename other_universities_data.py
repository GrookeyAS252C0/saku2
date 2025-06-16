# other_universities_data.py
OTHER_UNIVERSITIES_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本大学第一高等学校 2025年3月卒業生 他大学等進学状況レポート</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', 'Meiryo', sans-serif;
            line-height: 1.6;
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
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 50px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        }

        .header h1 {
            font-size: 2.8rem;
            color: #2c3e50;
            margin-bottom: 15px;
            font-weight: 700;
        }

        .header .subtitle {
            font-size: 1.4rem;
            color: #7f8c8d;
            margin-bottom: 25px;
        }

        .overview-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .overview-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            transform: translateY(0);
            transition: all 0.3s ease;
        }

        .overview-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
        }

        .overview-card .number {
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .overview-card .label {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 50px;
            margin-bottom: 30px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        }

        .section h2 {
            font-size: 2.2rem;
            color: #2c3e50;
            margin-bottom: 35px;
            text-align: center;
            position: relative;
        }

        .section h2::after {
            content: '';
            position: absolute;
            bottom: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 2px;
        }

        .section h3 {
            font-size: 1.8rem;
            color: #34495e;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }

        .university-category {
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(52, 73, 94, 0.05);
            border-radius: 20px;
            border-left: 6px solid #667eea;
        }

        .category-title {
            font-size: 1.6rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }

        .category-title::before {
            content: '';
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            margin-right: 12px;
        }

        .university-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }

        .university-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            border: 2px solid transparent;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .university-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .university-card:hover::before {
            transform: scaleX(1);
        }

        .university-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            border-color: #667eea;
        }

        .university-name {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .university-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 1.8rem;
            font-weight: 700;
            color: #667eea;
        }

        .stat-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-top: 5px;
        }

        .selection-methods {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            margin: 30px 0;
        }

        .selection-methods h3 {
            color: white;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
            text-align: center;
            margin-bottom: 30px;
        }

        .selection-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .selection-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .selection-card:hover {
            background: rgba(255, 255, 255, 0.25);
            transform: translateY(-3px);
        }

        .selection-number {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .selection-label {
            font-size: 1rem;
            opacity: 0.9;
        }

        .achievements {
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
            padding: 40px;
            border-radius: 20px;
            border-left: 6px solid #27ae60;
            margin: 30px 0;
        }

        .achievements h3 {
            color: #27ae60;
            border-bottom: 2px solid #27ae60;
            margin-bottom: 25px;
        }

        .achievement-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }

        .achievement-item {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .achievement-item h4 {
            color: #27ae60;
            font-size: 1.3rem;
            margin-bottom: 15px;
        }

        .achievement-item p {
            color: #2c3e50;
            line-height: 1.6;
        }

        .highlight-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }

        .highlight-stat {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
        }

        .highlight-stat.blue {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .highlight-stat.green {
            background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        }

        .highlight-stat.purple {
            background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
        }

        .footer {
            background: rgba(52, 73, 94, 0.95);
            color: white;
            text-align: center;
            padding: 40px;
            border-radius: 25px;
            backdrop-filter: blur(15px);
        }

        .scroll-indicator {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.2);
            z-index: 1000;
        }

        .scroll-progress {
            height: 100%;
            background: linear-gradient(45deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.1s ease;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2.2rem;
            }
            
            .overview-card .number {
                font-size: 2.8rem;
            }
            
            .container {
                padding: 15px;
            }
            
            .header, .section {
                padding: 30px 25px;
            }
            
            .university-grid {
                grid-template-columns: 1fr;
            }
        }

        .animate-on-scroll {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease;
        }

        .animate-on-scroll.animated {
            opacity: 1;
            transform: translateY(0);
        }
    </style>
</head>
<body>
    <div class="scroll-indicator">
        <div class="scroll-progress" id="scrollProgress"></div>
    </div>

    <div class="container">
        <!-- ヘッダー -->
        <header class="header animate-on-scroll">
            <h1>日本大学第一高等学校</h1>
            <div class="subtitle">2025年3月卒業生 他大学等進学状況レポート</div>
            
            <div class="overview-stats">
                <div class="overview-card">
                    <div class="number">240</div>
                    <div class="label">他大学等合格者総数</div>
                </div>
                <div class="overview-card">
                    <div class="number">75</div>
                    <div class="label">他大学進学者</div>
                </div>
                <div class="overview-card">
                    <div class="number">11</div>
                    <div class="label">併願から日本大学選択</div>
                </div>
                <div class="overview-card">
                    <div class="number">3</div>
                    <div class="label">専門学校進学者</div>
                </div>
            </div>

            <div style="margin-top: 30px; padding: 25px; background: rgba(255, 255, 255, 0.9); border-radius: 15px; border-left: 4px solid #667eea;">
                <h4 style="color: #2c3e50; margin-bottom: 15px; font-size: 1.3rem;">データの説明</h4>
                <p style="color: #2c3e50; line-height: 1.6; margin-bottom: 15px;">
                    このレポートは<strong>他大学を受験した生徒</strong>の結果を集計したものです。
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                    <div style="background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 10px;">
                        <strong style="color: #667eea;">他大学進学：75名</strong><br>
                        <small style="color: #7f8c8d;">他大学を第一志望として進学</small>
                    </div>
                    <div style="background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 10px;">
                        <strong style="color: #667eea;">日本大学選択：11名</strong><br>
                        <small style="color: #7f8c8d;">併願受験したが日本大学を選択</small>
                    </div>
                </div>
            </div>
        </header>

        <!-- 選抜方式別実績 -->
        <section class="selection-methods animate-on-scroll">
            <h3>選抜方式別実績（他大学受験者）</h3>
            <div class="selection-grid">
                <div class="selection-card">
                    <div class="selection-number">41名</div>
                    <div class="selection-label">指定校推薦<br>（他大学進学）</div>
                </div>
                <div class="selection-card">
                    <div class="selection-number">177名</div>
                    <div class="selection-label">一般選抜<br>（合格者総数）</div>
                </div>
                <div class="selection-card">
                    <div class="selection-number">29名</div>
                    <div class="selection-label">一般選抜<br>（他大学進学）</div>
                </div>
                <div class="selection-card">
                    <div class="selection-number">11名</div>
                    <div class="selection-label">公募制推薦<br>（他大学進学）</div>
                </div>
                <div class="selection-card">
                    <div class="selection-number">7名</div>
                    <div class="selection-label">総合型選抜<br>（他大学進学）</div>
                </div>
            </div>
            <p style="text-align: center; margin-top: 20px; color: rgba(255, 255, 255, 0.9); font-size: 0.95rem;">
                ※一般選抜合格177名のうち、29名が他大学進学、11名が日本大学選択、残りは日本大学専願進学
            </p>
        </section>

        <!-- 難関大学進学実績 -->
        <section class="section animate-on-scroll">
            <h2>他大学受験結果（難関大学）</h2>

            <div class="highlight-stats">
                <div class="highlight-stat blue">
                    <div class="number">15名</div>
                    <div class="label">早慶上理 合格者</div>
                </div>
                <div class="highlight-stat green">
                    <div class="number">28名</div>
                    <div class="label">MARCH 合格者</div>
                </div>
                <div class="highlight-stat purple">
                    <div class="number">25名</div>
                    <div class="label">成成明学＋学習院 合格者</div>
                </div>
            </div>

            <div style="background: rgba(255, 243, 205, 0.3); padding: 25px; border-radius: 15px; margin-bottom: 30px; border-left: 4px solid #f39c12;">
                <h4 style="color: #e67e22; margin-bottom: 15px;">🎯 併願戦略の成果</h4>
                <p style="color: #2c3e50; line-height: 1.6;">
                    多くの生徒が複数の難関大学に合格しており、選択肢を確保した上で最適な進路決定を行っています。<br>
                    <strong>合格者数 > 進学者数</strong>となっているのは、生徒が複数の選択肢の中から最も適した大学を選択できているためです。
                </p>
            </div>

            <!-- 早慶上理 -->
            <div class="university-category">
                <div class="category-title">早慶上理（早稲田・慶應・上智・東京理科）</div>
                <div class="university-grid">
                    <div class="university-card">
                        <div class="university-name">早稲田大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">4</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">1</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">慶應義塾大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">1</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">0</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">上智大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">4</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">2</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">東京理科大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">6</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">5</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- MARCH -->
            <div class="university-category">
                <div class="category-title">MARCH（明治・青山学院・立教・中央・法政）</div>
                <div class="university-grid">
                    <div class="university-card">
                        <div class="university-name">明治大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">6</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">3</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">青山学院大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">5</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">3</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">立教大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">3</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">1</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">中央大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">5</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">1</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">法政大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">9</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">3</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 理工系大学 -->
            <div class="university-category">
                <div class="category-title">理工系大学群</div>
                <div class="university-grid">
                    <div class="university-card">
                        <div class="university-name">千葉工業大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">21</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">0</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">東京工科大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">4</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">4</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">芝浦工業大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">2</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">2</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">東京電機大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">2</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">2</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 医療・薬学系 -->
            <div class="university-category">
                <div class="category-title">医療・薬学系大学</div>
                <div class="university-grid">
                    <div class="university-card">
                        <div class="university-name">星薬科大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">3</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">3</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">順天堂大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">1</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">1</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">東京薬科大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">2</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">1</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                    <div class="university-card">
                        <div class="university-name">明治薬科大学</div>
                        <div class="university-stats">
                            <div class="stat">
                                <div class="stat-number">2</div>
                                <div class="stat-label">合格者</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number">1</div>
                                <div class="stat-label">進学者</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 併願と選択の実態 -->
        <section class="section animate-on-scroll">
            <h2>併願と選択の実態</h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin-bottom: 30px;">
                <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); color: white; padding: 30px; border-radius: 20px; text-align: center;">
                    <h4 style="margin-bottom: 15px; font-size: 1.4rem;">他大学専願進学</h4>
                    <div style="font-size: 3rem; font-weight: 700; margin-bottom: 10px;">75名</div>
                    <p style="opacity: 0.9;">他大学を第一志望として進学</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%); color: white; padding: 30px; border-radius: 20px; text-align: center;">
                    <h4 style="margin-bottom: 15px; font-size: 1.4rem;">併願から日本大学選択</h4>
                    <div style="font-size: 3rem; font-weight: 700; margin-bottom: 10px;">11名</div>
                    <p style="opacity: 0.9;">他大学にも合格したが日本大学を選択</p>
                </div>
            </div>
            
            <div style="background: rgba(116, 185, 255, 0.1); padding: 25px; border-radius: 15px; border-left: 4px solid #74b9ff;">
                <h4 style="color: #0984e3; margin-bottom: 15px;">併願から日本大学を選択した11名の詳細</h4>
                <p style="color: #2c3e50; line-height: 1.6; margin-bottom: 15px;">
                    この11名は他大学（難関大学含む）にも合格しましたが、総合的な判断により日本大学を選択した生徒です。
                    これは日本大学の教育内容や環境に対する高い評価を示しています。
                </p>
                <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 15px;">
                    <strong style="color: #0984e3;">日本大学選択理由（推定）</strong>
                    <ul style="margin-top: 10px; color: #2c3e50;">
                        <li>付属校としての環境への親しみ</li>
                        <li>希望学部・学科での学習環境の良さ</li>
                        <li>進学後のサポート体制への期待</li>
                        <li>総合的な大学生活の質の評価</li>
                    </ul>
                </div>
            </div>
        </section>
        <section class="section animate-on-scroll">
            <h2>専門学校進学状況</h2>
            <div class="university-grid">
                <div class="university-card">
                    <div class="university-name">日本自動車大学校</div>
                    <div class="university-stats">
                        <div class="stat">
                            <div class="stat-number">1</div>
                            <div class="stat-label">進学者</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">総合型選抜</div>
                        </div>
                    </div>
                </div>
                <div class="university-card">
                    <div class="university-name">東京ウェディング・ブライダル</div>
                    <div class="university-stats">
                        <div class="stat">
                            <div class="stat-number">1</div>
                            <div class="stat-label">進学者</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">総合型選抜</div>
                        </div>
                    </div>
                </div>
                <div class="university-card">
                    <div class="university-name">中央工学校</div>
                    <div class="university-stats">
                        <div class="stat">
                            <div class="stat-number">1</div>
                            <div class="stat-label">進学者</div>
                        </div>
                        <div class="stat">
                            <div class="stat-label">総合型選抜</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 進路指導の成果 -->
        <section class="achievements animate-on-scroll">
            <h3>進路指導の成果とハイライト</h3>
            <div class="achievement-grid">
                <div class="achievement-item">
                    <h4>豊富な合格実績</h4>
                    <p>合格者総数240名により、多くの生徒が複数大学に合格して十分な選択肢を確保しています。</p>
                </div>
                <div class="achievement-item">
                    <h4>難関大学への確実な合格</h4>
                    <p>早慶上理、MARCH、成成明学レベルへの安定した合格実績を維持し、高い目標に挑戦する環境を提供しています。</p>
                </div>
                <div class="achievement-item">
                    <h4>理工系への強い実績</h4>
                    <p>理工系大学への合格者が多数おり、特に千葉工業大学21名合格など、工学分野での実績が顕著です。</p>
                </div>
                <div class="achievement-item">
                    <h4>効果的な併願戦略</h4>
                    <p>指定校推薦を軸としつつ一般選抜でも幅広く挑戦し、生徒が複数の選択肢から最適な進路を選択できています。</p>
                </div>
                <div class="achievement-item">
                    <h4>専門分野への対応</h4>
                    <p>医療系、薬学系、芸術系など専門性の高い分野への進学支援を行い、生徒の将来目標に応じたきめ細かい指導を実施しています。</p>
                </div>
                <div class="achievement-item">
                    <h4>適切な進路選択支援</h4>
                    <p>併願者11名が最終的に日本大学を選択するなど、生徒が複数の選択肢を比較検討した上で最適な進路決定ができています。</p>
                </div>
            </div>
        </section>

        <!-- フッター -->
        <footer class="footer">
            <p><strong>重要な注記</strong></p>
            <p>このレポートは<strong>他大学を受験した生徒</strong>の結果を集計したものです。</p>
            <p>進学者数は本年度の卒業生のみで、既卒生は含まれていません。</p>
            <p style="margin-top: 15px;">
                <strong>併願について：</strong>11名は他大学にも合格しましたが、最終的に日本大学を選択した生徒です。<br>
                これらの生徒は日本大学進学者246名に含まれます。
            </p>
            <p style="margin-top: 15px;"><strong>本レポートは令和6年度卒業生の実際の進路データに基づいて作成されています。</strong></p>
            <p>日本大学第一高等学校 進路指導部</p>
        </footer>
    </div>

    <script>
        // スクロール進捗バーの実装
        window.addEventListener('scroll', function() {
            const scrollProgress = document.getElementById('scrollProgress');
            const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
            scrollProgress.style.width = scrolled + '%';
        });

        // スクロールアニメーションの実装
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.animate-on-scroll').forEach(el => {
            observer.observe(el);
        });

        // カードのホバーエフェクト強化
        document.querySelectorAll('.university-card, .overview-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // 数字のカウントアップアニメーション
        function animateCountUp(element) {
            const target = parseInt(element.textContent);
            const duration = 1500;
            const step = target / (duration / 16);
            let current = 0;
            
            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                element.textContent = Math.floor(current) + (element.textContent.includes('名') ? '名' : '');
            }, 16);
        }

        // 数字要素が画面に入ったらカウントアップ
        const numberObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const numberElement = entry.target.querySelector('.number, .stat-number, .selection-number');
                    if (numberElement && !numberElement.classList.contains('animated')) {
                        numberElement.classList.add('animated');
                        animateCountUp(numberElement);
                    }
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.overview-card, .university-card, .selection-card').forEach(el => {
            numberObserver.observe(el);
        });
    </script>
</body>
</html>"""