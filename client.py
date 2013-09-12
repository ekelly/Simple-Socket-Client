#!/usr/bin/python

from optparse import OptionParser 
import socket
import ssl

# Parse the commandline input into a map of 
# name to values
def parse_input():
    usage = "usage: %prog [options] hostname NEU_ID"
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port", 
            help="TCP port that the server is listening on", 
            metavar="PORT")
    parser.add_option("-s", "--ssl", action="store_true", dest="ssl",
            help="Should this client connect using ssl", default=False)
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments")
    else:
        options.server = args[0]
        options.neuid = args[1]
    if options.port == None:
        if options.ssl:
            options.port = 27994
        else:
            options.port = 27993
    options.port = int(options.port)
    return options

# Open a socket to the server
def open_socket(server, port, use_ssl):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_ssl:
        s = ssl.wrap_socket(s)
    s.settimeout(5)
    s.connect((server, port))
    return s

# Close the socket
def close_socket(socket):
    socket.close()

# Parse the socket data
def parse_data(data):
    return data.split(' ')

# Receive data from the socket
def recv_data(socket):
    return socket.recv(4096)

# Send data on the socket
def send_data(socket, data):
    data = "cs5700fall2013 " + str(data) + "\n"
    return socket.send(data)

# Send the opening "hello" message to start us off
def send_hello(socket, neuid):
    return send_data(socket, "HELLO " + neuid)

# Is the socket message valid according to the given protocal?
def is_valid_msg(msg):
    msgLen = len(msg)
    if msgLen > 2:
        if msg[0] == "cs5700fall2013":
            if msgLen == 3:
                return msg[2] == "BYE\n"
            elif msgLen == 5:
                if msg[1] == "STATUS":
                    # have to chop off last character of msg[4]
                    # because last character should be \n
                    if msg[2].isdigit() and msg[4][:-1].isdigit():
                        if msg[4][-1:] == "\n":
                            return is_operator(msg[3])
    return False

# Is this string one of the 4 given mathematical operators?
def is_operator(op):
    return op in ["+", "-", "*", "/"]

# Calculate the mathematical solution to the problem
# round down to the nearest integer
def calculate_solution(left, operator, right):
    l = int(left)
    r = int(right)
    return { 
      '+': lambda: l + r,
      '-': lambda: l - r,
      '*': lambda: l * r,
      '/': lambda: l / r,
    }.get(operator, "+")()

# Entry point to the program
def main():
    args = parse_input()

    # Create a connection to the server
    socket = open_socket(args.server, args.port, args.ssl)
    send_hello(socket, args.neuid)

    # Listen for data and respond appropriately
    response = parse_data(recv_data(socket))
    while response:
        if is_valid_msg(response):
            if len(response) == 5:
                # feed teh rest of the response data directly
                # into calculate_solution
                solution = calculate_solution(*response[2:])
                sent_len = send_data(socket, solution)
            else:
                # Print the secret code
                print response[1]
                return
            response = parse_data(recv_data(socket))
        else:
            raise Exception('Bad response', response)

    # not necessary, but nice to close the socket
    close_socket(socket)

# These 2 lines allow us to import this file into another file 
# and test individual components without running it
if __name__ == "__main__":
    main()
