import socket
import threading

# Definición de la clase FTPServerThread que hereda de threading.Thread
class FTPServerThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)  # Inicializamos la clase Thread
        self.client_socket = client_socket  # Aqui almacenamos el socket del cliente
        self.client_address = client_address  # Aqui almacena la dirección del cliente

    def run(self):
        self.client_socket.sendall('220 Servicio listo\r\n'.encode('utf-8'))

        while True:
            command = self.client_socket.recv(1024).decode(
                'utf-8').strip()  # Recibimos el comando enviado por el cliente.

            if command.lower().startswith('user'):
                self.client_socket.sendall('331 Usuario correcto, necesito contraseña\r\n'.encode('utf-8'))
            elif command.lower().startswith('pass'):
                self.client_socket.sendall('230 Usuario autenticado\r\n'.encode('utf-8'))
            elif command.lower().startswith('stor'):
                filename = command.split(' ')[1]  # Extraemos el nombre de archivo del comando.
                self.client_socket.sendall('150 Estado del archivo OK; abriendo conexión de datos\r\n'.encode('utf-8'))

                data_socket, _ = data_server_socket.accept()  # Aceptamos una conexión en el socket del servidor de datos.

                with open(filename,
                          'wb') as file:  # Abre el archivo en modo escritura binaria y escribe los datos recibidos a través del socket de datos.
                    file.write(data_socket.recv(1024))
                data_socket.close()

                self.client_socket.sendall(
                    '226 Cerrando conexión de datos, transferencia de archivo exitosa\r\n'.encode('utf-8'))
            elif command.lower() == 'quit':
                self.client_socket.sendall('221 Cerrando conexión\r\n'.encode('utf-8'))
                self.client_socket.close()
                break
            else:
                self.client_socket.sendall('500 Comando no reconocido\r\n'.encode('utf-8'))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creamos un socket para el servidor.
server_socket.bind(('x.x', 44451))
server_socket.listen(1)

data_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_server_socket.bind(('x.x', 44450))
data_server_socket.listen(1)

print('Servidor FTP esperando conexiones...')

while True:
    client_socket, client_address = server_socket.accept()  # Aceptamos una conexión entrante en el socket del servidor.
    print('Conexión aceptada de', client_address)

    FTPServerThread(client_socket,
                    client_address).start()  # Iniciamos un nuevo hilo para manejar la comunicación con el cliente.
