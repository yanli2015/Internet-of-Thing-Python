import smtplib

def send_email(message):
    fromaddr = 'xxx@gmail.com'
    toaddrs  = 'xxx@gmail.com'
    msg = message
    username = 'xx@gmail.com'
    password = 'xxx'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()