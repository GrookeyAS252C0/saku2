# nihon_university_data.py
NIHON_UNIVERSITY_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日本大学第一高等学校 2025年3月卒業生進路実績レポート</title>
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
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header .subtitle {
            font-size: 1.2rem;
            color: #7f8c8d;
            margin-bottom: 20px;
        }

        .date {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 10px 25px;
            border-radius: 25px;
            display: inline-block;
            font-weight: 600;
        }

        .overview {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .overview h2 {
            font-size: 2rem;
            color: #2c3e50;
            margin-bottom: 30px;
            text-align: center;
            position: relative;
        }

        .overview h2::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 2px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            transform: translateY(0);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(102, 126, 234, 0.3);
        }

        .stat-card .number {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .stat-card .label {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .breakdown {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .breakdown-item {
            background: rgba(52, 73, 94, 0.1);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }

        .breakdown-item .value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2c3e50;
        }

        .breakdown-item .desc {
            color: #7f8c8d;
            font-size: 0.9rem;
        }

        .section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }

        .section h3 {
            font-size: 1.8rem;
            color: #2c3e50;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #ecf0f1;
        }

        .department-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }

        .department-card {
            background: rgba(52, 73, 94, 0.05);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(52, 73, 94, 0.1);
            transition: all 0.3s ease;
        }

        .department-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            border-color: #667eea;
        }

        .department-name {
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
        }

        .department-count {
            font-size: 2.2rem;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 10px;
        }

        .department-details {
            font-size: 0.9rem;
            color: #7f8c8d;
            line-height: 1.4;
        }

        .selection-method {
            background: rgba(102, 126, 234, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }

        .selection-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .selection-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid transparent;
            transition: border-color 0.3s ease;
        }

        .selection-item:hover {
            border-color: #667eea;
        }

        .selection-count {
            font-size: 1.8rem;
            font-weight: 600;
            color: #667eea;
        }

        .selection-label {
            font-size: 0.9rem;
            color: #7f8c8d;
            margin-top: 5px;
        }

        .highlights {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 20px;
            margin-bottom: 30px;
        }

        .highlights h3 {
            font-size: 1.8rem;
            margin-bottom: 25px;
            text-align: center;
        }

        .highlight-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .highlight-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }

        .highlight-item h4 {
            font-size: 1.2rem;
            margin-bottom: 15px;
            font-weight: 600;
        }

        .highlight-item p {
            opacity: 0.9;
            line-height: 1.5;
        }

        .footer {
            background: rgba(52, 73, 94, 0.9);
            color: white;
            text-align: center;
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }
            
            .stat-card .number {
                font-size: 2.5rem;
            }
            
            .container {
                padding: 15px;
            }
            
            .header, .overview, .section, .highlights {
                padding: 25px;
            }
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
    </style>
