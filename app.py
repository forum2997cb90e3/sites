from flask import Flask, render_template_string, request, jsonify, session, redirect
import time
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

MONGO_URI = "mongodb+srv://admin:123456qwerty@cluster0.mvdyb6h.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["bot"]

logs_collection = db["logs"]
bans_collection = db["bans"]
users_collection = db["users"]
clickers_collection = db["clickers"]
business_collection = db["business"]
site_access_collection = db["site_access"]
auth_logs_collection = db["auth_logs"]

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Вход</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background: #111;
            position: relative;
        }

        body::before {
            content: "";
            position: fixed;
            inset: -20%;

            background:
                repeating-conic-gradient(
                    from 0deg,
                    rgba(255,255,255,0.03) 0deg 10deg,
                    rgba(0,0,0,0) 10deg 20deg
                );

            border-radius: 50%;
            transform: scale(1.5);
            filter: blur(2px);
            opacity: 0.25;

            z-index: -2;
        }

        body::after {
            content: "";
            position: fixed;
            inset: 0;

            background: rgba(0,0,0,0.55);
            z-index: -1;
        }

        .login-wrap {
            width: 100%;
            max-width: 470px;
            padding: 20px;
            position: relative;
            z-index: 2;
        }

        .login-card {
            position: relative;
            background: rgba(26, 26, 32, 0.82);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 28px;
            padding: 95px 34px 28px;
            box-shadow:
                0 20px 50px rgba(0,0,0,0.45),
                inset 0 1px 0 rgba(255,255,255,0.05);
            backdrop-filter: blur(16px);
        }

        .login-icon-box {
            position: absolute;
            top: -52px;
            left: 50%;
            transform: translateX(-50%);
            width: 170px;
            height: 110px;
            border-radius: 26px;
            background: rgba(35, 35, 35, 0.95);
            border: 1px solid rgba(255,255,255,0.08);
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow:
                0 12px 30px rgba(0,0,0,0.45),
                0 0 25px rgba(255, 180, 90, 0.15);
        }

        .login-icon {
            font-size: 42px;
            color: #f2f2f2;
            text-shadow: 0 0 16px rgba(255,255,255,0.12)
        }

        .lock {
            margin-left: 8px;
            color: #ffc57a;
            text-shadow: 0 0 14px rgba(255, 197, 122, 0.45)
        }

        .login-title {
            text-align: center;
            font-size: 54px;
            font-weight: bold;
            color: #f3ece7;
            margin: 0 0 30px 0;
            letter-spacing: 1px;
            text-shadow: 0 0 20px rgba(255,255,255,0.08);
        }

        .input-box {
            position: relative;
            margin-bottom: 18px;
        }

        .input-box span {
            position: absolute;
            left: 18px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 20px;
            color: rgba(255,255,255,0.65);
            pointer-events: none;
        }

        .input-box input {
            width: 100%;
            height: 62px;
            border: 1px solid rgba(255,255,255,0.08);
            outline: none;
            border-radius: 18px;
            background: rgba(20,20,26,0.78);
            color: #fff;
            font-size: 17px;
            padding: 0 18px 0 54px;
            box-shadow: inset 0 1px 4px rgba(0,0,0,0.35);
            transition: 0.25s ease;
        }

        .input-box input::placeholder {
            color: rgba(255,255,255,0.35);
        }

        .input-box input:focus {
            border-color: rgba(255, 187, 102, 0.7);
            box-shadow:
                0 0 18px rgba(255, 187, 102, 0.20),
                inset 0 1px 4px rgba(0,0,0,0.35);
        }

        .login-btn {
            width: 100%;
            height: 64px;
            border: none;
            border-radius: 20px;
            margin-top: 14px;
            cursor: pointer;
            font-size: 20px;
            font-weight: bold;
            color: #fff4ea;
            background: linear-gradient(135deg, rgba(40,40,50,0.96), rgba(58,46,42,0.96));
            box-shadow:
                0 0 0 1px rgba(255,255,255,0.06),
                0 0 24px rgba(255, 174, 84, 0.18);
            transition: 0.25s ease;
        }

        .login-btn:hover {
            transform: translateY(-1px);
            box-shadow:
                0 0 0 1px rgba(255,255,255,0.08),
                0 0 30px rgba(255, 174, 84, 0.28);
        }

        .login-btn:active {
            transform: scale(0.985);
        }

        #error {
            min-height: 24px;
            margin-top: 18px;
            text-align: left;
            color: #ff9d8c;
            font-size: 16px;
            padding-left: 4px;
        }

        @media (max-width: 600px) {
            .login-title {
                font-size: 40px;
            }

            .login-card {
                padding: 85px 20px 24px;
                border-radius: 22px;
            }

            login-icon-box {
                width: 145px;
                height: 95px;
            }
        }
    </style>
</head>
<body>

    <div class="login-wrap">
        <div class="login-card">
            <div class="login-icon-box">
                <div class="login-icon">👤<span class="lock">🔒</span></div>
            </div>

            <h1 class="login-title">Вход</h1>

            <div class="input-box">
                <span>👤</span>
                <input id="username" placeholder="Username" autocomplete="username">
            </div>

            <div class="input-box">
                <span>🔒</span>
                <input id="password" type="password" placeholder="Password" autocomplete="current-password">
            </div>

            <button class="login-btn" onclick="login()">Войти</button>

            <p id="error"></p>
        </div>
    </div>

<script>
    function login() {
        fetch("/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: document.getElementById("username").value,
                password: document.getElementById("password").value
            })
        })
        .then(r => r.json())
        .then(d => {
            if (d.success) {
                location.href = "/";
            } else {
                document.getElementById("error").innerText = d.message;
            }
        })
    }
</script>

