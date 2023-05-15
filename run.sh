
cd /root/Apps/ashen_boring

echo "$(date)\r" >> README.md
git add .
git commit -m "$(date)"

git push
