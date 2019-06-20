#将build目录上传到github
cd build 
#git init
git config --global user.email "467784592@qq.com"
#git pull  
#当出现整合远程变更错误时，使用
git add .
git commit -m “update”
git remote add origin git@github.com:cgjue/cgjue.github.io.git
git push -u origin +master
#当强制上传到master时使用+
#git push -u origin master
cd ..
