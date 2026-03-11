#!/usr/bin/env python3
"""DNS lookup tool — zero dependencies (uses socket)."""
import socket, sys

def lookup(hostname, record_type="A"):
    try:
        if record_type == "A":
            return socket.gethostbyname_ex(hostname)
        elif record_type == "AAAA":
            results = socket.getaddrinfo(hostname, None, socket.AF_INET6)
            return list(set(r[4][0] for r in results))
        elif record_type == "ANY":
            results = socket.getaddrinfo(hostname, None)
            return list(set(r[4][0] for r in results))
    except socket.gaierror as e:
        return f"Error: {e}"

def reverse_lookup(ip):
    try: return socket.gethostbyaddr(ip)
    except socket.herror as e: return f"Error: {e}"

def test():
    result = lookup("localhost")
    assert "127.0.0.1" in str(result)
    rev = reverse_lookup("127.0.0.1")
    assert "localhost" in str(rev).lower()
    print(f"localhost → {result}")
    print(f"127.0.0.1 → {rev}")
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        host = sys.argv[1]; rtype = sys.argv[2] if len(sys.argv) > 2 else "A"
        print(lookup(host, rtype))
    else: test()