</body>
</html>
"""

BLOCKED_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Доступ ограничен</title>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0f1115, #1b1f27, #121418);
            color: white;
            padding: 20px;
        }

        .box {
            width: 100%;
            max-width: 560px;
            background: rgba(20, 20, 28, 0.92);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.45);
            text-align: center;
        }

        .icon {
            font-size: 56px;
            margin-bottom: 14px;
        }

        .title {
            font-size: 32px;
            font-weight: bold;
            color: #ff8f8f;
            margin-bottom: 16px;
        }

        .reason {
            font-size: 18px;
            color: #f1f1f1;
            background: rgba(255,255,255,0.05);
            border-radius: 14px;
            padding: 16px;
            margin-top: 18px;
        }

        .btn {
            margin-top: 24px;
            display: inline-block;
            padding: 12px 18px;
            border-radius: 12px;
            text-decoration: none;
            color: white;
            background: #dc3545;
        }
    </style>
</head>
<body>
    <div class="box">
        <div class="icon">⛔</div>
        <div class="title">Доступ к сайту ограничен</div>
        <div>Обратись к владельцу или к старшей администрации</div>
        <div class="reason">
            <b>Причина:</b> {{ reason }}
        </div>
        <a class="btn" href="/logout">Выйти</a>
    </div>
</body>
</html>
"""

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Логи Админов</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { 
            font-family: Arial;
            margin: 10px;
            position: relative;
            z-index: 0;
            min-height: 100vh;
            background: transparent;
        }

        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background: url("/static/bg.png") no-repeat center center;
            background-size: cover;
            filter: brightness(0.35) blur(2px);
            z-index: -2;
        }

        body::after {
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.35);
            z-index: -1;
        }
        
        h1 { 
            text-align: center;
        }
        
        .menu-btn {
            position: fixed;
            top: 12px;
            left: 12px;
            width: 70px;
            height: 70px;
            border: none;
            border-radius: 22px;
            background: linear-gradient(145deg, #0c1118, #121922);
            cursor: pointer;
            z-index: 1000;
            overflow: hidden;
        }
        
        .menu-btn::before {
            content: "";
            position: absolute;
            inset: -2px;
            border-radius: 22px;
            background: linear-gradient(45deg, #ffb300, #ff6a00, #ffb300);
            filter: blur(8px);
            opacity: 0.6;
            z-index: 0;
        }
        
        .menu-btn::after {
            content: "";
            position: absolute;
            inset: 2px;
            background: #0f141d;
            border-radius: 20px;
            z-index: 1;
        }
        
        .menu-btn:hover {
            box-shadow: 0 0 24px rgba(255, 170, 0, 0.28);
        }
        
        .menu-btn:active {
            transform: scale(0.96);
        }
        
        .menu-btn span {
            position: absolute;
            left: 50%;
            width: 32px;
            height: 4px;
            background: linear-gradient(90deg, #ffcc00, #ff9900);
            transform: translateX(-50%);
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(255, 200, 0, 0.9);
            z-index: 3;
        }
        
        .menu-btn span:nth-child(1) {
            top: 20px;
        }
        
        .menu-btn span:nth-child(2) {
            top: 32px;
        }
        
        .menu-btn span:nth-child(3) {
            top: 44px;
        }
        
        .menu-btn:hover::before {
            opacity: 1;
            filter: blur(12px);
        }
        
        .user-card {
            background: #ffffff;
            font-size: 16px;
        }
        
        .sidebar {
            position: fixed;
            top: 0;
            left: -290px;
            width: 250px;
            height: 100%;
            background: #222;
            color: white;
            padding: 60px 20px 20px 20px;
            transition: 0.3s;
            z-index: 999;
        }

        .sidebar.active {
            left: 0;
        }

        .sidebar h2 {
            margin-top: 0;
        }

        .sidebar a {
            display: block;
            color: white;
            text-decoration: none;
            margin: 10px 0;
            padding: 8px;
            border-radius: 5px;
            background: #333;
        }

        .sidebar a:hover {
            background: #555;
        }

        .overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            display: none;
            z-index: 998;
        }

        .overlay.active {
            display: block;
        }

        .card { 
            background: rgba(255,255,255,0.90);
            backdrop-filter: blur(6px);
            padding: 10px 15px;
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0.25);
            text-align: left;
            font-weight: normal;
        }

        .bold { 
            font-weight: bold; 
        }

        .refresh { 
            display: flex; 
            justify-content: center; 
            margin-bottom: 15px; 
        }

        .refresh a { 
            padding: 5px 10px; 
            font-size: 14px; 
            text-decoration: none; 
            color: #fff; 
            background: #28a745; 
            border-radius: 5px; 
        }

        #logs-section {
            text-align: center;
        }

        .cards-container {
            text-align: left;
            max-width: 950px;
            margin: 0 auto;
        }

        .card.ban {
            background-color: #ff4d4d;
            text-align: left;
            font-weight: normal;
            font-size: 18px;
            padding: 15px 20px;
        }

        .card.unban {
            background-color: #4dff4d;
            text-align: left;
            font-weight: normal;
            font-size: 18px;
            padding: 15px 20px;
        }

        .card.other {
            background-color: #fff3b0;
            text-align: left;
            font-weight: normal;
        }

        #bans-section {
            display: none;
            text-align: center;
            max-width: 600px;
            margin: 50px auto;
            font-weight: bold;
            font-size:20px
        }

        .btn-unban {
            padding: 5px 10px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-left: 10px
        }

        .confirm-popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
            display: none;
            z-index: 2000;
            text-align: center;
        }

        .confirm-popup button {
            margin: 5px;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 5px;
        }
        
        #admin-panel-section {
            display: none;
            text-align: center;
            max-width: 700px;
            margin: 50px auto;
        }
        
        .admin-panel-box {
            background: rgba(255,255,255,0.92);
            backdrop-filter: blur(6px);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.25);
        }
        
        .admin-panel-box input {
            width: 100%;
            max-width: 400px;
            padding: 10px;
            font-size: 16px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        
        .admin-panel-box button {
            padding: 10px 16px;
            font-size: 16px;
            border: none;
            border-radius: 6px;
            background: #007bff;
            color: white;
            cursor: pointer;
        }
        
        .admin-panel-result {
            margin-top: 20px;
            font-size: 18px;
            word-break: break-all;
        }
        
        .admin-link:hover {
            color: #007bff;
            border-bottom-color: #007bff;   
        }
        
        .copy-id-box {
            margin-top: 10px;
            display: inline-flex;
            gap: 10px;
            align-items: center;
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .copy-id-box input {
            max-width: 250px;
            margin: 0;
            text-align: center;
            font-weight: bold;
        }

        .notification {
            position: fixed;
            top: 10px;
            right: 10px;
            background: #28a745;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            display: none;
            z-index: 3000;
        }
        
        .admin-link {
            color: inherit;
            text-decoration: none;
            border-bottom: 1px dashed rgba(0,0,0,0.4);
        }

        .ban-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .admin-card {
            color: white;
            font-size: 18px;
            padding: 15px 20px;
        }
        
        .admin-lvl-5 {
            background-color: #ff4d4d;
        }
        
        .admin-lvl-4 {
            background-color: #ffd633;
        }
        
        .admin-lvl-3 {
            background-color: #007bff;
        }
        
        .admin-lvl-2 {
            background-color: #66ccff;
            color: black;
        }
        
        .admin-lvl-1 {
            background-color: #222222
        }

        .admin-me {
            position: relative;
            overflow: hidden;
        }

        .admin-me::before {
            content: "";
            position: absolute;
            inset: -2px;
            background: linear-gradient(
                45deg,
                red,
                orange,
                yellow,
                green,
                cyan,
                blue,
                violet,
                red
            );
            background-size: 400%;
            animation: rainbow 6s linear infinite;
            filter: blur(8px);
            z-index: 0;
        }

        .admin-me::after {
            content: "";
            position: absolute;
            inset: 2px;
            background: inherit;
            border-radius: 8px;
            z-index: 1;
        }

        .admin-me * {
            position: relative;
            z-index: 2;
        }

        @keyframes rainbow {
            0% { background-position: 0% }
            100% { background-position: 400% }
        }

        .you-label {
            color: #00ff88;
            font-weight: bold;
            margin-left: 8px;
            font-size: 14px;
        }
        
        #admins-section {
            display: none;
            text-align: center;
        }
        
        .admins-container {
            text-align: left;
            max-width: 700px;
            margin: 0 auto;
        }
        
        .btn-delete {
            padding: 8px 12px;
            background: #111;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .user-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .btn-ban {
            padding: 8px 12px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .user-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 15px;
        }
        
        .ban-popup textarea {
            width: 100%;
            height: 80px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <button class="menu-btn" onclick="toggleMenu()">
        <span></span>
        <span></span>
        <span></span>
    </button>

    <div id="sidebar" class="sidebar">
        <h2>Меню</h2>

        {% if session.get('lvl', 0) >= 3 %}
            <a href="javascript:void(0)" onclick="showSection('logs')">📜 Админ логи</a>
        {% endif %}

        <a href="javascript:void(0)" onclick="showSection('bans')">🚫 Список банов</a>
        <a href="javascript:void(0)" onclick="showSection('admins')">👮 Список администраторов</a>
        <a href="javascript:void(0)" onclick="showSection('users')">👤 Список пользователей</a>

        {% if session.get('lvl', 0) >= 3 %}
            <a href="javascript:void(0)" onclick="showSection('admin-panel')">⚙️ Админ панель</a>
        {% endif %}

        {% if session.get('lvl', 0) >= 4 %}
            <a href="javascript:void(0)" onclick="showSection('auth-logs')">🔐 Логи авторизайций</a>
        {% endif %}
    </div>

    <div id="overlay" class="overlay" onclick="toggleMenu()"></div>

    {% if session.get('lvl') >= 1 %}
    <div id="logs-section" style="display:none;">
        <h1>Логи Админов</h1>

        <div class="refresh">
            <a href="/">Обновить</a>
        </div>

        <div class="cards-container">
            {% for log in logs %}
                {% set action_lower = log.action|lower %}
                <div class="card
                    {% if 'разбан' in action_lower and 'топ' not in action_lower %}unban
                    {% elif 'бан' in action_lower and 'топ' not in action_lower %}ban
                    {% else %}other{% endif %}">
                    <div class="bold">
                        Админ:
                        <a class="admin-link" href="/admin/{{ log.admin_id }}">
                            {{ log.admin_username }} ({{ log.admin_id }})
                        </a>
                    </div>
                    <div>Действие: {{ log.action }}</div>
                    <div>Пользователь: {{ log.target_username }} ({{ log.target_id }})</div>
                    <div>Время: {{ log.time }}</div>
                </div>
            {% else %}
                <p>Логи не найдены.</p>
            {% endfor %}
        </div>
    </div>
    {% endif %}

    <div id="bans-section" style="display:none;">
        <h1>Список забаненых пользователей</h1>
        <div class="cards-container">
            {% for ban in bans %}
                <div class="card ban ban-row">
                    <div>
                        Пользователь: {{ ban.user_id }}<br>
                        Причина: {{ ban.reason }}
                    </div>

                    {% if session.get('lvl', 0) > 1 %}
                    <button class="btn-unban" onclick="confirmUnban('{{ ban.user_id }}')">
                        Разбанить
                    </button>
                    {% endif %}
                </div>
            {% else %}
                <p>Список банов пуст</p>
            {% endfor %}
        </div>
    </div>

    <div id="auth-logs-section" style="display:none;">
        <h1>Логи Авторизаций</h1>

        <div class="cards-container">
            {% for log in auth_logs %}
                <div class="card">
                    <div><b>Username:</b> {{ log.username }}</div>
                    <div><b>id:</b> {{ log.user_id }}</div>
                    <div><b>time:</b> {{ log.time }}</div>
                </div>
            {% else %}
                <p>Логи авторизаций пустые</p>
            {% endfor %}
        </div>
    </div>
    
    <div id="admins-section" style="display:none;">
        <h1>Список администрараторов</h1>
        <div class="admins-container">
            {% for admin in admins %}
                <div class="card admin-card admin-lvl-{{ admin.lvl }}
                    {% if admin.user_id|string == session.get('user_id')|string %}
                        admin-me
                    {% endif %}
                ">

                    <div class="user-row">

                        <div>
                            <div><b>ID:</b> {{ admin.user_id }}</div>
                            <div>
                                <b>Username:</b> {{ admin.username }}

                            {% if admin.user_id|string == session.get('user_id')|string %}
                                <span class="you-label">Это ты</span>
                            {% endif %}
                            </div>

                            <div><b>lvl:</b> {{ admin.lvl }}</div>
                        </div>

                        <div class="user-actions">

                            {% if session.get('lvl')|int >= 4 %}

                                {% if session.get('lvl')|int == 4 and admin.lvl == 1 %}
                                    <button class="btn-delete"
                                        onclick="removeAdminFromList('{{ admin.user_id }}')">
                                        снять
                                    </button>
                                {% endif %}

                                {% if session.get('lvl')|int >= 5 %}
                                    <button class="btn-delete"
                                        onclick="removeAdminFromList('{{ admin.user_id }}')">
                                        снять
                                    </button>
                                {% endif %}
                            
                            {% endif %}
                        
                        </div>
                    
                    </div>

                </div>
            {% else %}
                <p>Список админов не был найден</p>
            {% endfor %}
        </div>
    </div>
    
    <div id="users-section" style="display:none;">
        <h1>Список пользователей</h1>
        <div class="admins-container">
            {% for user in users %}
                <div class="card user-card">
                    
                    <div><b>ID:</b> {{ user.user_id }}</div>
                    <div><b>Username:</b> {{ user.username }}</div>
                    <div><b>Admin:</b> {{ user.admin_lvl }}</div>
                    <div><b>Money:</b> {{ user.money }}</div>
                    
                    <hr>
                    
                    <div><b>Clicks:</b> {{ user.clicks }}</div>
                    <div><b>topBan:</b> {{ user.top_ban }}</div>
                    <div><b>Reason:</b> {{ user.top_ban_reason }}</div>
                    
                    <hr>
                    
                    <div><b>Business:</b> {{ user.business_lvl }}</div>
                    <div><b>Exp:</b> {{ user.business_exp }}</div>
                    <div><b>Money:</b> {{ user.business_money }}</div>
                 
                <div class="user-actions">
                    {% if session.get('lvl', 0) >= 3 %}
                    <button class="btn-ban" onclick="confirmBan('{{ user.user_id }}')">
                        Забанить
                    </button>
                    {% endif %}
                
                    {% if session.get('lvl', 0) >= 5 %}
                    <button class="btn-delete" onclick="confirmDeleteAccount('{{ user.user_id }}')">
                        Удалить аккаунт пользователя
                    </button>
                    {% endif %}
                </div>
                
                </div>
            {% else %}
                <p>Список базы данных полностью пуст</p>
            {% endfor %}
        </div>
    </div>
    
    {% if session.get('lvl', 0) > 1 %}
    <div id="admin-panel-section" style="display:none;">
        <h1>Админ панель</h1>
        <div class="admin-panel-box">
            <input type="text" id="search-username" placeholder="Username">
            <br>
            <button onclick="findUserId()">Узнать Id</button>
            
            <div class="admin-panel-result" id="admin-panel-result"></div>
            
            <hr style="margin:20px 0;">
            
            <h3>Выдать бан</h3>
            
            <input type="number" id="ban-user-id" placeholder="User Id">
            <br>
            
            <button onclick="confirmBanFromPanel()">Ban</button>

            {% if session.get('lvl', 0) >= 4 %}

            <hr style="margin:20px 0;">

            <h3>Управление администраторами</h3>

            <input type="number" id="admin-user-id" placeholder="User Id">
            <br><br>

            <button onclick="openGiveAdmin()">Назначить администратора</button>
            <button onclick="removeAdmin()">Снять администратора</button>

            {% endif %}

            {% if session.get('lvl', 0) >= 5 %}

            <hr style="margin:20px 0;">

            <h3>Ограничение на сайте</h3>

            <input type="number" id="restrict-user-id" placeholder="User id">
            <br>

            <textarea id="restrict-reason" placeholder="Причина ограничения" style="width:100%; max-width:400px; height:90px; margin-top:10px; border-radius:6px; padding:10px;"></textarea>
            <br><br>

            <button onclick="restrictSiteAccess()">Ограничить</button>
            <button onclick="unrestrictSiteAccess()">Снять ограничение</button>

            {% endif %}
        </div>
    </div>
    {% endif %}
                
    <div class="confirm-popup" id="confirm-popup">
        <p id="confirm-text"></p>
        <button onclick="unbanConfirmed()">✔️</button>
        <button onclick="closePopup()">❌</button>
    </div>
    
    <div class="confirm-popup" id="ban-popup">
        <p id="ban-text"></p>
        <textarea id="ban-reason" placeholder="Причина"></textarea>
        <br>
        <button onclick="banConfirmed()">✔️</button>
        <button onclick="closeBanPopup()">❌</button>
    </div>
    
    <div class="confirm-popup" id="delete-popup">
        <p id="delete-text"></p>
        <button onclick="deleteAccountConfirmed()">✔️</button>
        <button onclick="closeDeletePopup()">❌</button>
    </div>

    <div class="notification" id="notification"></div>

    <script>
        function toggleMenu() {
            const sidebar = document.getElementById("sidebar");
            const overlay = document.getElementById("overlay");
            const btn = document.querySelector(".menu-btn");
            
            sidebar.classList.toggle("active");
            overlay.classList.toggle("active");
            
            if (sidebar.classList.contains("active")) {
                btn.style.display = "none";
            } else {
                btn.style.display = "block";
            }
        }

        function showSection(section) {
            const lvl = Number("{{ session.get('lvl', 0) }}");

            if (
                (lvl < 3 && (section === 'logs' || section === 'admin-panel')) ||
                (lvl < 4 && section === 'auth-logs')
            ) {
                showNotification("Нет доступа", true);
                toggleMenu();
                return;
            }

            const logsSection = document.getElementById("logs-section");
            const bansSection = document.getElementById("bans-section");
            const adminsSection = document.getElementById("admins-section");
            const usersSection = document.getElementById("users-section");
            const adminPanelSection = document.getElementById("admin-panel-section");
            const authLogsSection = document.getElementById("auth-logs-section");

            if (logsSection) logsSection.style.display = (section === 'logs') ? 'block' : 'none';
            if (bansSection) bansSection.style.display = (section === 'bans') ? 'block' : 'none';
            if (adminsSection) adminsSection.style.display = (section === 'admins') ? 'block' : 'none';
            if (usersSection) usersSection.style.display = (section === 'users') ? 'block' : 'none';
            if (adminPanelSection) adminPanelSection.style.display = (section === 'admin-panel') ? 'block' : 'none';
            if (authLogsSection) authLogsSection.style.display = (section === 'auth-logs') ? 'block' : 'none'

            toggleMenu();
        }

        let currentUserId = null;

        function confirmUnban(userId) {
            currentUserId = userId;
            document.getElementById('confirm-text').textContent = "Вы хотите разбанить пользователя " + userId + "?";
            document.getElementById("confirm-popup").style.display = "block";
        }

        function closePopup() {
            document.getElementById("confirm-popup").style.display = "none";
            currentUserId = null;
        }

        function unbanConfirmed() {
            fetch("/unban", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: currentUserId})
        }).then(res => res.json())
            .then(data => {
                closePopup();
                showNotification(data.message);
                setTimeout(() => location.reload(), 1000);
            });
        }

        function showNotification(msg, isError=false) {
            const notif = document.getElementById("notification");
            notif.textContent = msg;
            
            notif.style.background = isError ? "#dc3545" : "#28a745";
            
            notif.style.display = "block";
            
            setTimeout(() => {
                notif.style.display = "none";
            }, 5000);
        }
        
        let banUserId = null;
        
        function confirmBan(userId) {
            banUserId = userId;
            document.getElementById("ban-text").textContent = 
                "Забанить пользователя " + userId + "?";
            document.getElementById("ban-popup").style.display = "block";
        }
        
        function closeBanPopup() {
            document.getElementById("ban-popup").style.display = "none";
            document.getElementById("ban-reason").value = "";
            banUserId = null;
        }
        
        function banConfirmed() {
            const reason = document.getElementById("ban-reason").value;
            
            fetch("/ban", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    user_id: banUserId,
                    reason: reason
                })
            })
            .then(res => res.json())
            .then(data => {
                closeBanPopup();
                showNotification(data.message, true);
                setTimeout(() => location.reload(), 1000);
            });
        }
        
        function findUserId() {
            const username = document.getElementById("search-username").value.trim();
            
            fetch("/find_user_id", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ username: username })
            })
            .then(res => res.json())
            .then(data => {
                const result = document.getElementById("admin-panel-result");
                
                if (data.success) {
                    result.innerHTML = `
                        <div>Найдет ID:</div>
                        <div class="copy-id-box">
                            <input type="text" id="found-user-id" value="${data.user_id}" readonly>
                            <button onclick="copyFoundId()">Скоприровать</button>
                        </div>
                    `;
                } else {
                    result.innerHTML = `<div style="color:red;">${data.message}</div>`;
                }
            });
        }
        
        function copyFoundId() {
            const input = document.getElementById("found-user-id");
            input.select();
            input.setSelectionRange(0, 999999);
            navigator.clipboard.writeText(input.value);
            
            showNotification("Ид был скопирован");
        }
        
        let deleteUserId = null;
        
        function confirmDeleteAccount(userId) {
            deleteUserId = userId;
            document.getElementById("delete-text").textContent = 
                "Удалить аккаунт пользователя " + userId + " ?";
            document.getElementById("delete-popup").style.display = "block";
        }
        
        function closeDeletePopup() {
            document.getElementById("delete-popup").style.display = "none";
            deleteUserId = null;
        }
        
        function deleteAccountConfirmed() {
            fetch("/delete_account", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ user_id: deleteUserId })
            })
            .then(res => res.json())
            .then(data => {
                closeDeletePopup();
                showNotification(data.message, true);
                setTimeout(() => location.reload(), 1000);
            });
        }
        
        function confirmBanFromPanel() {
            const userId = document.getElementById("ban-user-id").value.trim();
            
            if (!userId || isNaN(userId)) {
                showNotification("Напиши ид числом", true);
                return;
            }
            
            banUserId = userId;
            
            document.getElementById("ban-text").textContent = 
                "Подверди выдачу бана для " + userId;
            
            document.getElementById("ban-popup").style.display = "block";
        }

        function openGiveAdmin() {
            const userId = document.getElementById("admin-user-id").value.trim();

            if (!userId || isNaN(userId)) {
                showNotification("Не введен ид", true);
                return;
            }

            const lvl = prompt("Введи лвл администратора");

            if (!lvl || isNaN(lvl)) {
                showNotification("числом", true);
                return;
            }

            fetch("/give_admin", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    user_id: userId,
                    lvl: lvl
                })
            })
            .then(res => res.json())
            .then(data => {
                showNotification(data.message);
            })
        }

        function removeAdmin() {
            const userId = document.getElementById("admin-user-id").value.trim();
            
            if (!userId || isNaN(userId)) {
                showNotification("числом", true);
                return;
            }
            
            fetch("/remove_admin", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    user_id: userId
                })
            })
            .then(res => res.json())
            .then(data => {
                showNotification(data.message);
            });
        }

        function removeAdminFromList(userId) {
            if (!confirm("Снять администратора " + userId + "?")) return;

            fetch("/remove_admin", {
                method: "POST", 
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ user_id: userId })
            })
            .then(res => res.json())
            .then(data => {
                showNotification(data.message);
                setTimeout(() => location.reload(), 1000);
            });
        }

        function restrictSiteAccess() {
            const userId = document.getElementById("restrict-user-id").value.trim();
            const reason = document.getElementById("restrict-reason").value.trim();

            if (!userId || isNaN(userId)) {
                showNotification("числом", true);
                return;
            }

            if (!reason) {
                showNotification("причина", true);
                return;
            }

            fetch("/restrict_site_access", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    user_id: userId,
                    reason: reason
                })
            })
            .then(res => res.json())
            .then(data => {
                showNotification(data.message, !data.message.includes("ограничен"));
            });
        }

        function unrestrictSiteAccess() {
            const userId = document.getElementById("restrict-user-id").value.trim();

            if (!userId || isNaN(userId)) {
                showNotification("числом", true);
                return;
            }

            fetch("/unrestrict_site_access", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    user_id: userId
                })
            })
            .then(res => res.json())
            .then(data => {
                showNotification(data.message, false);
            });
        }
    </script>

    <div style="
    position:fixed;
    bottom:10px;
    right: 10px;
    background: #111;
    color: white;
    padding: 10px;
    border-radius: 8px;
    font-size: 14px;
    ">
    admin username: {{ session['username'] }}<br>
    lvl dostup: {{ session['lvl'] }}
    </div> 

