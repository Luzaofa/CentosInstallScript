#!/usr/bin/env python
# encoding: utf-8
# Time    : 2/11/2019 8:21 AM
# Author  : Luzaofa


""" 邮件参数配置(具体配置参考模板样式) """

"""
一、正文配置方法
    正文类型1、massage            模板样式：subject='主题', mass='纯文本正文信息'
    正文类型2、html_massage       模板样式：subject='主题', mass='<p>html文本信息</p><p><a href="http://www.
                                           luzaofa.com">爱情链接!</a></p>'
    正文类型3、html_pic_massage   模板样式：subject='主题', mass='<p>html文本信息</p><img src="cid:imageid">',
                                           pic_path='图片文件地址'，cid=['cid1', 'cid2', 'cid3'
二、附件配置信息
    附件类型1、xlsx_att            模板样式： xls_path='目标文件地址'
    附件类型1、docx_att            模板样式： doc_path='目标文件地址'
    附件类型1、jpg_att             模板样式： pic_path='目标文件地址'
"""

receiver = ['', ]  # 接受用户邮箱地址

# 正文配置
mass_type = 'html_massage'  # 所发邮件类型（html、是否带有图片、纯文本）

subject = '服务器配置反馈信息'  # 邮件主题
mass = '<p>相关结果请查看附件</p>'  # 邮件正文
mass_pic_path = []  # 正文所添加图片地址
cid = []  # 正文所添加图片ID

# 附件配置
att_type = ['xlsx_att']  # 所要发送附件类型（Excel、Word、JPG）

xls_path = ['/SendEmail/Enclosure/installLog.txt']  # Excel文件地址
doc_path = []  # Word文件地址
pic_path = []  # 图片地址
