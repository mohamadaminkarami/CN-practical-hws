import threading
from client_wrapper import handle_client_wrapper, handle_timeout
from server_wrapper import handle_server_wrapper

if __name__ == "__main__":
    client_wrapper_thread = threading.Thread(target=handle_client_wrapper)
    timeout_thread = threading.Thread(target=handle_timeout)
    server_wrapper_thread = threading.Thread(target=handle_server_wrapper)

    client_wrapper_thread.start()
    timeout_thread.start()
    server_wrapper_thread.start()

    client_wrapper_thread.join()
    timeout_thread.join()
    server_wrapper_thread.join()