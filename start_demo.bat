@echo off
cd /d "%~dp0"
echo ============================================
echo   个人主页 · 前端 + 后台 一键启动
echo.
echo   前台：http://127.0.0.1:5001/personal-site/
echo   后台：http://127.0.0.1:5001/admin
echo   账号：admin / chenkun2026
echo ============================================
start "" "http://127.0.0.1:5001/personal-site/"
start "" "http://127.0.0.1:5001/admin"

if exist "E:\vscode\课设\.venv\Scripts\python.exe" (
    "E:\vscode\课设\.venv\Scripts\python.exe" server\app.py
) else (
    python server\app.py
)
pause
