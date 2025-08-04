import socket
import threading

# Глобальные переменные
clients = {}  # словарь пользователей {nickname: connection}
admin_commands = ['/kick', '/ban']  # доступные администраторские команды


def broadcast(message):
    """Отправляет сообщение всем клиентам"""
    for conn in clients.values():
        try:
            conn.sendall(message.encode())
        except Exception as e:
            print(f'Ошибка отправки сообщения: {e}')


def handle_client(conn, addr):
    """Обрабатывает входящие соединения клиентов"""
    nickname = None
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        
        if not nickname:
            nickname = data
            clients[nickname] = conn
            broadcast(f'{nickname} присоединился к чату!')
            continue
            
        if nickname == 'Admin-Commands':
            # Администраторская команда
            command = data.split()[0]
            if command in admin_commands:
                args = data.split()[1:]
                if command == '/kick':
                    user_to_kick = args[0]
                    if user_to_kick in clients:
                        del clients[user_to_kick]
                        broadcast(f'{user_to_kick} был выгнан из чата.')
                    else:
                        broadcast('Пользователь не найден.')
                elif command == '/ban':
                    pass  # Можно добавить реализацию блокировки
            else:
                broadcast(f'[Администратор]: {data}')
        else:
            # Обычное сообщение
            broadcast(f'[{nickname}]: {data}')
    
    # Удаляем соединение и уведомляем остальных участников
    del clients[nickname]
    broadcast(f'{nickname} покинул чат.')
    conn.close()


def start_server(host='localhost', port=8765):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на {host}:{port}")
    
    while True:
        client_conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_conn, addr))
        thread.start()


if __name__ == "__main__":
    choice = input("Выберите режим: [S]erver or [C]lient? ").lower()
    if choice == 's':
        start_server()  # Запускаем сервер
    elif choice == 'c':
        host = input("Введите адрес сервера: ")
        port = int(input("Введите порт сервера: "))
        nick = input("Ваш никнейм: ")
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(nick.encode())  # Отправка имени пользователя
        
        while True:
            message = input("")
            client_socket.send(message.encode())
 
