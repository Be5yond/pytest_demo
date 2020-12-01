import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pathlib
import configparser
HOME = pathlib.Path(__file__).absolute().parent.parent
config = configparser.ConfigParser()
config.read(HOME/'config.ini')



def sendmail(title, content):
    sender = config.get('report.mail', 'sender')
    receivers =  json.loads(config.get('report.mail', 'receivers'))

    # 构造邮件正文
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header("autotest robot", 'utf-8') 
    message['To'] =  Header(','.join([s.split('@')[0] for s in receivers]), 'utf-8')      
    subject = f'AutoTest执行结果: {title}'
    message['Subject'] = Header(subject, 'utf-8')

    server = smtplib.SMTP('smtp.exmail.qq.com')
    server.login(sender, config.get('report.mail', 'secret'))
    server.sendmail(sender, receivers, message.as_string())
    
