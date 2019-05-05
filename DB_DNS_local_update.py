import socket
import binascii
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from DB_DNS_local_create import DNS
import time
from libs_server_local import DB_DNS_in

engine = create_engine('sqlite:///DB_DNS_Server')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
query = session.query(DNS)
last = query.filter(DNS.dns_id).count()

z=1
while True:
    if z > last :
        time.sleep(20)
        print("Slept for 20 seconds")
        z=1
    else:
        menu = session.query(DNS).filter(DNS.dns_id == z).one()
        can_ttl = float(menu.Time) + float(int(menu.TTL, 16))  # can ttl
        if time.time()> can_ttl:
            List_out_call = {}
            List_out_call["ID"] = "A0A0"  # id request update ttl
            List_out_call["QR"] = "0"  # 0-requst , 1 answer
            List_out_call["OPCODE"] = "0000"  # 0- standart requst and variant
            List_out_call["AA"] = "0"  # Code answer
            List_out_call["TC"] = "0"  # TrunCation
            List_out_call["RD"] = "1"  # Recursion
            List_out_call["RA"] = "0"  # Recursion Available
            List_out_call["Z"] = "000"  # Reservation
            List_out_call["RCODE"] = "0000"  # Code answer(0,1,2,3,4,5,6-15)
            List_out_call["QDCOUNT"] = "0001"  # 1-requst
            List_out_call["ANCOUNT"] = "0000"  # Code answer
            List_out_call["NSCOUNT"] = "0000"  # numba write name servis available
            List_out_call["ARCOUNT"] = "0000"  # numba write recurs additionally

            Header_1 = List_out_call.get("QR") + List_out_call.get("OPCODE") + List_out_call.get(
                "AA") + List_out_call.get("TC") \
                       + List_out_call.get("RD")
            Header_2 = List_out_call.get("RA") + List_out_call.get("Z") + List_out_call.get("RCODE")

            Header_1_1 = Header_1[0:4]
            Header_1_2 = Header_1[4:8]
            Header_2_1 = Header_2[0:4]
            Header_2_2 = Header_2[4:8]
            List_out_call["Header"] = str(int((Header_1_1), 2)) + str(int((Header_1_2), 2)) \
                                      + str(int((Header_2_1), 2)) + str(int((Header_2_2), 2))
            name_hex = menu.NAME
            start_in = 0
            lis_name_hex = ""
            for i in range(0, len(name_hex), 2):
                if name_hex[i: i + 2] == "2e":  # 2e toshka
                    stop_in = i  # toshka
                    sum_in = str(hex(int((stop_in - start_in) / 2)))
                    if int(sum_in, 16) < 16:
                        lis_name_hex = lis_name_hex + "".join(sum_in[0] + sum_in[2] + name_hex[start_in:stop_in])
                        start_in = stop_in + 2
                    else:
                        lis_name_hex = lis_name_hex + "".join(sum_in[2] + sum_in[3] + name_hex[start_in:stop_in])
                        start_in = stop_in + 2


            stop_in = len(name_hex)
            sum_in = str(hex(int((stop_in - start_in) / 2)))
            lis_name_hex = lis_name_hex + "".join(sum_in[0] + sum_in[2] + name_hex[start_in:stop_in]) + "00"
            List_out_call["QNAME"] = lis_name_hex
            List_out_call["QTYPE"] = "0001"  # write A
            List_out_call["QCLASS"] = "0001"  # 1 internet

            message = List_out_call.get("ID") + List_out_call.get("Header") + List_out_call.get(
                "QDCOUNT") + List_out_call.get(
                "ANCOUNT") + List_out_call.get("NSCOUNT") + List_out_call.get("ARCOUNT") + List_out_call.get(
                "QNAME") + List_out_call.get("QTYPE") + List_out_call.get("QCLASS")
          #  print(message)

            host_apdate = '8.8.8.8'  # apdate adres DNS server
            port = 53  # Port to listen on (non-privileged ports are > 1023)

            UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("update ip", z)  # request dns server update ttl
            adres=(host_apdate, port)
            try:
                UDPServerSocket.sendto(binascii.unhexlify(message),adres )
                data,_ = UDPServerSocket.recvfrom(4096)
                in_message = binascii.hexlify(data).decode("utf-8")
            finally:
                UDPServerSocket.close()
            DB_DNS_in(in_message)
        z=z+1


session.commit()

