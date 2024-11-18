import serial;
import serial.tools.list_ports

class SerialCommunication():

    def message(self):
        self.Text = "communication established"
        Texttosend = "10"
        self.Text_bytes=Texttosend.encode()

    def getInfo(self):
        ports = serial.tools.list_ports.comports()

        if not ports:
            self.comport = None
            self.ser = None
            return

        for port in ports:
            self.comport = port.device
            self.ser = serial.Serial(self.comport,115200)  # Hier wird self.ser gesetzt
                
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
        else:
            self.connected = 0