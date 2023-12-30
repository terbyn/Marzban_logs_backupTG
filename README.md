<h1 align="left">Копирование логов Marzban-node и backup Marzban </h1>
<p align="left">Эти скрипты нужны для сбора логов с нод Marzban и выполнения бэкапа с помощью TG.</p>
<p align="left">Перед установкой убедитесь, что у вас включено логирование для нод и мэйн сервера.</p>
'''
Это 'код' внутри текста.
'''

###

<h1 align="left">Как это работает</h1>

###
<h3 align="left">Описание:</h3>
<p align="left">Репозиторий содержит два Python срипта: logs.py, backup.py. Скрипт logs.py позволяет скопировать файл access.log с ваших нод и положить его на мейн, после копирования файла с логами скрипт удаляет все строки из него кроме последних 5. Скрипт отрабатывает каждые 5 минут.  <br><br></p>

<p align="left">Скрипт backup.py делает бэкап двух каталогов /opt/marzban и /var/lib/marzban каждые 5 минут и отправляет их в вашего ТГ бота.<br><br></p>
<p align="left">Скрипт systemd.sh помогает создать демона для ваших скриптов. Запускается следующим образом: "sh systemd.sh 'имя скрипта'<br><br></p>

<h3 align="left">Шаг 1: скачиваем репозиторий</h3>

###

<p align="left">Скачиваем репозиторий и устанавливаем зависимости<br><br></p>

```bash
git clone https://github.com/terbyn/Marzban_logs.git
cd /Marzban_logs
pip install -r requirements.txt
```

###

<h3 align="left">Шаг 2 : Настройка backup.py </h3>

###

<p align="left">Открываем backup.py и правим значения под свои <br><br></p>

```bash
bot_token = 'token'
chat_id = 'chat id'
```

<h3 align="left">Шаг 3 : Установка systemctl для того чтобы скрипт был запущен в качестве демона </h3>


```bash
sh systemd.sh backup
```

###

<h3 align="left">Шаг 2 : Настройка logs.py </h3>

###

<p align="left">Открываем logs.py и правим значения под свои <br><br></p>

```bash
'server1_name': 'root@10.70.80.20',
'server2_name': 'root@10.10.10.20'
```
<p align="left">Первый раз скрипт нужно запустить вручную и ввести пароли от серверов, чтобы скрипт мог прокинуть SSH ключи. <br><br></p>

<h3 align="left">Шаг 3 : Установка systemctl для того чтобы скрипт был запущен в качестве демона </h3>
###

```bash
sh systemd.sh logs
```

<p align="left">Вы можете опционально настраивать каждый скрипт отдельно друг от друга. </p>

###


