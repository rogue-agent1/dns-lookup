#!/usr/bin/env python3
"""DNS record lookup using socket (no dnspython needed)."""
import sys, socket, struct, random

def build_query(domain, qtype=1):
    tid = random.randint(0,65535)
    header = struct.pack('>HHHHHH', tid, 0x0100, 1, 0, 0, 0)
    question = b''
    for part in domain.split('.'):
        question += bytes([len(part)]) + part.encode()
    question += b'\x00' + struct.pack('>HH', qtype, 1)
    return header + question

def parse_response(data):
    tid, flags, qdcount, ancount = struct.unpack('>HHHH', data[:8])
    offset = 12
    # Skip questions
    for _ in range(qdcount):
        while data[offset] != 0:
            offset += data[offset] + 1 if data[offset] < 192 else 2
            if data[offset-1] >= 192: break
        if data[offset] == 0: offset += 1
        offset += 4
    records = []
    for _ in range(ancount):
        # Skip name
        if data[offset] >= 192: offset += 2
        else:
            while data[offset] != 0: offset += data[offset]+1
            offset += 1
        rtype, rclass, ttl, rdlength = struct.unpack('>HHIH', data[offset:offset+10])
        offset += 10
        rdata = data[offset:offset+rdlength]
        offset += rdlength
        if rtype == 1:  # A
            records.append(('A', '.'.join(str(b) for b in rdata), ttl))
        elif rtype == 28:  # AAAA
            records.append(('AAAA', ':'.join(f'{rdata[i]:02x}{rdata[i+1]:02x}' for i in range(0,16,2)), ttl))
        elif rtype == 5:  # CNAME
            records.append(('CNAME', str(rdlength), ttl))
        else:
            records.append((f'TYPE{rtype}', f'{rdlength} bytes', ttl))
    return records

def lookup(domain, server='8.8.8.8'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    for qtype, name in [(1,'A'), (28,'AAAA')]:
        try:
            query = build_query(domain, qtype)
            sock.sendto(query, (server, 53))
            data, _ = sock.recvfrom(1024)
            records = parse_response(data)
            for rtype, rdata, ttl in records:
                print(f"  {rtype:6s} {rdata:40s} TTL={ttl}")
        except socket.timeout:
            pass
        except Exception as e:
            print(f"  {name}: error ({e})")
    sock.close()

if __name__ == '__main__':
    if len(sys.argv) < 2: print("Usage: dns_lookup.py <domain> [dns-server]"); sys.exit(1)
    domain = sys.argv[1]
    server = sys.argv[2] if len(sys.argv) > 2 else '8.8.8.8'
    print(f"DNS lookup: {domain} (via {server})\n")
    lookup(domain, server)
    # Also show socket resolution
    try:
        ips = socket.getaddrinfo(domain, None)
        seen = set()
        print(f"\nSystem resolver:")
        for family, _, _, _, addr in ips:
            ip = addr[0]
            if ip not in seen:
                seen.add(ip)
                t = 'IPv4' if family == socket.AF_INET else 'IPv6'
                print(f"  {t:5s} {ip}")
    except: pass
