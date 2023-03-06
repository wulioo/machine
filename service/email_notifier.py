from functools import partial

from notifiers import get_notifier

from conf.settings import email

# 配置邮件发送
mail_params = {
    "username": email.get("username"),
    "password": email.get("password"),
    "from": email.get("from"),
    "to": email.get("to"),
    "host": email.get("host"),
    "port": email.get("port"),
    "ssl": email.get("ssl"),
    "tls": email.get("tls"),
    "html": email.get("html"),
}
notify = get_notifier("email")
notify = partial(notify.notify, **mail_params)

# sigh_files = [r'C:\Users\mike\PycharmProjects\tmp\a.pyc']
#
# notify(**mail_params, message='sss', subject='ddd')

if __name__ == "__main__":
    print(email)
    notify(message="hello", subject="test")
