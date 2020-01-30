import hub
import time
hub.ble.callback(lambda x: print("ble callback = %s" % x))
class LWPDevice:
  def __init__(self, conn):
    self.conn = conn
    self.conn.callback(self.recv)
    time.sleep(0.5)
    self.conn.subscribe()

  def recv(self, data):
    print("recv data:", data)

  def send(self, data):
    self.conn.send((len(data)+2).to_bytes(2, 'little') + data)

  def writePort(self, port, mode, data):
    self.send(bytes([0x81, port, 0x11, 0x51, mode]) + data)

  def writePort1(self, port, mode, b):
    self.writePort(port, mode, bytes([b]))

  def portMode(self, port, mode, notify = 1):
    self.send(bytes([0x41, port, mode, notify, 0, 0, 0, 1]))

def connect(timeout = 15):
  hub.ble.scan(timeout)
  for _ in range(timeout):
    for i, a in enumerate(hub.ble.scan_result()):
      if a['service_id'] == '00001623-1212-EFDE-1623-785FEABCD123':
        hub_model_id = a['man_data'][1] if len(a['man_data']) > 1 else None
        print("Connecting to hub model %d" % hub_model_id)
        conn = hub.ble.connect(i)
        if conn:
          return LWPDevice(conn)
        return None
    time.sleep(1)
  return None
