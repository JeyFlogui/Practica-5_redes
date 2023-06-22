import asyncio
import os

class SMTPServer:
    def __init__(self):
        self.mailbox = {}  # Buzón de correo para almacenar los mensajes recibidos

    async def handle_client(self, reader, writer):
        await self.send_response(writer, 220, 'escom.com Simple Mail Transfer Service Ready')  # Enviamos una respuesta inicial al cliente
        sender = None
        recipient = None
        while True:
            line = await reader.readline()  # Leemos la línea enviada por el cliente
            if not line:
                break
            line = line.decode().strip()
            if line.startswith('HELO'):
                await self.send_response(writer, 250, 'OK')  # Respondemos al comando HELO
            elif line.startswith('MAIL FROM:'):
                sender = line[10:].strip('<>')  # Aqui se obtiene el remitente del correo
                await self.send_response(writer, 250, 'OK')  # Responde al comando MAIL FROM
            elif line.startswith('RCPT TO:'):
                recipient = line[8:].strip('<>')  # Aqui se obtiene el destinatario del correo
                if recipient not in self.mailbox:  # Verificamos si el destinatario existe en el buzón
                    self.mailbox[recipient] = []  # Creamos una entrada en el buzón para el destinatario
                    await self.send_response(writer, 550, 'No such user here')  # Responde con un error si el destinatario no existe
                else:
                    await self.send_response(writer, 250, 'OK')  # Responde al comando RCPT TO
            elif line == 'DATA':
                await self.send_response(writer, 354, 'Start mail input; end with <CR><LF>.<CR><LF>')  # Responde al comando DATA
                while True:
                    data = await reader.readline()  # Lee el contenido del correo línea por línea
                    if data.strip() == b'.':
                        break
                    self.mailbox[recipient].append(data.decode())  # Almacenamos el contenido del correo en el buzón
                    self.save_to_inbox(recipient, data.decode())  # Aqui se guarda el contenido del correo en la bandeja de entrada
                await self.send_response(writer, 250, 'OK')  # Responde al finalizar el envío del correo
            elif line == 'QUIT':
                await self.send_response(writer, 221, 'escom.com closing transmission channel')  # Responde al comando QUIT
                break
            else:
                await self.send_response(writer, 500, 'Command not recognized')  # Responde con un error si el comando no es reconocido

    async def send_response(self, writer, code, message):
        print(f"Server: {code} {message}")
        writer.write(f"{code} {message}\r\n".encode())  # Enviamos la respuesta al cliente
        await writer.drain()

    def save_to_inbox(self, recipient, data):
        with open(f'{recipient}_inbox.txt', 'a') as f:
            f.write(data + '\n')

async def main():
    server = SMTPServer()
    server = await asyncio.start_server(server.handle_client, '192.168.1.75', 44444)

    async with server:
        await server.serve_forever()  # Aqui hacemos el "servir por siempre"

asyncio.run(main())