</head>
<body>
    <div class="scroll-indicator">
        <div class="scroll-progress" id="scrollProgress"></div>
    </div>

    <div class="container">
        <!-- ヘッダー -->
        <header class="header">
            <h1>日本大学第一高等学校</h1>
            <div class="subtitle">2025年3月卒業生進路実績レポート</div>
            <div class="date">データ基準日：令和7年3月27日現在</div>
        </header>

        <!-- 全体概要 -->
        <section class="overview">
            <h2>全体概要</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="number">336</div>
                    <div class="label">卒業生総数</div>
                </div>
                <div class="stat-card">
                    <div class="number">324</div>
                    <div class="label">進学決定者数</div>
                </div>
                <div class="stat-card">
                    <div class="number">96.4%</div>
                    <div class="label">進学率</div>
                </div>
            </div>

            <h3>進路別内訳</h3>
            <div class="breakdown">
                <div class="breakdown-item">
                    <div class="value">246名 (73.2%)</div>
                    <div class="desc">日本大学進学者（総数）</div>
                </div>
                <div class="breakdown-item">
                    <div class="value">75名 (22.3%)</div>
                    <div class="desc">他大学進学者</div>
                </div>
                <div class="breakdown-item">
                    <div class="value">3名 (0.9%)</div>
                    <div class="desc">専門学校進学者</div>
                </div>
                <div class="breakdown-item">
                    <div class="value">12名 (3.6%)</div>
                    <div class="desc">進路未決定者</div>
                </div>
            </div>

            <div style="margin-top: 30px; padding: 25px; background: rgba(102, 126, 234, 0.1); border-radius: 15px; border-left: 4px solid #667eea;">
                <h4 style="color: #2c3e50; margin-bottom: 15px;">日本大学進学者246名の内訳</h4>
                <div class="breakdown" style="margin-bottom: 0;">
                    <div class="breakdown-item">
                        <div class="value">235名</div>
                        <div class="desc">日本大学専願進学者</div>
                    </div>
                    <div class="breakdown-item">
                        <div class="value">11名</div>
                        <div class="desc">他大学併願からの日本大学選択者</div>
                    </div>
                </div>
                <p style="font-size: 0.9rem; color: #7f8c8d; margin-top: 15px; text-align: center;">
                    ※11名は他大学も受験したが、最終的に日本大学を選択した生徒
                </p>
            </div>
        </section>

        <!-- 日本大学進学実績 -->
        <section class="section">
            <h3>日本大学進学実績（詳細）</h3>
            
            <div class="department-grid">
                <div class="department-card">
                    <div class="department-name">理工学部</div>
                    <div class="department-count">48名</div>
                    <div class="department-details">
                        付属特別選抜：16名<br>
                        基礎学力選抜：31名<br>
                        一般選抜：1名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">法学部</div>
                    <div class="department-count">43名</div>
                    <div class="department-details">
                        第一部：38名<br>
                        第二部：5名<br>
                        付属特別選抜・基礎学力選抜中心
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">文理学部</div>
                    <div class="department-count">32名</div>
                    <div class="department-details">
                        公募推薦：1名<br>
                        付属特別選抜：4名<br>
                        基礎学力選抜：26名<br>
                        一般選抜：1名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">経済学部</div>
                    <div class="department-count">32名</div>
                    <div class="department-details">
                        指定校推薦：1名<br>
                        付属特別選抜：6名<br>
                        基礎学力選抜：24名<br>
                        一般選抜：1名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">生産工学部</div>
                    <div class="department-count">24名</div>
                    <div class="department-details">
                        付属特別選抜：2名<br>
                        基礎学力選抜：21名<br>
                        一般選抜：1名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">生物資源科学部</div>
                    <div class="department-count">16名</div>
                    <div class="department-details">
                        付属特別選抜：5名<br>
                        基礎学力選抜：11名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">商学部</div>
                    <div class="department-count">15名</div>
                    <div class="department-details">
                        基礎学力選抜：15名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">薬学部</div>
                    <div class="department-count">9名</div>
                    <div class="department-details">
                        基礎学力選抜：7名<br>
                        一般選抜：2名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">芸術学部</div>
                    <div class="department-count">7名</div>
                    <div class="department-details">
                        総合型選抜：1名<br>
                        付属特別選抜：1名<br>
                        基礎学力選抜：4名<br>
                        一般選抜：1名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">危機管理学部</div>
                    <div class="department-count">7名</div>
                    <div class="department-details">
                        付属特別選抜：1名<br>
                        基礎学力選抜：6名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">国際関係学部</div>
                    <div class="department-count">5名</div>
                    <div class="department-details">
                        付属特別選抜：1名<br>
                        基礎学力選抜：3名<br>
                        追加募集：1名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">スポーツ科学部</div>
                    <div class="department-count">2名</div>
                    <div class="department-details">
                        公募推薦：1名<br>
                        基礎学力選抜：1名
                    </div>
                </div>
                
                <div class="department-card">
                    <div class="department-name">医学部・歯学部</div>
                    <div class="department-count">2名</div>
                    <div class="department-details">
                        医学部：1名<br>
                        歯学部：1名<br>
                        （いずれも基礎学力選抜）
                    </div>
                </div>
            </div>

            <div class="selection-method">
                <h4>選抜方式別内訳（日本大学全体）</h4>
                <div class="selection-grid">
                    <div class="selection-item">
                        <div class="selection-count">191名</div>
                        <div class="selection-label">基礎学力選抜<br>(56.8%)</div>
                    </div>
                    <div class="selection-item">
                        <div class="selection-count">42名</div>
                        <div class="selection-label">付属特別選抜<br>(12.5%)</div>
                    </div>
                    <div class="selection-item">
                        <div class="selection-count">7名</div>
                        <div class="selection-label">一般選抜<br>(2.1%)</div>
                    </div>
                    <div class="selection-item">
                        <div class="selection-count">4名</div>
                        <div class="selection-label">その他<br>(1.2%)</div>
                    </div>
                </div>
            </div>

            <h4>日本大学短期大学部進学者：4名</h4>
            <div class="breakdown">
                <div class="breakdown-item">
                    <div class="value">2名</div>
                    <div class="desc">三島（商経）</div>
                </div>
                <div class="breakdown-item">
                    <div class="value">2名</div>
                    <div class="desc">船橋（建築、もの、生命）</div>
                </div>
            </div>
        </section>

        <!-- 他大学進学実績 -->
        <section class="section">
            <h3>他大学進学実績</h3>
            <div class="stat-card" style="margin-bottom: 20px;">
                <div class="number">75名</div>
                <div class="label">他大学進学者総計（22.3%）</div>
            </div>

            <h4>選抜方式別内訳</h4>
            <div class="selection-grid">
                <div class="selection-item">
                    <div class="selection-count">40名</div>
                    <div class="selection-label">指定校推薦<br>(11.9%)</div>
                </div>
                <div class="selection-item">
                    <div class="selection-count">22名</div>
                    <div class="selection-label">一般入試<br>(6.5%)</div>
                </div>
                <div class="selection-item">
                    <div class="selection-count">7名</div>
                    <div class="selection-label">公募制推薦<br>(2.1%)</div>
                </div>
                <div class="selection-item">
                    <div class="selection-count">6名</div>
                    <div class="selection-label">総合型入試<br>(1.8%)</div>
                </div>
            </div>
        </section>

        <!-- 特徴とハイライト -->
        <section class="highlights">
            <h3>進路指導の成果とハイライト</h3>
            <div class="highlight-grid">
                <div class="highlight-item">
                    <h4>高い進学率</h4>
                    <p>全卒業生の96.4%が進学を決定し、充実した進路指導の成果が表れています。</p>
                </div>
                <div class="highlight-item">
                    <h4>理工系学部への強い実績</h4>
                    <p>理工学部48名、生産工学部24名と、工学系分野での進学者が際立って多く、理系教育の充実を示しています。</p>
                </div>
                <div class="highlight-item">
                    <h4>多様な進路選択</h4>
                    <p>日本大学内でも文系から理系、医歯薬系まで幅広い学部への進学実績があり、生徒の多様な進路希望に対応しています。</p>
                </div>
                <div class="highlight-item">
                    <h4>付属校の特色活用</h4>
                    <p>基礎学力選抜を中心とした内部進学制度により、73.2%の生徒が日本大学に進学し、付属校としての特色を最大限活用しています。</p>
                </div>
            </div>
        </section>

        <!-- フッター -->
        <footer class="footer">
            <p><strong>本レポートは令和6年度卒業生の実際の進路データに基づいて作成されています。</strong></p>
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

        // カードのホバーエフェクト強化
        document.querySelectorAll('.department-card, .stat-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // スムーズスクロール
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>"""