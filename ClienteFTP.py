import socket  # Importa el módulo socket para la comunicación de red

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket para el cliente

# Conecta el socket del cliente a la dirección IP y puerto del servidor
client_socket.connect(('x.x', 44451))

data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crea un socket para el servidor de datos

# Conecta el socket del servidor de datos a la dirección IP y puerto correspondientes
data_socket.connect(('x.x', 44450))

while True:
    response = client_socket.recv(1024).decode('utf-8').strip()  # Aqui recibimos la respuesta del servidor
    print('Respuesta del servidor:', response)

    if response.startswith('221'):  # Si la respuesta indica que la conexión se cerrará
        client_socket.close()  # Cierra el socket del cliente
        break

    command = input('Introduce un comando FTP: ')
    client_socket.sendall((command + '\r\n').encode('utf-8'))  # Enviamos el comando al servidor

    if command.lower().startswith('stor'):  # Si el comando es "stor" (subir archivo)
        command_parts = command.split(' ')
        if len(command_parts) < 2:
            print('Falta el nombre del archivo después de "stor"')
            continue
        filename = command_parts[1]
        with open(filename, 'rb') as file:
            data_socket.sendall(file.read())  # Envía los datos del archivo al servidor de datos
        data_socket.close()  # Cierra el socket del servidor de datos