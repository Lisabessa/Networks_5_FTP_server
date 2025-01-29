import socket
import os
import shutil

PORT = 6666
WORK_DIR = os.path.join(os.getcwd(), 'working_dir')
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)


def process(req):
    try:
        parts = req.split(' ')
        command = parts[0]

        if command == 'pwd':  # Рабочая директория
            return WORK_DIR

        elif command == 'ls':  # Список файлов
            return '; '.join(os.listdir(WORK_DIR))
        
        elif command == 'create':  # Создание нового файла
            if len(parts) < 3:
                return 'Error: Usage create <filename> <content>'
            filename = os.path.join(WORK_DIR, parts[1])
            content = ' '.join(parts[2:])
            with open(filename, 'w') as f:
                f.write(content)
            return f'File {parts[1]} created'

        elif command == 'cat':  # Чтение файла
            if len(parts) < 2:
                return 'Error: File name not specified'
            filename = os.path.join(WORK_DIR, parts[1])
            if os.path.exists(filename) and os.path.isfile(filename):
                with open(filename, 'r') as f:
                    return f.read()
            return 'Error: File not found'
        
        elif command == 'rm':  # Удаление файлов
            if len(parts) < 2:
                return 'Error: File name not specified'
            filename = os.path.join(WORK_DIR, parts[1])
            if os.path.exists(filename) and os.path.isfile(filename):
                os.remove(filename)
                return f'File {parts[1]} removed'
            return 'Error: File not found'

        elif command == 'rename':  # Переименование файла
            if len(parts) < 3:
                return 'Error: Usage rename <old_name> <new_name>'
            old_name = os.path.join(WORK_DIR, parts[1])
            new_name = os.path.join(WORK_DIR, parts[2])
            if os.path.exists(old_name):
                os.rename(old_name, new_name)
                return f'File renamed from {parts[1]} to {parts[2]}'
            return 'Error: File not found'

        elif command == 'mkdir':  # Создание новой директории
            if len(parts) < 2:
                return 'Error: Directory name not specified'
            dirname = os.path.join(WORK_DIR, parts[1])
            os.makedirs(dirname, exist_ok=True)
            return f'Directory {parts[1]} created'

        elif command == 'rmdir':  # Удаление директории
            if len(parts) < 2:
                return 'Error: Directory name not specified'
            dirname = os.path.join(WORK_DIR, parts[1])
            if os.path.exists(dirname) and os.path.isdir(dirname):
                shutil.rmtree(dirname)
                return f'Directory {parts[1]} removed'
            return 'Error: Directory not found'

        elif command == 'exit':
            return 'Exit..'

        else:
            return 'Error: Unknown command'

    except Exception as e:
        return f'Error: {str(e)}'
    
    
def run_server():
    sock = socket.socket()
    sock.bind(('', PORT))
    sock.listen()
    print(f"Сервер запущен. Рабочая директория: {WORK_DIR}")

    while True:
        conn, addr = sock.accept()
        print(f"Подключение от: {addr}")

        request = conn.recv(1024).decode()
        print(f"Запрос: {request}")

        response = process(request)
        conn.send(response.encode())

        if request == 'exit':
            break

    conn.close()


run_server()