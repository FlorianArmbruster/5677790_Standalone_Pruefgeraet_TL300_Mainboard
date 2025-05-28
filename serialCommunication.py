import serial;
import serial.tools.list_ports

class SerialCommunication():

    
    def __init__(self):
        self.ser = None
        self.comport = None
        self.Text = ""
        self.Text_bytes = b""
        self.connected = 0
        self.getInfo()  # Port wird direkt beim Erstellen geöffnet


    def message(self):
        self.Text = "1"
        Texttosend = "10"
        self.Text_bytes=Texttosend.encode()

    def getInfo(self):
        

        # Wenn der Port bereits offen ist, nichts tun
        if self.ser and self.ser.is_open:
            return

        # Wenn bereits versucht wurde, aber fehlgeschlagen ist, auch nichts tun
        if self.ser is not None:
            return




        ports = serial.tools.list_ports.comports()

        if not ports:
            self.comport = None
            self.ser = None
            return

        for port in ports:
            if not hasattr(self, 'comport') or self.comport != port.device:
                self.comport = port.device
                try:
                    self.ser = serial.Serial(self.comport,115200)  # Hier wird self.ser gesetzt
                    print(f"Port {self.comport} geöffnet.")
                    break
                
                except serial.SerialException as e:
                    print(f"Fehler beim Öffnen von {self.comport}: {e}")
                    self.ser = None

                
    def printtext(self):
        self.message()
        self.getInfo()

        if self.ser:
            self.ser.write(self.Text_bytes)
            data=self.ser.readline()
            dataDecoded = data.decode('utf-8')
            if self.Text in dataDecoded:
                print(dataDecoded)
                self.connected = 1
                return
            self.connected = 0
        else:
            #self.connected = 1 #SIMULATION ONLY REMOVE FOR FINAL!!!!! 
            self.connected = 0
                
            