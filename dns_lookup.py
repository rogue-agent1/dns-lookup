#!/usr/bin/env python3
"""DNS lookup — resolve hostnames using socket (no dnspython)."""
import sys, socket
def resolve(host, family=socket.AF_INET):
    try: return [addr[4][0] for addr in socket.getaddrinfo(host, None, family)]
    except socket.gaierror: return []
def cli():
    if len(sys.argv) < 2: print("Usage: dns_lookup <hostname> [--all]"); sys.exit(1)
    host = sys.argv[1]
    ipv4 = list(set(resolve(host, socket.AF_INET)))
    ipv6 = list(set(resolve(host, socket.AF_INET6)))
    print(f"  Host: {host}")
    if ipv4: print(f"  A:    {', '.join(ipv4)}")
    if ipv6: print(f"  AAAA: {', '.join(ipv6)}")
    if not ipv4 and not ipv6: print("  No records found")
if __name__ == "__main__": cli()