</body>
</html>
"""

ADMIN_CABINET_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Кабинет администратора</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f4f4;
        }
        
        .layout {
            display: flex;
            min-height: 100vh;
        }
        
        .cabinet-sidebar {
            width: 235px;
            background: linear-gradient(180deg, #1a1a1d 0%, #101114 100%);
            color: white;
            padding: 26px 18px;
            box-sizing: border-box;
            min-height: 100vh;
        }
        
        .cabinet-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 24px;
            line-height: 1.15;
        }
        
        .cabinet-back {
            display: inline-block;
            margin-bottom: 40px;
            color: #e5e5e5;
            text-decoration: none;
            font-size: 15px;
            transition: 0.35s ease;
        }
        
        .cabinet-back:hover {
            color: white;
        }
        
        .cabinet-hover-menu {
            margin-top: 14px;
            display: flex;
            flex-direction: column;
            gap: 34px;
        }
        
        .cabinet-line-item {
            position: relative;
            height: 42px;
            cursor: pointer;
            border-radius: 14px;
        }
        
        .cabinet-line {
            position: absolute;
            left: 0;
            top: 50%;
            width: 100%;
            height: 6px;
            transform: translateY(-50%);
            background: rgba(255,255,255,0.28);
            border-radius: 999px;
            transition: all 0.45s ease;
        }
        
        .cabinet-line-label {
            position: absolute;
            left: 50%;
            top: -8px;
            transform: translateX(-50%);
            color: white;
            font-size: 18px;
            font-weight: 700;
            opacity: 0;
            pointer-events: none;
            white-space: nowrap;
            transition: opacity 0.45s ease, top 0.45s ease;
        }
        
        .cabinet-line-item:hover .cabinet-line-label {
            opacity: 1;
            top: -18px;
        }
        
        .cabinet-line-item:hover .cabinet-line {
            background: rgba(255,255,255,0.95);
            box-shadow: 0 0 12px rgba(255,255,255,0.22);
        }
        
        .cabinet-line-item.active .cabinet-line {
            background: #ffffff;
            box-shadow: 0 0 14px rgba(255,255,255,0.22);
        }
        
        .cabinet-line-item.active .cabinet-line-label {
            opacity: 1;
            top: -18px;
        }
        
        .cabinet-content {
            flex: 1;
            padding: 28px 20px 28px 24px;
            box-sizing: border-box;
        }
        
        .cabinet-header {
            background: white;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .cabinet-header h1 {
            margin: 0 0 10px 0;
            font-size: 28px;
        }
        
        .cabinet-sub {
            color: #555;
            font-size: 16px;
        }
        
        .cards-container {
            width: 100%;
            max-width: none;
        }
        
        .card {
            background: #fff;
            padding: 14px 18px;
            margin: 12px 0;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.08);
            text-align: left;
            width: 100%;
            box-sizing: border-box;
        }
        
        .card.ban {
            background-color: #ffdddd;
        }
        
        .card.unban {
            background-color: #ddffdd;
        }
        
        .cabinet-line-item {
            text-decoration: none;
            display: block;
        }
        
        .card.other {
            background-color: #fff8cc;
        }
        
        .bold {
            font-weight: bold;
        }
        
        .disabled-block {
            background: white;
            border-radius: 14px;
            padding: 18px;
            margin-top: 18px;
            color: #666;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .chart-box {
            background: white;
            border-radius: 14px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-top: 10px
        }
        
        .chart-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px
        }
        
        .chart-circle {
            width: 260px;
            height: 260px;
            margin: 0 auto 20px auto;
            border-radius: 50%;
            position: relative;
        }
        
        .chart-center {
            position: absolute;
            inset: 55px;
            background: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
            flex-direction: column;
        }
        
        .chart-legend {
            max-width: 420px;
            margin: 0 auto;
        }
        
        .chart-legend-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
            font-size: 18px;
        }
        
        .chart-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <div class="layout">
        <div class="cabinet-sidebar">
            <div class="cabinet-title">Личный кабинет администратора</div>
            
            <a href="/" class="cabinet-back">← Назад</a>
            
            <div class="cabinet-hover-menu">
                <a href="/admin/{{ admin_id }}?tab=logs" class="cabinet-line-item {% if active_tab == 'logs' %}active{% endif %}">
                    <div class="cabinet-line-label">Логи</div>
                    <div class="cabinet-line"></div>
                </a>
                
                {% if session.get('lvl', 0) >= 4 %}
                <a href="/admin/{{ admin_id }}?tab=manage" class="cabinet-line-item {% if active_tab == 'manage' %}active{% endif %}">
                    <div class="cabinet-line-label">Управление</div>
                    <div class="cabinet-line"></div>
                </a>
                {% endif %}
                
                <a href="/admin/{{ admin_id }}?tab=charts" class="cabinet-line-item {% if active_tab == 'charts' %}active{% endif %}">
                    <div class="cabinet-line-label">Диограммы</div>
                    <div class="cabinet-line"></div>
                </a>
            </div>
        </div>
            
        <div class="cabinet-content">
            <div class="cabinet-header">
                <h1>{{ admin_username }}</h1>
                <div class="cabinet-sub">ID: {{ admin_id }}</div>
            </div>
            
            {% if active_tab == 'logs' %}
            
            <div class="cards-container">
                {% for log in logs %}
                    <div class="card {% set action_lower = log.action.lower() %}{% if 'разбан' in action_lower and 'топ' not in action_lower %}unban{% elif 'бан' in action_lower and 'топ' not in action_lower %}ban{% else %}other{% endif %}">
                        <div class="bold">Админ: {{ log.admin_username }} ({{ log.admin_id }})</div>
                        <div>Действие: {{ log.action }}</div>
                        <div>Пользователь: {{ log.target_username }} ({{ log.target_id }})</div>
                        <div>Время: {{ log.time }}</div>
                    </div>
                {% else %}
                    <div class="disabled-block">Логи этого администратора не найденны</div>
                {% endfor %}
            </div>
            
            {% elif active_tab == 'charts' %}
            
            <div style="background:white; padding:20px; border-radius:12px;">
                <h2>Диаграмма банов</h2>
                
                <div style="
                    width:200px;
                    height:200px;
                    margin:auto;
                    border-radius:50%;
                    background: conic-gradient(
                        red 0% {{ ban_percent }}%,
                        green {{ ban_percent }}% 100%
                    );
                ">
                </div>
                
                <p>Баны: {{ bans_count }} ({{ ban_percent }}%)</p>
                <p>Разбаны: {{ unbans_count }} ({{ unban_percent }}%)</p>
            </div>

            {% elif active_tab == 'manage' %}

            <div class="admin-panel-box">
                <h2>Управление</h2>

                <div style="font-size:18px; margin-bottom:15px;">
                    Администратор: <b>{{ admin_username }}</b><br>
                    ид: <b>{{ admin_id }}</b>
                </div>

                {% if session.get('lvl', 0) >= 5 %}
                    <div style="display:flex; gap:10px; flex-wrap:wrap; justify-content:center; margin-top:15px;">
                        <button onclick="promoteAdmin('{{ admin_id }}')">Повысить</button>
                        <button onclick="demoteAdmin('{{ admin_id }}')">Понизить</button>
                    </div>
                {% else %}
                    <div class="disabled-block">Нет доступа</div>
                {% endif %}
            </div>

            {% endif %}

        </div>
    </div>

    <script>
        function promoteAdmin(adminId) {
            fetch("/promote_admin", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ user_id: adminId })
            })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                location.reload();
            });
        }

        function demoteAdmin(adminId) {
            fetch("/demote_admin", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ user_id: adminId })
            })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                location.reload();
            });
        }
    </script>
</body>
</html>
"""

