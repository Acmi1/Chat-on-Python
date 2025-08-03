import socket
import threading

# Настройки соединения
HOST = 'localhost'  # Адрес хоста
PORT = 8080         # Порт

# Команды
COMMANDS = {
    '/help': 'Показать доступные команды',
    '/nick': 'Изменить ваш никнейм',
    '/exit': 'Закрыть сессию',
}

def send_message(sock, message):
    """Отправка сообщения."""
    sock.sendall(message.encode('utf-8'))

def receive_message(sock):
    """Получение сообщения."""
    return sock.recv(1024).decode('utf-8')

class Server:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.nickname = "Server"
    
    def start(self):
        print("Запускаем сервер...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        
        print(f"Слушаю подключения на {HOST}:{PORT}")
        client_sock, addr = self.server_socket.accept()
        print(f"Пользователь подключился с адреса {addr}")
        self.client_socket = client_sock
        
        # Запрашиваем никнейм у клиента
        send_message(self.client_socket, "Введите свой никнейм:")
        nickname = receive_message(self.client_socket)
        print(f"{nickname} присоединился к чату.")
        
        # Поток для приема сообщений от клиента
        recv_thread = threading.Thread(target=self.receive_messages)
        recv_thread.start()
        
        # Основной цикл отправки сообщений сервером
        while True:
            command = input("\n>>> ")
            
            if command.lower().startswith('/'):
                if command.strip() in COMMANDS.keys():
                    if command.strip() == '/help':
                        for cmd, desc in COMMANDS.items():
                            print(f"{cmd}: {desc}")
                    
                    elif command.strip() == '/nick':
                        new_nick = input("Новый никнейм: ").strip()
                        if len(new_nick) > 0:
                            self.nickname = new_nick
                            print(f"Ваш новый никнейм: {new_nick}")
                        else:
                            print("Никнейм пуст. Никнейм не изменён.")
                    
                    elif command.strip() == '/exit':
                        break
                else:
                    print("Команда не найдена.")
            else:
                full_message = f"[{self.nickname}] {command}"
                send_message(self.client_socket, full_message)
        
        # Завершаем работу сервера
        self.shutdown()
    
    def shutdown(self):
        print("Завершение работы сервера.")
        try:
            if self.client_socket:
                self.client_socket.close()
            if self.server_socket:
                self.server_socket.close()
        except Exception as e:
            pass
    
    def receive_messages(self):
        while True:
            try:
                data = receive_message(self.client_socket)
                if not data:
                    break
                print(f"\nПользователь отправил: {data}\n>>> ", end="")
            except ConnectionResetError:
                print("Клиент отключился.")
                break


class Client:
    def __init__(self):
        self.client_socket = None
        self.nickname = ""
    
    def connect(self):
        print("Подключение к серверу...")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        print("Успешно подключились!")
        
        # Отправляем никнейм серверу
        self.nickname = input("Введите свой никнейм: ").strip()
        send_message(self.client_socket, self.nickname)
        
        # Поток для приема сообщений от сервера
        recv_thread = threading.Thread(target=self.receive_messages)
        recv_thread.start()
        
        # Цикл отправки сообщений
        while True:
            message = input("\n>>> ")
            
            if message.lower().startswith('/'):
                if message.strip() in COMMANDS.keys():
                    if message.strip() == '/help':
                        for cmd, desc in COMMANDS.items():
                            print(f"{cmd}: {desc}")
                        
                    elif message.strip() == '/nick':
                        new_nick = input("Новый никнейм: ").strip()
                        if len(new_nick) > 0:
                            self.nickname = new_nick
                            print(f"Ваш новый никнейм: {new_nick}")
                        else:
                            print("Никнейм пуст. Никнейм не изменён.")
                    
                    elif message.strip() == '/exit':
                        break
                else:
                    print("Команда не найдена.")
            else:
                full_message = f"[{self.nickname}] {message}"
                send_message(self.client_socket, full_message)
    
    def receive_messages(self):
        while True:
            try:
                data = receive_message(self.client_socket)
                if not data:
                    break
                print(f"\nСервер отправил: {data}\n>>> ", end="")
            except ConnectionResetError:
                print("Отключены от сервера.")
                break

if __name__ == "__main__":
    choice = input("Выберите режим:\n1. Создать сервер\n2. Подключиться к серверу\nВаш выбор: ")
    
    if choice == "1":
        HOST = input("Введите IP адрес чтоб создать на нем хост; ")
        server = Server()
        server.start()
    elif choice == "2":
        HOST = input("Введите IP адрес чтобы подключиться к хосту который создал на этом адресе: ")
        client = Client()
        client.connect()
    else:
        print("Ошибка выбора режима.")