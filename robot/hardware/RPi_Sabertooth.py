import serial

"""
    class to represent all Sabertooth motor controllers on one Serial pin (can be up to 8 sabertooth motor controllers, just specify the proper address)
    In this library, just call drive() and pass in an address (0-7), speed (-127-127), and motor (0 or 1).

    Note to the EEs: Check the datasheet below to see how this should be set up. The motor and battery connections are intuitive.
        As for the signal stuffs, there are four pins:
        S1: Serial(UART) TX(Transmit) pin of controller
        S2: NC
        0V: Any GND pin on the controller
        5V: This provides a regulated 5V 1A output. Feel free to use it to power whatever.
        
        Now for the switches... This is IMPORTANT!
        Since we are using packetized serial, the first three pins are as follows:
        LOW LOW HIGH
        The next three count binary... Inverted and reversed. That is HIGH = 0 and LSB is switch 6(rightmost).
        This software automatically takes care of the fact that the addresses are offset by 128, so treat the HIGH HIGH HIGH as 0 and LOW HIGH HIGH as 1 etc.
        Note that this means the CS team will be referencing them from 0 to 7, so please for the love of God make the numbering intuitive!

    NOTE: Intended use is for Packetized Serial mode
    https://www.dimensionengineering.com/datasheets/Sabertooth2x25v2.pdf (page 17 for Packetized Serial)
"""
class Sabertooth:
    def __init__(self):
        self.sout = serial.Serial('/dev/serial0', 9600)#Figuring out the port: https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3-pi3b-pizerow/45571#45571
        sout.open()
    """
        Build a packet in the format expected by the Sabertooth motor controller.
    """
    def buildPacket(address, command, data):
        address = address + 128#the address is actually between 128 and 135, so by adding 128, addresses 0-8 can be used to reference sabertooths
        checksum = (address + command + data) & 127
        buffer = bytearray()#the serial "sout" expects a byte or bytearray, so we give it a bytearray
        buffer.append(address)#we just append all the data in the order necessary to the bytearray. Check the datasheet to see this.
        buffer.append(command)
        buffer.append(data)
        buffer.append(checksum)
        sout.write(buffer)

    """
        Drives a motor at the specified speed on the sabertooth with the specified address.
    """
    def drive(address=0, speed=30, motor=0):
        if address > 7 or address < 0:#just validating the inputs :)
            raise ValueError("Address must be in range 0-7")
        if speed > 127 or speed < 0:
            raise ValueError("Speed must be in range 0-127")
        if motor != 0 and motor != 1:
            raise ValueError("Motor must be in range 0-1")
        command = 0
        if motor == 1:
            command = command + 4
        if speed < 0:
            command = command + 1
        buildPacket(address, command, abs(speed))
    
    """
        Feel free to add any functionality you want down here! (i.e. driveAll, driveTwo, etc.)
    """