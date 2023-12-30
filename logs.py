import os
import paramiko
import schedule
import time

# Словарь с именами и адресами серверов
servers = {
    'server1_name': 'root@10.10.85.24',
    'server2_name': 'root@10.1.10.20'
}

# Путь, где будет храниться SSH ключ
ssh_key_path = os.path.expanduser('~/.ssh/marzban_key')

# Генерация SSH ключа, если он не существует
if not os.path.exists(ssh_key_path):
    os.system(f'ssh-keygen -t rsa -b 4096 -f {ssh_key_path} -N ""')
    print("SSH ключ сгенерирован.")
else:
    print("SSH ключ уже существует.")

def copy_and_delete_file(ssh, server_name, remote_file_path, local_dir):
    local_file_path = os.path.join(local_dir, f"{server_name}-access.log")

    # Чтение содержимого файла
    stdin, stdout, stderr = ssh.exec_command(f'cat {remote_file_path}')
    file_contents = stdout.read()
    
    # Дозапись в локальный файл
    with open(local_file_path, 'ab') as local_file:
        local_file.write(file_contents)

    # Удаляем все строки кроме последних 5
    ssh.exec_command(f"sed -i -e :a -e '$q;N;6,$D;ba' {remote_file_path}")
    print(f"Файл с сервера {server_name} скопирован и дозаписан. Старые строки удалены.")

# Обработка каждого сервера
for server_name, server_address in servers.items():
    username, hostname = server_address.split('@')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, username=username, key_filename=ssh_key_path)
        print(f"Успешно подключено к {server_name} ({hostname}) с существующим ключом.")
    except paramiko.ssh_exception.NoValidConnectionsError:
        os.system(f'ssh-copy-id -i {ssh_key_path}.pub {server_address}')
        ssh.connect(hostname, username=username, key_filename=ssh_key_path)
        print(f"Ключ скопирован и подключено к {server_name} ({hostname}).")

    remote_file_path = "/var/lib/marzban-node/access.log"
    local_dir = "/var/lib/marzban/"

    copy_and_delete_file(ssh, server_name, remote_file_path, local_dir)
    ssh.close()
    
if __name__ == "__main__":
    # Запуск функции main каждые 5 минут
    schedule.every(5).minutes.do(main)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
