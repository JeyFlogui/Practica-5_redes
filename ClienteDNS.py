# Código del Cliente DNS
import socket


def dns_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('192.168.100.18', 44000)

    while True:
        url = input("Ingrese la URL (o 'salir' para salir): ")

        if url.lower() == 'salir':
            break

        try:
            sock.sendto(url.encode(), server_address)
            data, _ = sock.recvfrom(1024)
            response = data.decode().strip()

            if url.lower() == 'www.ipn.mx':
                question = "¿Cuál es la IP de www.ipn.mx?"
                print("Enviando pregunta al servidor DNS:", question)
                sock.sendto(question.encode(), server_address)
                data, _ = sock.recvfrom(1024)
                response = data.decode().strip()
                print("Respuesta del servidor DNS:", response)

                # Suponemos que el cliente tiene conocimiento de la jerarquía del DNS y hace las consultas correspondientes
                for dns in ['root', 'ccTLD.mx', 'www.ipn.mx']:
                    print(f"Consultando al servidor {dns}...")
                    sock.sendto(dns.encode(), server_address)
                    data, _ = sock.recvfrom(1024)
                    response = data.decode().strip()
                    print(f"Respuesta del servidor DNS: {response}")
        except socket.timeout:
            print("Tiempo de espera agotado. No se pudo obtener una respuesta del servidor.")

    sock.close()


if __name__ == '__main__':
    dns_client()