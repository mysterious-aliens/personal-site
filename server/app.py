# -*- coding: utf-8 -*-
"""个人主页后端：内容读取 + 管理端登录 + 保存。

启动：
    pip install flask flask-cors
    python server/app.py

接口：
    GET  /api/health
    GET  /api/content            读取整站内容（公开）
    POST /api/login              管理员登录，返回 token
    PUT  /api/content            保存内容（需 Bearer token）
    POST /api/content/reset      恢复默认内容（需 Bearer token）
"""

import hashlib
import hmac
import json
import os
import sqlite3
import time

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "site.db")
DIST_DIR = os.path.join(os.path.dirname(BASE_DIR), "dist")

ADMIN_USER = os.environ.get("SITE_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("SITE_ADMIN_PASSWORD", "chenkun2026")
SECRET = os.environ.get("SITE_SECRET", "personal-site-dev-secret")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.after_request
def allow_private_network(resp):
    # 允许从公网 HTTPS 页面（GitHub Pages）访问本机后端
    resp.headers["Access-Control-Allow-Private-Network"] = "true"
    return resp

DEFAULT_CONTENT = {
    "name": "陈堃",
    "role": "物联网工程在读 · 大模型与深度学习方向",
    "tagline": "从零训练 63.91M 参数中文模型，手写 BPE 分词器",
    "badge": "辽宁 · 大连　正在学习大模型",
    "stats": [
        {"num": "04", "label": "实训项目"},
        {"num": "63.91M", "label": "模型参数"},
        {"num": "1.24GB", "label": "训练语料"},
    ],
    "about": [
        "我是陈堃，大连民族大学物联网工程专业大三学生，方向是大模型与深度学习工程。",
        "喜欢从零开始造轮子，从分词器到预训练模型都自己动手实现过一遍，喜欢把原理搞懂再写代码。",
        "目前在做课程设计项目，学习 Web 开发、Git 部署、AI 辅助开发等技术。",
    ],
    "meta": ["📍 辽宁 · 大连", "🎓 大连民族大学", "💡 大模型工程"],
    "skills": [
        {"icon": "💻", "title": "编程语言", "desc": "日常写代码的主力语言", "tags": ["Python", "C语言", "Java", "JavaScript"]},
        {"icon": "🧠", "title": "AI / 深度学习", "desc": "从训练到微调的完整链路", "tags": ["PyTorch", "Transformers", "LoRA", "BPE 分词器"]},
        {"icon": "🛠️", "title": "开发工具", "desc": "版本管理与 AI 辅助开发", "tags": ["Git", "GitHub", "VS Code", "Cursor"]},
        {"icon": "✨", "title": "其他", "desc": "课程里接触过的技术", "tags": ["HTML/CSS", "MySQL", "51单片机", "Proteus"]},
    ],
    "projects": [
        {"title": "MiniMind 大模型预训练", "desc": "从零实现 63.91M 参数的中文预训练模型，包括 BPE 分词器、Transformer 架构与训练流程。", "tags": ["PyTorch", "Transformer"]},
        {"title": "SFT 微调作业", "desc": "在魔搭云端进行全量 SFT 与 LoRA 微调，理解聊天模板与 loss 遮盖机制。", "tags": ["LoRA", "Transformers"]},
        {"title": "电商图片下载插件", "desc": "Chrome 扩展插件，使用 Cursor 辅助开发，GitHub Pages 部署。", "tags": ["JavaScript", "Chrome 扩展"]},
        {"title": "个人主页网站", "desc": "深色科技风个人主页，Vue 3 + Vite 构建，带终端打字机动画，后端可实时修改内容。", "tags": ["Vue 3", "Vite"]},
    ],
    "blog": [
        {"date": "2026 · 10", "title": "从零实现一个 BPE 分词器", "desc": "记录手写 BPE 分词器的过程，理解合并规则与词表构建。"},
        {"date": "2026 · 10", "title": "大模型预训练流程记录", "desc": "从数据准备、训练脚本到 loss 曲线的完整流程。"},
    ],
    "contact": {"email": "3465473990@qq.com", "github": "github.com/mysterious-aliens"},
}


def hash_password(password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), SECRET.encode(), 100_000).hex()


