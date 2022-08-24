import socket
import tqdm
import os
BUFFER_SIZE = 4096
SERVER : str = input("Enter IP: ")
PORT = int(input("Enter PORT: "))
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
SEPARATOR = ":"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def receive(client):
    # Code to send files
    received = client.recv(BUFFER_SIZE).decode(FORMAT)
    filename , filesize= received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename} " , unit ="B", unit_scale=True, unit_divisor=1024)
    with open(f"./{filename}","wb") as f:
        while  True:
            bytes_read = client.recv(BUFFER_SIZE)
            if not bytes_read:
                progress.update(len(bytes_read))
                f.close()
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    
    client.close()        
    
receive(client)


