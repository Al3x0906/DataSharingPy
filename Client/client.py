import socket
import tqdm
import os
BUFFER_SIZE = 4096
PORT = 5001
SERVER = '192.168.56.1'
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
SEPARATOR = ":"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(client):
    # Code to send files
    received = client.recv(BUFFER_SIZE).decode(FORMAT)
    print(received)
    filename , filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    print(filename,filesize)

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename} " , unit ="B", unit_scale=True, unit_divisor=1024)
    with open(f"./{filename}","wb") as f:
        while True :
            bytes_read = client.recv(BUFFER_SIZE)
            if not bytes_read:
                progress.update(len(bytes_read))
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    client.close()        
    
send(client)


