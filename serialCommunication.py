import serial
import serial.tools.list_ports

class SerialCommunication:
    def __init__(self):
        # Initialisierung der Variablen
        self.ser = None         # Serielle Verbindung
        self.comport = None     # COM-Port
        self.answerPassed = "1" # Erfolgsantwort vom ESP32
        self.answerFailed = "0" # Fehlerantwort vom ESP32
        self.Text_bytes = b""   # Zu sendende Bytes
        self.connected = 0      # Verbindungsstatus
        self.getInfo()          # Versuche, eine serielle Verbindung herzustellen

    def getInfo(self):
        # Prüfe, ob bereits eine Verbindung besteht
        if self.ser and self.ser.is_open:
            return
        if self.ser is not None:
            return

        # Liste aller verfügbaren seriellen Ports
        ports = serial.tools.list_ports.comports()
        if not ports:
            self.comport = None
            self.ser = None
            return

        # Versuche, den ersten verfügbaren Port zu öffnen
        for port in ports:
            if not hasattr(self, 'comport') or self.comport != port.device:
                self.comport = port.device
                try:
                    self.ser = serial.Serial(self.comport, 115200, timeout=20)
                    print(f"Port {self.comport} geöffnet.")
                    break
                except serial.SerialException as e:
                    print(f"Fehler beim Öffnen von {self.comport}: {e}")
                    self.ser = None

    def send_and_receive(self, text_to_send):
        """
        Sendet einen Befehl an den ESP32 und wartet bis zu 20 Sekunden auf eine Antwort.
        Beendet die Abfrage sofort, wenn '1' oder '0' empfangen wird.
        Gibt True zurück bei Erfolg ('1'), sonst False ('0' oder Timeout).
        """
        try:
            self.Text_bytes = text_to_send.encode()
            self.ser.reset_input_buffer()
            self.ser.write(self.Text_bytes)
    
            data = self.ser.readline()
            data_decoded = data.decode('utf-8').strip()
            print(f"Antwort vom ESP: {data_decoded}")

            # Antwort auswerten
            if self.answerPassed in data_decoded:
                self.connected = 1
                return True
            elif self.answerFailed in data_decoded:
                self.connected = 0
                return False
            else:
                self.connected = 0
                return False

        except Exception as e:
            print(f"Fehler bei der seriellen Kommunikation: {e}")
            self.connected = 0
            return False
