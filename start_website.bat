@echo off
title University AI Helpdesk Chatbot - B.Tech Project
echo ========================================================
echo   AI UNIVERSITY HELPDESK CHATBOT - B.TECH PROJECT
echo   Starting Web Server at http://127.0.0.1:8000
echo ========================================================
start "" "C:\Program Files\Mozilla Firefox\firefox.exe" "http://127.0.0.1:8000"
python server.py
pause
