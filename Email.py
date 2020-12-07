# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import time
import os


# 发邮件
def send_mail(title, content, receiver_list, attachment=None):
    if attachment is None:
        attachment = []
    maunder = '15201114041@163.com'
    sender_name = '15201114041@163.com'
    sender_pwd = 'MTUDRDLSJUCLCEDM'
    sm_tp_server = 'smtp.163.com'

    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    subject = title + "_" + time_str

    msg = MIMEMultipart()
    part1 = MIMEText(content, _subtype='html', _charset="utf-8")
    msg.attach(part1)
    # 构造附件
    if len(attachment) > 0:
        for img in attachment:
            att = MIMEText(open(img, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="%s"' % img.split(os.sep)[-1]
            msg.attach(att)

    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = maunder
    msg['To'] = ";".join(receiver_list)

    sm_tp = smtplib.SMTP_SSL(sm_tp_server, 465)
    # sm_tp.starttls()
    sm_tp.login(sender_name, sender_pwd)
    sm_tp.sendmail(maunder, receiver_list, msg.as_string())
    print("发送邮件成功")
    sm_tp.quit()
