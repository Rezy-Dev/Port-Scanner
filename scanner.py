import sys
import socket
import datetime
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Adjust the timeout as needed
        result = sock.connect_ex((host, port))
        if result == 0:
            return port  # Return the opened port
        sock.close()
    except socket.error:
        pass  # Ignore connection errors

def print_banner():
    banner = '''
    #############################################
    #                                           #
    #           PORT SCANNER                     #
    #                                           #
    #############################################
    '''
    print(banner)

if len(sys.argv) != 2:
    print("Usage: python3 port_scanner.py <host>")
    sys.exit(1)

host = sys.argv[1]
print_banner()
print(f"Scanning all ports on host {host}...")
start_time = datetime.datetime.now()

max_workers = 100

executor = ThreadPoolExecutor(max_workers=max_workers)

futures = []

for port in range(1, 65536):
    future = executor.submit(scan_port, host, port)
    futures.append(future)

opened_ports = []

for future in futures:
    result = future.result()
    if result:
        opened_ports.append(result)

end_time = datetime.datetime.now()
scan_time = end_time - start_time

if opened_ports:
    print("Opened ports:")
    for port in opened_ports:
        print(f"Port {port} is open")
else:
    print("No open ports found")

print(f"Scanning completed in {scan_time}")
