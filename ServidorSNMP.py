from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.proto import rfc1902
from pysnmp.proto.api import v2c
from pysnmp.smi import builder

class MyCommandResponder(cmdrsp.CommandResponderBase):
    def __init__(self, snmpEngine, snmpContext):
        cmdrsp.CommandResponderBase.__init__(self, snmpEngine, snmpContext)

    def handleMgmtOperation(self, snmpEngine, stateReference, contextName, PDU, acInfo):
        varBinds = process_request(snmpEngine, stateReference, contextName, PDU, acInfo)
        print(f'Response varBinds: {varBinds}')
        try:
            self.sendRsp(snmpEngine, stateReference, PDU.getRequestID(), 0, 0, varBinds)
        except Exception as e:
            print("Error: " + str(e))

def process_request(snmpEngine, stateReference, contextName, PDU, acInfo):
    print(f'Received PDU: {PDU.prettyPrint()}')
    # Cargar los datos del archivo MIB
    mibData = load_mib_data()

    # Validar el OID de la solicitud
    oid = PDU[-1][0]

    if oid in mibData:
        value = mibData[oid]
        print(f'Requested OID: {oid}, value: {value}')
        return [(oid, value)]
    else:
        print(f'Requested OID not found: {oid}')
        return []

def load_mib_data():
    global mibData

    if not mibData:
    # Cargar los datos del archivo MIB.txt
        with open('MIB.txt', 'r') as file:
            for line in file:
                if line.strip():
                    oid, value = line.strip().split()
                    mibData[rfc1902.ObjectName(oid)] = rfc1902.OctetString(value)

    return mibData

def run_agent():
    # Configuración del agente
    comunidad = "public"
    puerto = 8161

    # Crear el motor SNMP
    snmpEngine = engine.SnmpEngine()

    # Cargar los datos de configuración
    config.addV1System(snmpEngine, comunidad, comunidad, contextName=comunidad)

    # Crear una instancia de SnmpContext
    snmpContext = context.SnmpContext(snmpEngine)

    # Registrar el procesador de solicitudes
    MyCommandResponder(snmpEngine, snmpContext)

    # Configurar el transporte UDP
    udpTransport = udp.UdpTransport()
    udpTransport.openServerMode(('localhost', puerto))

    # Registrar el transporte en el motor SNMP
    config.addTransport(
        snmpEngine,
        udp.domainName,
        udpTransport
    )

    # Iniciar el bucle de recepción de solicitudes
    snmpEngine.transportDispatcher.jobStarted(1)
    print("Agente SNMP iniciado")
    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except Exception as e:
        print("Error en el dispatcher: " + str(e))

# Ejecutar el agente SNMP
run_agent()