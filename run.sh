
cd /root/Apps/ashen_boring

echo "$(date) 1\r" > README.md
git add .
git commit -m "$(date) 1"

git push