def check_lvl(min_lvl):
    if not check_auth():
        return False
    return int(session.get("lvl", 0)) >= min_lvl

def check_auth():
    if "user_id" not in session:
        return False
    
    if time.time() - session.get("time", 0) > 900:
        session.clear()
        return False
    
    session["time"] = time.time()
    return True

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template_string(LOGIN_TEMPLATE)
    
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = site_access_collection.find_one({"username": username})

    if not user or user.get("password") != password:
        return jsonify({"success": False, "message": "Таких данных нет"})
    
    session["user_id"] = str(user["user_id"])
    session["username"] = user["username"]
    session["lvl"] = user.get("lvl", 0)
    session["time"] = time.time()
    session["site_blocked"] = bool(user.get("site_blocked", False))
    session["site_block_reason"] = str(user.get("site_block_reason", ""))

    auth_logs_collection.insert_one({
        "username": str(user.get("username", "")),
        "user_id": str(user.get("user_id", "")),
        "time": time.strftime("%d.%m.%Y %H:%M:%S")
    })

    return jsonify({"success": True})

@app.route("/", methods=["GET"])
def index():
    if not check_auth():
        return redirect("/login")
    
    if session.get("site_blocked", False):
        return render_template_string(
            BLOCKED_TEMPLATE,
            reason=session.get("site_block_reason", "нет")
        )
    
    logs = []

    if check_lvl(3):
        for log in logs_collection.find():
            action_text = str(log.get("action", ""))

            logs.append({
                "admin_id": str(log.get("admin_id", "")),
                "admin_username": str(log.get("admin_username", "")),
                "target_id": str(log.get("target_id", "")),
                "target_username": str(log.get("target_username", "")),
                "action": str(log.get("action", "")),
                "time": str(log.get("time", ""))
            })

    auth_logs = []
    
    if check_lvl(4):
        for log in auth_logs_collection.find().sort("_id", -1).limit(100):
            auth_logs.append({
                "username": str(log.get("username", "")),
                "user_id": str(log.get("user_id", "")),
                "time": str(log.get("time", ""))
            })

    bans = []

    for ban in bans_collection.find():
        user_id = str(ban.get("user_id", ""))
        reason = str(ban.get("reason", ""))

        bans.append({
            "user_id": user_id,
            "reason": reason
        })

    admins = []

    my_id = session.get("user_id")

    my_admin = None
    other_admins = []

    for user in users_collection.find({"lvl": {"$gt": 0}}).sort("lvl", -1):
        admin_data = {
            "user_id": str(user.get("user_id", "")),
            "username": str(user.get("username", "")),
            "lvl": int(user.get("lvl", 0))
        }

        if str(user.get("user_id")) == str(my_id):
            my_admin = admin_data
        else:
            other_admins.append(admin_data)
    
    if my_admin:
        admins.append(my_admin)

    admins.extend(other_admins)

    users = []

    for user in users_collection.find():
        user_id = str(user.get("user_id", ""))

        clickers = clickers_collection.find_one({"user_id": int(user_id)}) or {}

        clicks = clickers.get("clicks", 0)
        top_ban = 1 if clickers.get("top_ban") else 0
        top_ban_reason = clickers.get("top_ban_reason", "")

        business = business_collection.find_one({"user_id": int(user_id)}) or {}

        business_lvl = business.get("lvl", 0)
        business_exp = business.get("exp", 0)
        business_money = business.get("money", 0)

        users.append({
            "user_id": user_id,
            "username": user.get("username", ""),
            "admin_lvl": user.get("lvl", 0),
            "money": user.get("money", 0),

            "clicks": clicks,
            "top_ban": top_ban,
            "top_ban_reason": top_ban_reason,

            "business_lvl": business_lvl,
            "business_exp": business_exp,
            "business_money": business_money
        })

    return render_template_string(
        HTML_TEMPLATE,
        logs=logs,
        auth_logs=auth_logs,
        bans=bans,
        admins=admins,
        users=users,
    )

