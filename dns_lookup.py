#!/usr/bin/env python3
"""dns_lookup - DNS record lookup using socket."""
import sys, socket, struct
def resolve(hostname, record_type="A"):
    try:
        if record_type=="A":
            results=socket.getaddrinfo(hostname, None, socket.AF_INET)
            return list(set(r[4][0] for r in results))
        elif record_type=="AAAA":
            results=socket.getaddrinfo(hostname, None, socket.AF_INET6)
            return list(set(r[4][0] for r in results))
        elif record_type=="PTR":
            return [socket.gethostbyaddr(hostname)[0]]
        elif record_type=="MX":
            # Use system dig if available
            import subprocess
            r=subprocess.run(["dig","+short","MX",hostname],capture_output=True,text=True,timeout=5)
            return r.stdout.strip().split("\n") if r.stdout.strip() else []
        elif record_type=="NS":
            import subprocess
            r=subprocess.run(["dig","+short","NS",hostname],capture_output=True,text=True,timeout=5)
            return r.stdout.strip().split("\n") if r.stdout.strip() else []
    except Exception as e: return [str(e)]
    return []
if __name__=="__main__":
    if len(sys.argv)<2: print("Usage: dns_lookup <hostname> [A|AAAA|MX|NS|PTR]"); sys.exit(1)
    host=sys.argv[1]; rtype=sys.argv[2].upper() if len(sys.argv)>2 else "A"
    results=resolve(host, rtype)
    print(f"{host} {rtype} records:")
    for r in results: print(f"  {r}")
