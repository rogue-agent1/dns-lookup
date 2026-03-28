#!/usr/bin/env python3
"""dns_lookup - DNS lookup with multiple record types."""
import sys, socket, subprocess

def resolve(host, record_type='A'):
    try:
        result = subprocess.check_output(['dig', '+short', host, record_type], text=True, timeout=5).strip()
        return result.splitlines() if result else []
    except:
        if record_type == 'A':
            try: return [socket.gethostbyname(host)]
            except: return []
        return []

def reverse(ip):
    try: return socket.gethostbyaddr(ip)[0]
    except: return 'N/A'

def main():
    args = sys.argv[1:]
    if not args or '-h' in args:
        print("Usage: dns_lookup.py HOST [A|AAAA|MX|NS|TXT|CNAME|SOA] [--reverse IP]"); return
    if args[0] == '--reverse':
        print(f"  {args[1]} -> {reverse(args[1])}"); return
    host = args[0]
    types = [a.upper() for a in args[1:] if a.upper() in ('A','AAAA','MX','NS','TXT','CNAME','SOA','PTR')]
    if not types: types = ['A','AAAA','MX','NS']
    for t in types:
        records = resolve(host, t)
        if records:
            print(f"  {t}:")
            for r in records: print(f"    {r}")
        else:
            print(f"  {t}: (none)")

if __name__ == '__main__': main()
