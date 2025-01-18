import socket

def is_internet_available(host="8.8.8.8", port=53, timeout=3):
    """
    Checks if the internet is available by attempting to connect to a DNS server (default: Google DNS).

    :param host: The host to connect to. Default is Google's public DNS server (8.8.8.8).
    :param port: The port to connect to. Default is 53.
    :param timeout: Timeout in seconds for the connection attempt.
    :return: True if the connection is successful, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        return True
    except (socket.timeout, socket.error):
        return False

if __name__ == "__main__":
    if is_internet_available():
        print("Internet connection is available.")
    else:
        internet_connection_error_popup()
