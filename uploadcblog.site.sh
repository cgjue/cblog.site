git init
git config --global user.email "467784592@qq.com"
git add README
git add *.py
git add *.sh
git add cblog/*
git commit -m "update"
git remote add origin git@github.com:cgjue/cblog.site.git
#当强制上传到master时使用
#git push https://gitee.com/ssasa1/cblog.site.git
git push -u origin +master
#git push -u origin master
