#! /usr/bin/env python
# -*- coding: UTF-8 -*-

#python app.py ：运行服务
#flask initdb : 初始化数据库
import cblog
app = cblog.create_app()
app.run(host='127.0.0.1',port=5000, debug = True)
