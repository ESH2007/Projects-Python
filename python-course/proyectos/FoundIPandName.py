import socket

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

input("Press ENTER to continue...")
input("El nombre de tu ordenador es: " + hostname)
input("Tu direccion de IP es: " + ip)

input("thanks for giving me your IP " + hostname)

