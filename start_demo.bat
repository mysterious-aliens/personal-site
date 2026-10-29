@echo off
cd /d "%~dp0"
echo ============================================
echo   个人主页 · 前端 + 后端 一键启动
echo   启动后浏览器访问：
echo   http://127.0.0.1:5001/personal-site/
echo   管理入口：http://127.0.0.1:5001/personal-site/#admin
echo   账号 admin / chenkun2026
echo ============================================
start "" "http://127.0.0.1:5001/personal-site/"

if exist "E:\vscode\课设\.venv\Scripts\python.exe" (
    "E:\vscode\课设\.venv\Scripts\python.exe" server\app.py
) else (
    python server\app.py
)
pause