def make_token(username):
    raw = f"{username}:{int(time.time() // 3600)}"
    return hmac.new(SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()


def check_token(username, token):
    # 允许当前小时与上一小时，避免整点掉登录
    for offset in (0, 1):
        raw = f"{username}:{int(time.time() // 3600) - offset}"
        expected = hmac.new(SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(expected, token):
            return True
    return False


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS content (id INTEGER PRIMARY KEY, data TEXT NOT NULL, updated_at REAL NOT NULL)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS admin (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT)"
    )
    if conn.execute("SELECT id FROM content WHERE id = 1").fetchone() is None:
        conn.execute(
            "INSERT INTO content (id, data, updated_at) VALUES (1, ?, ?)",
            (json.dumps(DEFAULT_CONTENT, ensure_ascii=False), time.time()),
        )
    if conn.execute("SELECT id FROM admin WHERE username = ?", (ADMIN_USER,)).fetchone() is None:
        conn.execute(
            "INSERT INTO admin (username, password_hash) VALUES (?, ?)",
            (ADMIN_USER, hash_password(ADMIN_PASSWORD)),
        )
    conn.commit()
    conn.close()


def read_content():
    conn = get_db()
    row = conn.execute("SELECT data, updated_at FROM content WHERE id = 1").fetchone()
    conn.close()
    return json.loads(row["data"]), row["updated_at"]


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "time": time.time()})


@app.get("/api/content")
def get_content():
    data, updated = read_content()
    return jsonify({"ok": True, "data": data, "updated_at": updated})


@app.post("/api/login")
def login():
    body = request.get_json(silent=True) or {}
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""

    conn = get_db()
    row = conn.execute("SELECT password_hash FROM admin WHERE username = ?", (username,)).fetchone()
    conn.close()

    if row is None or not hmac.compare_digest(row["password_hash"], hash_password(password)):
        return jsonify({"ok": False, "error": "用户名或密码错误"}), 401

    return jsonify({"ok": True, "token": make_token(username), "username": username})


@app.put("/api/content")
def update_content():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer ") or not check_token(ADMIN_USER, auth[7:].strip()):
        return jsonify({"ok": False, "error": "未登录或登录已过期"}), 401

    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"ok": False, "error": "内容格式不正确"}), 400

    for key in ("name", "role", "tagline", "about", "skills", "projects"):
        if key not in body:
            return jsonify({"ok": False, "error": f"缺少字段：{key}"}), 400

    conn = get_db()
    conn.execute(
        "UPDATE content SET data = ?, updated_at = ? WHERE id = 1",
        (json.dumps(body, ensure_ascii=False), time.time()),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "updated_at": time.time()})


@app.post("/api/content/reset")
def reset_content():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer ") or not check_token(ADMIN_USER, auth[7:].strip()):
        return jsonify({"ok": False, "error": "未登录或登录已过期"}), 401
    conn = get_db()
    conn.execute(
        "UPDATE content SET data = ?, updated_at = ? WHERE id = 1",
        (json.dumps(DEFAULT_CONTENT, ensure_ascii=False), time.time()),
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


@app.get("/")
@app.get("/personal-site")
@app.get("/personal-site/")
@app.get("/personal-site/index.html")
def index():
    if not os.path.exists(os.path.join(DIST_DIR, "index.html")):
        return jsonify({"ok": False, "error": "还没有构建前端，请先执行 npm run build"}), 503
    return send_from_directory(DIST_DIR, "index.html")


@app.get("/personal-site/<path:filename>")
def frontend_files(filename):
    return send_from_directory(DIST_DIR, filename)


init_db()

if __name__ == "__main__":
    print("后端已启动：http://127.0.0.1:5001")
    print(f"管理账号：{ADMIN_USER} / {ADMIN_PASSWORD}")
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
