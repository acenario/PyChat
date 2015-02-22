
import CN_Sockets # CN_Sockets adds ability to interrupt "while True" loop with ctl-C
from chatterbotapi import ChatterBotFactory, ChatterBotType


class UDP_Clever_Client(object):

    def __init__(self, server_address):
        self.Server_Address = server_address
        socket, AF_INET, SOCK_DGRAM = CN_Sockets.socket, CN_Sockets.AF_INET, CN_Sockets.SOCK_DGRAM
        self.sock = socket(AF_INET,SOCK_DGRAM)

        factory = ChatterBotFactory()
        bot = factory.create(ChatterBotType.CLEVERBOT)
        self.botsession = bot.create_session()
        self.message = None

    def receive(self):

        #send dummy message to connect client to server
        bytearray_message = bytearray("",encoding="UTF-8")
        bytes_sent = self.sock.sendto(bytearray_message, self.Server_Address)
        import json

        while True:
            try:
                bytearray_msg, source_address = self.sock.recvfrom(1024)

                source_IP, source_port = source_address

                import json
                dict_message = bytearray_msg.decode("UTF-8")
                decoded_message = json.loads(dict_message)

                payload = decoded_message["PAYLOAD"]
                sender_IP, sender_port = decoded_message["SOURCE"]


                print "\n" + "=== MESSAGE RECEIVED ==="
                out = "\n" + "<" + str(sender_IP) + ":" + str(sender_port) + ">" + ": " + payload
                print out
                print "\n" + "=== MESSAGE ENDED ===" + "\n"

                self.message = payload

                #This line is necessary for formatting purposes because of threading
                # print "Enter message to send to server:"

            except timeout:

                print "."#,end="" #,flush=True  # if process times out, just print a "dot" and continue waiting.  The effect is to have the server print  a line of dots
                                               # so that you can see if it's still working.
                continue  # go wait again


    def send(self):
        while True:
            # str_message = raw_input("Enter message to send to server: ")

            if self.message != None:
            
                str_message = self.botsession.think(self.message)

                bytearray_message = bytearray(str_message,encoding="UTF-8") # note that sockets can only send 8-bit bytes.
                                                                            # Since Python 3 uses the Unicode character set,
                                                                            # we have to specify this to convert the message typed in by the user
                                                                            # (str_message) to 8-bit ascii


                bytes_sent = self.sock.sendto(bytearray_message, self.Server_Address) # this is the command to send the bytes in bytearray to the server at "Server_Address"

                print "{} bytes sent".format(bytes_sent) #sock_sendto returns number of bytes send.
                print "=== MESSAGE SENT ===" + "\n"

                self.message = None


    def start_client(self):
        print "UDP_TX client started for UDP_Server at IP address {} on port {}".format(
            self.Server_Address[0],self.Server_Address[1])

        #threadify
        from threading import Thread
        listen_thread = Thread(target=self.receive, args=())
        send_thread = Thread(target=self.send, args=())
        listen_thread.start()
        send_thread.start()



if __name__ == "__main__":
    address = raw_input("Enter server address: ")
    server_address = (address, 6280)
    UDP_Clever_Client = UDP_Clever_Client(server_address)
    UDP_Clever_Client.start_client()