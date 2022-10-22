import socket
import threading
import os
import tqdm
import sys

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, 0)
FORMAT = 'utf-8'
SEPARATOR = ":"
BUFFER_SIZE = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def file_paths():
    fn = sys.argv
    fn.pop(0)
    return fn


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected: ")
    files = file_paths()
    num_of_files = len(files)
    conn.send(f"{num_of_files}".encode(FORMAT))
    ack = conn.recv(BUFFER_SIZE).decode(FORMAT)
    if ack != "SUCCESS":
        print("ERROR")
        return

    for file in files:
        filesize = os.path.getsize(file)
        conn.send(f"{file}{SEPARATOR}{filesize}".encode(FORMAT))
        ack = conn.recv(BUFFER_SIZE).decode(FORMAT)

        progress = tqdm.tqdm(range(
            filesize), f"Sending {file}", unit="B", unit_scale=True, unit_divisor=1024)

        with open(file, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    progress.update(len(bytes_read))
                    conn.send("{SEPARATOR}SENT{SEPARATOR}".encode(FORMAT))
                    ack = conn.recv(BUFFER_SIZE).decode(FORMAT)
                    ##progress.set_description("We finished")
                    if ack == "SUCCESS":
                        f.close()
                        break
                    else:
                        print(f"{file} not sent succesfully!!")
                conn.send(bytes_read)
                progress.update(len(bytes_read))
    conn_close(conn)


def conn_close(conn):
    print("\nConnection closed!!")
    conn.close()


def start(server):
    server.listen()
    print(f"[LISTENING] on {server.getsockname()}")

    conn, addr = server.accept()
    # thread = threading.Thread(target=handle_client, args=(conn, addr))
    # thread.start()
    # print(f"[ACTIVE] {threading.active_count()-1} ")
    handle_client(conn, addr)
    print("FILE SENT SUCCESSFULLY ")
    server.close()


print("[STARTING] server is starting : ")

start(server)
