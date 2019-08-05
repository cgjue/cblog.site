# 在flask例子flaskr的基础上改的。

# cblog.site网站源代码。使用sqlite3数据库， 登录后可编辑新页面。
使用命令python genStaticHtml.py 可导出所有静态页面，在github page上浏览，效果还可以。

# 文章生成使用了wangEditor.js ,代码高亮使用highlight.min.js

# 启动web服务
$python app.py


# 数据库初始化
$flask initdb

# 注册账号需要邀请码，自己往数据库表welcode中添加即可，注册页面中邀请码输入栏禁止输入，要自己想办法输进去
    tips: 浏览器页面中修改标签属性




# 生成静态页面
在web服务正常运行的前提下，使用命令 python genStaticHtml.py生成静态页面

# 上传静态页面到github page  修改uploadcgjue.site.io.sh 中的github地址，然后运行
$sh uploadcgjue.site.io.sh

 费了些时间，增加了上传文件功能，方便以后引入脚本和图片等。

## next step:
    1. 增加评论功能，对于静态网站来说，引用第三方的评论插件就行了吧。

很久没做网站，3天时间能搞这么多，意外了(&^_^&)。

## 更新 2019 06-20
将wangEditor更改为showdown.js
原因: 
1 近期使用markdwon比较多,感觉这种语法挺好的.
2 github向我报告说说wangEditor有bug, 虽然我只是本地编辑,上传到网上的都是静态页面,后wangEditor没关系.但还是改下吧,说不定有人会下载我的blog,搭在某个服务器上呢

使用方法, 编辑器相当丑陋,对markdown语法相当熟悉的人而言就无所谓了吧,不然的话,还是选择一个markdwon编辑器编完后,再上传吧.
额,我在用有道云笔记,目前恰好可以.
