# Código del Servidor DNS
import socket

dns_table = {
    'www.ipn.mx': '148.204.103.43',
    'root': "148.204.103.100",
    'ccTLD.mx': '148.204.103.200',
}

def resolve_dns(query):
    if query in dns_table:
        return dns_table[query]
    else:
        return "No se puede resolver la consulta."


def dns_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('192.168.100.18', 44000)
    sock.bind(server_address)

    print('Servidor DNS iniciado.')

    while True:
        data, client_address = sock.recvfrom(1024)
        domain = data.decode().strip()
        response = resolve_dns(domain)
        sock.sendto(response.encode(), client_address)


if __name__ == '__main__':
    dns_server()