@app.route("/remove_admin", methods=["POST"])
def remove_admin():
    if not check_lvl(4):
        return jsonify({"message": "Нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")

    try:
        user_id_int = int(user_id)
    except:
        return jsonify({"message": "числом"})
    
    user = users_collection.find_one({
        "$or": [{"user_id": user_id_int}, {"user_id": str(user_id)}]
    })

    if not user:
        return jsonify({"message": "Пользователь не найден"})
    
    if str(user_id) == "8617037882":
        return jsonify({"message": "Нельзя"})
    
    if str(user_id) == session.get("user_id"):
        return jsonify({"message": "Нельзя снять себя"})
    
    current_lvl = int(user.get("lvl", 0))
    my_lvl = int(session.get("lvl", 0))

    if my_lvl == 4:
        if current_lvl != 1:
            return jsonify({"message": "Ты можешь снять только 1 лвл админа"})
        
    elif my_lvl >= 5:
        pass

    else:
        return jsonify({"message": "Нет доступа"})
    
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"lvl": 0}}
    )

    site_access_collection.update_many(
        {"user_id": {"$in": [user_id_int, str(user_id)]}},
        {"$set": {"lvl": 0}}
    )

    return jsonify({"message": f"{user_id} был снят с поста администратора"})

@app.route("/unban", methods=["POST"])
def unban_user():
    if not check_lvl(2):
        return jsonify({"message": "Нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")

    if user_id is None:
        return jsonify({"message": "Ошибка: пользователь не найден"})
    
    deleted = 0

    try:
        deleted += bans_collection.delete_many({"user_id": int(user_id)}).deleted_count
    except:
        pass

    deleted += bans_collection.delete_many({"user_id": str(user_id)}).deleted_count

    if deleted > 0:
        return jsonify({"message": f"Пользователь {user_id} разбанен"})
    else:
        return jsonify({"message": "Пользователь не найден"})
    
@app.route("/unrestrict_site_access", methods=["POST"])
def unrestrict_site_access():
    if not check_lvl(5):
        return jsonify({"message": "нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"message": "юзер ид не был указан"})
    
    try:
        user_id_int = int(user_id)
    except:
        return jsonify({"message": "ид должен быть числом"})
    
    target = site_access_collection.find_one({
        "user_id": {"$in": [user_id_int, str(user_id)]}
    })

    if not target:
        return jsonify({"message": "Пользователь не зарегестрирован как администратор"})
    
    site_access_collection.update_many(
        {"user_id": {"$in": [user_id_int, str(user_id)]}},
        {
            "$set": {
                "site_blocked": False,
                "site_block_reason": ""
            }
        }
    )

    return jsonify({"message": f"{user_id} получил доступ к сайту, снова"})
    
@app.route("/demote_admin", methods=["POST"])
def demote_admin():
    if not check_lvl(5):
        return jsonify({"message": "нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")

    try:
        user_id_int = int(user_id)
    except:
        return jsonify({"message": "числом"})
    
    user = users_collection.find_one({
        "$or": [{"user_id": user_id_int}, {"user_id": str(user_id)}]
    })

    if not user:
        return jsonify({"message": "пользователь не существует"})
    
    if str(user_id) == session.get("user_id"):
        return jsonify({"message": "нельзя менять свой лвл"})
    
    my_lvl = int(session.get("lvl", 0))
    target_lvl = int(user.get("lvl", 0))

    if target_lvl >= my_lvl:
        return jsonify({"message": "нельзя менять выше или равного себе"})
    
    if target_lvl <= 0:
        return jsonify({"message": "не является администратором"})
    
    new_lvl = target_lvl - 1

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"lvl": new_lvl}}
    )

    site_access_collection.update_many(
        {"user_id": {"$in": [user_id_int, str(user_id)]}},
        {"$set": {"lvl": new_lvl}}
    )

    return jsonify({"message": f"понижен на {new_lvl}"})
    
@app.route("/give_admin", methods=["POST"])
def give_admin():
    if not check_lvl(4):
        return jsonify({"message": "нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")
    lvl = int(data.get("lvl", 0))

    try:
        user_id_int = int(user_id)
    except:
        return jsonify({"message": "числом"})
    
    user = users_collection.find_one({
        "$or": [{"user_id": user_id_int}, {"user_id": str(user_id)}]
    })

    if not user:
        return jsonify({"message": "пользователь не существует"})
    
    if str(user_id) == session.get("user_id"):
        return jsonify({"message": "нельзя менять свой лвл"})
    
    current_lvl = int(user.get("lvl", 0))
    my_lvl = int(session.get("lvl", 0))

    if my_lvl == 4:
        if lvl != 1:
            return jsonify({"message": "администратор может выдавать только 1 лвл"})
        if current_lvl > 0:
            return jsonify({"message": "уже является администратором"})
        
    elif my_lvl >= 5:
        if lvl < 1 or lvl > 5:
            return jsonify({"message": "от 1 до 5"})
        
    else:
        return jsonify({"message": "нет доступа"})
    
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"lvl": lvl}}
    )

    return jsonify({"message": f"выдано {lvl} лвл пользователю {user_id}"})

