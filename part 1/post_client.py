import pickle
import socket
import sys
from datetime import datetime

def main():

    # check for correct number of cl arguments 
    if len(sys.argv) != 5:
        print("Usage: python post_client.py <ip> <port> <username> 'message'")
        sys.exit(1)

    # define content
    ip = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3]
    message = sys.argv[4]
    timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    msg_data = (username, timestamp, message)


    try:
        # set up socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))

        client_socket.sendall(pickle.dumps(msg_data))

        # receive server data with buffer bytes
        response_data = client_socket.recv(1024)
        response = pickle.loads(response_data)
        print(response)

        if response.error:
            print(response.error)
        elif response.status:
            print(response.status)

                
    except ConnectionRefusedError:
        print("Connection refused")
    except Exception as e:
        print(f"Error occured {e}")

    if message.upper() == "EXIT":
        client_socket.sendall(pickle.dumps(("exit",)))
        client_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    main()