import socket
import ast
filename = "test_sended.py"

def process_data(target, iter):
    lib = __import__(filename.replace(".py", ""))
    result = lib.main(target, iter)
    if result:
        return result
    else:
        return False


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('127.0.0.1', 5001)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

def receive_all(sock, buffer_size=4096):
    data = b''
    while True:
        part = sock.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            # either 0 or end of data
            break
    return data


def save_script(script_string):
    with open("test_sended.py", 'w') as file:
        file.write(script_string)


while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data
        data = receive_all(connection)
        print('received {!r}'.format(data))
        if data:
            request = data.decode("utf-8")
            del data
            headers, body = request.split('\r\n\r\n', 1)
            boundary = headers[headers.index('boundary=') + 9:]
            del headers
            datas = body.split(f"--{boundary}")
            target = body.split(f"--{boundary}")[1].split("\r\n")[3]
            iter = body.split(f"--{boundary}")[2].split("\r\n")[3]
            file_data = body.split(f"--{boundary}")[3].split("\r\n")[3]
            del body
            iter = ast.literal_eval(iter)
            save_script(file_data)
            response = 'Success'
            connection.sendall(response.encode('utf-8'))
            result = process_data(target, iter)
            connection.sendall(result.encode('utf-8'))

    finally:
        # Clean up the connection
        connection.close()