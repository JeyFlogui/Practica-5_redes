from pysnmp.hlapi import *


def send_request(oid, comunidad, host, puerto):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, puerto)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print(f"Error al enviar la solicitud: {errorIndication}")
    elif errorStatus:
        print(f"Error en la respuesta: {errorStatus.prettyPrint()}")
    else:
        for varBind in varBinds:
            print(f"Respuesta recibida: {varBind.prettyPrint()}")


def run_manager():
    # Configuración del gestor
    oid = "1.3.6.1.2.1.1.1.0"
    comunidad = "public"
    host = "localhost"
    puerto = 8161

    # Enviar la solicitud GETREQUEST al agente
    send_request(oid, comunidad, host, puerto)


# Ejecutar el gestor SNMP
run_manager()
