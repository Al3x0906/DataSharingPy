import socket
import tqdm
import os
BUFFER_SIZE = 4096
SERVER: str = input("Enter IP: ")
PORT = int(input("Enter PORT: "))
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
SEPARATOR = ":"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def receive(client):
    received = client.recv(BUFFER_SIZE).decode(FORMAT)
    num_of_files = int(received)
    client.send("SUCCESS".encode(FORMAT))

    for i in range(num_of_files):
        received = client.recv(BUFFER_SIZE).decode(FORMAT)
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        client.send("SUCCESS".encode(FORMAT))
        progress = tqdm.tqdm(range(
            filesize), f"Receiving {filename} ", unit="B", unit_scale=True, unit_divisor=1024)
        with open(f"./{filename}", "wb") as f:
            while True:
                bytes_read = client.recv(BUFFER_SIZE).decode(FORMAT)
                progress.update(len(bytes_read))
                if "{SEPARATOR}SENT{SEPARATOR}" in bytes_read:
                    bytes_read = bytes_read.replace(
                        "{SEPARATOR}SENT{SEPARATOR}", "")
                    bytes_read = bytes(bytes_read, FORMAT)
                    f.write(bytes_read)
                    client.send("SUCCESS".encode(FORMAT))
                    f.close()
                    break
                bytes_read = bytes(bytes_read, FORMAT)
                f.write(bytes_read)
                progress.update(len(bytes_read))

    client.close()


receive(client)
