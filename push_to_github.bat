@echo off
echo ========================================
echo  PUSHING TO GITHUB
echo ========================================
echo.

git init
git add .
git commit -m "Initial deployment - Haramaya Health Center"
git remote add origin https://github.com/charidedecha7-ops/Oromia-Health-.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo  DONE! Check GitHub repository
echo ========================================
pause
