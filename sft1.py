import math
import struct
import socket
import select
import threading

_HOST = '127.0.0.1'  # defines the host as "localhost"
_PORT = 10000        # defines the port as "10000"

class ChatServer(threading.Thread):
    """
    Defines the chat server as a Thread.
    """

    MAX_WAITING_CONNECTIONS = 10
    RECV_BUFFER = 4096
    RECV_MSG_LEN = 4

    def __init__(self, host, port):
        """
        Initializes a new ChatServer.

        :param host: the host on which the server is bounded
        :param port: the port on which the server is bounded
        """
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.connections = []  # collects all the incoming connections
        self.running = True  # tells whether the server should run

    def _bind_socket(self):
        """
        Creates the server socket and binds it to the given host and port.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.MAX_WAITING_CONNECTIONS)
        self.connections.append(self.server_socket)

    def _send(self, sock, msg):
        """
        Prefixes each message with a 4-byte length before sending.

        :param sock: the incoming socket
        :param msg: the message to send
        """
        # Packs the message with 4 leading bytes representing the message length
        msg = struct.pack('>I', len(msg)) + msg
        # Sends the packed message
        sock.send(msg)

    def _receive(self, sock):
        """
        Receives an incoming message from the client and unpacks it.

        :param sock: the incoming socket
        :return: the unpacked message
        """
        data = None
        # Retrieves the first 4 bytes from the message
        tot_len = 0
        while tot_len < self.RECV_MSG_LEN:
            msg_len = sock.recv(self.RECV_MSG_LEN)
            tot_len += len(msg_len)
        # If the message has the 4 bytes representing the length...
        if msg_len:
            data = ''
            # Unpacks the message and gets the message length
            msg_len = struct.unpack('>I', msg_len)[0]
            tot_data_len = 0
            while tot_data_len < msg_len:
                # Retrieves the chunk i-th chunk of RECV_BUFFER size
                chunk = sock.recv(self.RECV_BUFFER)
                # If there isn't the expected chunk...
                if not chunk:
                    data = None
                    break # ... Simply breaks the loop
                else:
                    # Merges the chunks content
                    data += chunk
                    tot_data_len += len(chunk)
        return data


    def _broadcast(self, client_socket, client_message):
        """
        Broadcasts a message to all the clients different from both the server itself and
        the client sending the message.

        :param client_socket: the socket of the client sending the message
        :param client_message: the message to broadcast
        """
        for sock in self.connections:
            is_not_the_server = sock != self.server_socket
            is_not_the_client_sending = sock != client_socket
            if is_not_the_server and is_not_the_client_sending:
                try :
                    self._send(sock, client_message)
                except socket.error:
                    # Handles a possible disconnection of the client "sock" by...
                    sock.close()  # closing the socket connection
                    self.connections.remove(sock)  # removing the socket from the active connections list

    def _run(self):
        """
        Actually runs the server.
        """
        while self.running:
            # Gets the list of sockets which are ready to be read through select non-blocking calls
            # The select has a timeout of 60 seconds
            try:
                ready_to_read, ready_to_write, in_error = select.select(self.connections, [], [], 60)
            except socket.error:
                continue
            else:
                for sock in ready_to_read:
                    # If the socket instance is the server socket...
                    if sock == self.server_socket:
                        try:
                            # Handles a new client connection
                            client_socket, client_address = self.server_socket.accept()
                        except socket.error:
                            break
                        else:
                            self.connections.append(client_socket)
                            print ("Client (%s, %s) connected") % client_address

                            # Notifies all the connected clients a new one has entered
                            self._broadcast(client_socket, "\n[%s:%s] entered the chat room\n" % client_address)
                    # ...else is an incoming client socket connection
                    else:
                        try:
                            data = self._receive(sock) # Gets the client message...
                            if data:
                                # ... and broadcasts it to all the connected clients
                                self._broadcast(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                        except socket.error:
                            # Broadcasts all the connected clients that a clients has left
                            self._broadcast(sock, "\nClient (%s, %s) is offline\n" % client_address)
                            print ("Client (%s, %s) is offline") % client_address
                            sock.close()
                            self.connections.remove(sock)
                            continue
        # Clears the socket connection
        self.stop()

    def run(self):
        """Given a host and a port, binds the socket and runs the server.
        """
        self._bind_socket()
        self._run()

    def stop(self):
        """
        Stops the server by setting the "running" flag before closing
        the socket connection.
        """
        self.running = False
        self.server_socket.close()


def main():
    """
    The main function of the program. It creates and runs a new ChatServer.
    """
    chat_server = ChatServer(_HOST, _PORT)
    chat_server.start()


if __name__ == '__main__':
    """The entry point of the program. It simply calls the main function.
    """
