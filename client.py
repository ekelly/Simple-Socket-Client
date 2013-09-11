#!/usr/bin/python

from optparse import OptionParser 
import socket

# Parse the commandline input into a map of 
# name to values
def parse_input():
    usage = "usage: %prog [options] hostname NEU_ID"
    parser = OptionParser(usage)
    parser.add_option("-p", "--port", dest="port", 
            help="TCP port that the server is listening on", 
            metavar="PORT", default=27993)
    parser.add_option("-s", "--ssl", action="store_true", dest="ssl",
            help="Should this client connect using ssl", default=False)
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments")
    else:
        options.server = args[0]
        options.neuid = args[1]
    return options

# Open a socket to the server
def open_socket(server, port):
    print "open_socket: " + server + ":" + str(port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((server, port))
    return s

# Close the socket
def close_socket(socket):
    print "close_scoket"
    socket.close()
    return

# Parse the socket data
# Byte array -> string[]
def parse_data(data):
    print "parse_data"
    return data.split(' ')

# Receive data from the socket
def recv_data(socket):
    print "recv_data"
    return socket.recv(4096)

# Send data on the socket
def send_data(socket, data):
    print "send_data"
    data = "cs5700fall2013 " + str(data) + "\n"
    return socket.send(data)

# Send the opening "hello" message to start us off
def send_hello(socket, neuid):
    print "send_hello"
    return send_data(socket, "HELLO " + neuid)

# Convert the given string representation of the number
# to a number (int or float)
def num(s):
    print "num"
    try:
        return int(s)
    except ValueError:
        return float(s)

# Calculate the mathematical solution to the problem
# round down to the nearest integer
def calculate_solution(left, operator, right):
    print "calculate_solution"  
    l = num(left)
    r = num(right)
    return { 
      '+': lambda: l + r,
      '-': lambda: l - r,
      '*': lambda: l * r,
      '/': lambda: l / r,
    }.get(operator, "+")()

# Entry point to the program
def main():
    args = parse_input()
    socket = open_socket(args.server, args.port)
    send_hello(socket, args.neuid)
    response = parse_data(recv_data(socket))
    while response:
      print response
      if len(response) == 5:
          solution = calculate_solution(*response[2:])
          sent_len = send_data(socket, solution)
      else:
          print response
          print "HOORAY"
          return
      response = parse_data(recv_data(socket))

    print str(args)

# These 2 lines allow us to import this file into another file 
# and test individual components without running it
if __name__ == "__main__":
    main()