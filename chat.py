import socket
import threading

# Настройки соединения
HOST = 'localhost'
PORT = 8080

def send_message(sock, message):
    sock.sendall(message.encode())

def receive_message(sock):
    return sock.recv(1024).decode()

class Server:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
    
    def start(self):
        print("Запускаем сервер...")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(1)
        
        print(f"Слушаю подключения на {HOST}:{PORT}")
        client_sock, addr = self.server_socket.accept()
        print(f"Пользователь подключился с адреса {addr}")
        self.client_socket = client_sock
        
        # Запускаем поток для приема сообщений от клиента
        recv_thread = threading.Thread(target=self.receive_messages)
        recv_thread.start()
        
        while True:
            command = input("\n>>> ")
            
            if command.lower() == "/quit":
                break
                
            elif command.startswith("/"):
                print("Неверная команда")
                continue
            
            else:
                send_message(self.client_socket, command)
        
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
    
    def connect(self):
        print("Подключение к серверу...")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((HOST, PORT))
        print("Успешно подключились!")
        
        # Запускаем поток для приема сообщений от сервера
        recv_thread = threading.Thread(target=self.receive_messages)
        recv_thread.start()
        
        while True:
            message = input("\n>>> ")
            send_message(self.client_socket, message)
    
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
        HOST = input("Введите IP к которому подключаться клиенты: ")
        server = Server()
        server.start()
    elif choice == "2":
        HOST = input("Введите IP чтоб подключиться к хосту:  ")
        client = Client()
        client.connect()
    else:
        print("Ошибка выбора режима.")
