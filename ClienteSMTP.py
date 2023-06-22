import asyncio

class SMTPClient:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port

    async def send_email(self, sender, recipient, message):
        reader, writer = await asyncio.open_connection(self.server_address, self.server_port)  # Aqui establecemos una conexión con el servidor SMTP
        await reader.readline()
        await self.send_command(writer, f"HELO {self.server_address}")  # Aqui enviamos el comando HELO al servidor SMTP
        await reader.readline()
        await self.send_command(writer, f"MAIL FROM:<{sender}>")  # Aqui enviamos el comando MAIL FROM al servidor SMTP con el remitente del correo
        await reader.readline()
        await self.send_command(writer, f"RCPT TO:<{recipient}>")  # Aqui enviamos el comando RCPT TO al servidor SMTP con el destinatario del correo
        response = await reader.readline()
        if response.decode().startswith('550'):
            await self.send_command(writer, f"RCPT TO:<{recipient}>")  # Volvemos a enviar el comando RCPT TO si el destinatario no existe
            await reader.readline()
        await self.send_command(writer, 'DATA')  # Aqui enviamos el comando DATA al servidor SMTP para indicar el contenido del correo
        await reader.readline()
        await self.send_command(writer, message)  # Aqui enviamos el contenido del correo línea por línea
        await self.send_command(writer, '.')  # Aqui enviamos el comando '.' para indicar el final del correo
        await reader.readline()
        await self.send_command(writer, 'QUIT')  # Aqui enviamos el comando QUIT para cerrar la conexión con el servidor SMTP
        await reader.readline()
        writer.close()

    async def send_command(self, writer, command):
        print(f"Client: {command}")
        writer.write(f"{command}\r\n".encode())  # Desde aqui enviamos un comando al servidor SMTP
        await writer.drain()

async def main():
    client = SMTPClient('192.168.1.75', 44444)
    await client.send_email('alan@escom.com', 'jey@escom.com', 'Holaaa')  # Enviamos un correo desde el remitente al destinatario

asyncio.run(main())