@app.route("/restrict_site_access", methods=["POST"])
def restrict_site_access():
    if not check_lvl(5):
        return jsonify({"message": "нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")
    reason = str(data.get("reason", "")).strip()

    if not user_id:
        return jsonify({"message": "не указан ид"})
    
    if not reason:
        return jsonify({"message": "причина"})
    
    try:
        user_id_int = int(user_id)
    except:
        return jsonify({"message": "числом"})
    
    target = site_access_collection.find_one({
        "user_id": {"$in": [user_id_int, str(user_id)]}
    })

    if not target:
        return jsonify({"message": "пользователь не найден"})
    
    if str(user_id) == session.get("user_id"):
        return jsonify({"message": "нельзя ограничить себя"})
    
    site_access_collection.update_many(
        {"user_id": {"$in": [user_id_int, str(user_id)]}},
        {
            "$set": {
                "site_blocked": True,
                "site_block_reason": reason
            }
        }
    )

    return jsonify({"message": f"{user_id} больше не может пользоватся сайтом"})

@app.route("/ban", methods=["POST"])
def ban_user():
    if not check_lvl(3):
        return jsonify({"message": "Нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")
    reason = data.get("reason", "")

    if not user_id:
        return jsonify({"message": "Ошибка нет user_id"})

    try:
        user_id_int = int(user_id)
    except:
        return jsonify({"message": "Напиши ид числом"})

    user = users_collection.find_one({
        "$or": [
            {"user_id": user_id_int},
            {"user_id": str(user_id)}
        ]
    })

    if not user:
        return jsonify({"message": f"Пользователь {user_id} не найден"})

    bans_collection.insert_one({
        "user_id": user_id_int,
        "reason": reason
    })

    return jsonify({"message": f"Пользователь {user_id} забанен"})

@app.route("/promote_admin", methods=["POST"])
def promote_admin():
    if not check_lvl(5):
        return jsonify({"message": "нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")

    try:
        user_id_int = int(user_id)
    except:
        return jsonify({"message": "ид должен быть числом"})
    
    user = users_collection.find_one({
        "$or": [{"user_id": user_id_int}, {"user_id": str(user_id)}]
    })

    if not user:
        return jsonify({"message": "юзер не найден"})
    
    if str(user_id) == session.get("user_id"):
        return jsonify({"message": "нельзя менять свой лвл администратора"})
    
    my_lvl = int(session.get("lvl", 0))
    target_lvl = int(user.get("lvl", 0))

    if target_lvl >= my_lvl:
        return jsonify({"message": "нельзя повысить выше или равного себе"})
    
    if target_lvl >= 5:
        return ({"message": "максимальный лвл"})
    
    new_lvl = target_lvl + 1

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"lvl": new_lvl}}
    )

    site_access_collection.update_many(
        {"user_id": {"$in": [user_id_int, str(user_id)]}},
        {"$set": {"lvl": new_lvl}}
    )

    return jsonify({"message": f"{new_lvl} был выдан"})

@app.route("/find_user_id", methods=["POST"])
def find_user_id():
    if not check_lvl(3):
        return jsonify({"success": False, "message": "Нет доступа"})
    
    data =  request.get_json()
    username = str(data.get("username", "")).strip()

    if not username:
        return jsonify({
            "success": False,
            "message": "Введи username"
        })

    user = users_collection.find_one({"username": {"$regex": f"^{username}$", "$options": "i"}})

    if not user:
        return jsonify({
            "success": False,
            "message": "Пользователь не найден"
        })

    return jsonify({
        "success": True,
        "user_id": str(user.get("user_id", ""))
    })

@app.route("/delete_account", methods=["POST"])
def delete_account():
    if not check_lvl(5):
        return jsonify({"message": "Нет доступа"})
    
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"message": "Ошибка: user_id не передан"})

    deleted_users = 0
    deleted_clickers = 0
    deleted_business = 0

    try:
        user_id_int = int(user_id)
    except:
        user_id_int = user_id

    try:
        deleted_users += users_collection.delete_many({"user_id": user_id_int}).deleted_count
        deleted_clickers += clickers_collection.delete_many({"user_id": user_id_int}).deleted_count
        deleted_business += business_collection.delete_many({"user_id": user_id_int}).deleted_count
    except:
        pass

    deleted_users += users_collection.delete_many({"user_id": str(user_id)}).deleted_count
    deleted_clickers += clickers_collection.delete_many({"user_id": str(user_id)}).deleted_count
    deleted_business += business_collection.delete_many({"user_id": str(user_id)}).deleted_count

    total_deleted = deleted_users + deleted_clickers + deleted_business

    if total_deleted > 0:
        return jsonify({
            "message": f"Аккаунт: {user_id} удалён"
        })

    else:
        return jsonify({
            "message": f"Пользователь {user_id} не был найден"
        })

@app.route("/admin/<admin_id>", methods=["GET"])
def admin_cabinet(admin_id):
    if not check_auth():
        return redirect("/login")
    if not check_lvl(2):
        return redirect("/")
    
    active_tab = request.args.get("tab", "logs")

    if active_tab == "manage" and not check_lvl(4):
        return redirect(f"/admin/{admin_id}?tab=logs")

    query_ids = [admin_id]
    if admin_id.isdigit():
        query_ids.append(int(admin_id))

    admin_logs = []

    for log in logs_collection.find({"admin_id": {"$in": query_ids}}):
        admin_logs.append({
            "admin_id": str(log.get("admin_id", "")),
            "admin_username": str(log.get("admin_username", "")),
            "target_id": str(log.get("target_id", "")),
            "target_username": str(log.get("target_username", "")),
            "action": str(log.get("action", "")),
            "time": str(log.get("time", ""))
        })

    admin_username = "Неизвестный"

    admin_user = None
    try:
        admin_user = users_collection.find_one({"user_id": int(admin_id)})
    except:
        admin_user = None

    if not admin_user:
        admin_user = users_collection.find_one({"user_id": str(admin_id)})

    if admin_user:
        admin_username = str(admin_user.get("username", "Неизвестный"))
    elif admin_logs:
        admin_username = admin_logs[0]["admin_username"]

    bans_count = 0
    unbans_count = 0

    for log in admin_logs:
        action_lower = log["action"].lower()

        if "разбан" in action_lower and "топ" not in action_lower:
            unbans_count += 1
        elif "бан" in action_lower and "топ" not in action_lower:
            bans_count += 1

    total_actions = bans_count + unbans_count

    if total_actions > 0:
        ban_percent = round(bans_count / total_actions * 100)
        unban_percent = 100 - ban_percent
    else:
        ban_percent = 0
        unban_percent = 0

    return render_template_string(
        ADMIN_CABINET_TEMPLATE,
        admin_id=admin_id,
        admin_username=admin_username,
        logs=admin_logs,
        active_tab=active_tab,
        bans_count=bans_count,
        unbans_count=unbans_count,
        total_actions=total_actions,
        ban_percent=ban_percent,
        unban_percent=unban_percent
    )

import os 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
