from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from DB_DNS_local_create import DNS
import time






def DB_DNS_in(in_message):
    # distionary incoming message
    #
    engine = create_engine('sqlite:///DB_DNS_Server')
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(DNS)
    List_db_dns_in = {}
    List_db_dns_in["ID"] = in_message[0:4]
    if List_db_dns_in.get("ID") == "a0a0" or List_db_dns_in.get("ID") == "A0A0":  # message answer dns
        id2 = bin(int((in_message[4:8]), 16))
        List_db_dns_in["QR"] = id2[2]
        List_db_dns_in["OPCODE"] = id2[3:7]
        List_db_dns_in["AA"] = id2[7]
        List_db_dns_in["TC"] = id2[8]
        List_db_dns_in["RD"] = id2[9]
        List_db_dns_in["RA"] = id2[10]
        List_db_dns_in["Z"] = id2[11:14]
        List_db_dns_in["RCODE"] = id2[14:18]
        List_db_dns_in["QDCOUNT"] = in_message[8:12]
        List_db_dns_in["ANCOUNT"] = in_message[12:16]
        List_db_dns_in["NSCOUNT"] = in_message[16:20]
        List_db_dns_in["ARCOUNT"] = in_message[20:24]
        i = (int((in_message[24:26]), 16))
        y = i

        while True:
            if (in_message[(26 + y * 2):(28 + y * 2)]) == "00":
                z = y
                List_db_dns_in["QNAME"] = in_message[24:28 + y * 2]
                break
            else:
                i = (int((in_message[(26 + y * 2):(28 + y * 2)]), 16))
                y = y + i + 1

        List_db_dns_in["QTYPE"] = in_message[(28 + z * 2):(32 + z * 2)]
        List_db_dns_in["QCLASS"] = in_message[(32 + z * 2):(36 + z * 2)]
        id3 = bin(int(in_message[(36 + z * 2):(40 + z * 2)], 16))
        if id3[2:4] == "11":
            List_db_dns_in["NAME"] = in_message[(36 + z * 2):(40 + z * 2)]
        else:
            return print('NAME adress non Available')


        List_db_dns_in["TYPE"] = in_message[(40 + z * 2):(44 + z * 2)]
        List_db_dns_in["CLASS"] = in_message[(44 + z * 2):(48 + z * 2)]
        List_db_dns_in["TTL"] = in_message[(48 + z * 2):(56 + z * 2)]
        if in_message[(56 + z * 2):(60 + z * 2)] == "0004":
            List_db_dns_in["RDLENGTH"] = in_message[(56 + z * 2):(60 + z * 2)]
        else:
            return print('ip adress non Available')

        if List_db_dns_in["ANCOUNT"] == "0001":
            List_db_dns_in["RDDATA"] = in_message[(60 + z * 2):(68 + z * 2)]
        elif List_db_dns_in["ANCOUNT"] == "0002":
            List_db_dns_in["RDDATA"] = in_message[(60 + z * 2):(100 + z * 2)]
        elif List_db_dns_in["ANCOUNT"] == "0003":
            List_db_dns_in["RDDATA"] = in_message[(60 + z * 2):(140 + z * 2)]
        elif List_db_dns_in["ANCOUNT"] == "0004":
            List_db_dns_in["RDDATA"] = in_message[(60 + z * 2):(180 + z * 2)]
        elif List_db_dns_in["ANCOUNT"] == "0005":
            List_db_dns_in["RDDATA"] = in_message[(60 + z * 2):(220 + z * 2)]
        List_db_dns_in["List_db_dns_in"] = in_message

        # add db  # write A # 1 internet
        if List_db_dns_in["QTYPE"] == "0001" and List_db_dns_in["QCLASS"] == "0001"and List_db_dns_in["RCODE"]=="0000":
            id4 = bin(int(List_db_dns_in.get("NAME"), 16))
            stpname = int(id4[4:18], 2)
            name_lend = int(List_db_dns_in.get("List_db_dns_in")[0 + stpname * 2:2 + stpname * 2])
            start_ind = 2 + stpname * 2
            stop_ind = 2 + stpname * 2 + name_lend * 2
            name = List_db_dns_in.get("List_db_dns_in")[start_ind:stop_ind]
            s = 2
            nam_lend = int(List_db_dns_in.get("List_db_dns_in")[stop_ind:2 + stop_ind], 16)

            while True:
                if nam_lend == 00:
                    break

                else:
                    start_ind = s + stop_ind
                    stop_ind = s + stop_ind + nam_lend * 2
                    name = name + "2e" + (List_db_dns_in.get("List_db_dns_in")[start_ind:stop_ind])
                    nam_lend = int(List_db_dns_in.get("List_db_dns_in")[stop_ind:2 + stop_ind], 16)


            filt = query.filter(DNS.NAME == name).count()
            if filt == 1:
                query.update({DNS.TTL: List_db_dns_in.get("TTL")})
                query.update({DNS.Time: time.time()})
            else:
                DB_DNS_add = DNS(NAME=name,
                             TYPE=List_db_dns_in.get("TYPE"),
                             CLASS=List_db_dns_in.get("CLASS"),
                             TTL=List_db_dns_in.get("TTL"),
                             ANCOUNT=List_db_dns_in.get("ANCOUNT"),
                             RDLENGTH=List_db_dns_in.get("RDLENGTH"),
                             RDATA=List_db_dns_in.get("RDDATA"),
                             Time=time.time())
                session.add(DB_DNS_add)
            session.commit()
        else:
            pass

    else: #message incoming db_dns
        id2 = bin(int((in_message[4:8]), 16))
        List_db_dns_in["QR"] = id2[2]
        List_db_dns_in["OPCODE"] = id2[3:7]
        List_db_dns_in["AA"] = id2[7]
        List_db_dns_in["TC"] = id2[8]
        List_db_dns_in["RD"] = id2[9]
        List_db_dns_in["RA"] = id2[10]
        List_db_dns_in["Z"] = id2[11:14]
        List_db_dns_in["RCODE"] = id2[14:18]
        List_db_dns_in["QDCOUNT"] = in_message[8:12]
        List_db_dns_in["ANCOUNT"] = in_message[12:16]
        List_db_dns_in["NSCOUNT"] = in_message[16:20]
        List_db_dns_in["ARCOUNT"] = in_message[20:24]
        i = (int((in_message[24:26]), 16))
        y = i

        while True:
            if (in_message[(26 + y * 2):(28 + y * 2)]) == "00":
                z = y
                List_db_dns_in["QNAME"] = in_message[24:28 + y * 2]
                break
            else:
                i = (int((in_message[(26 + y * 2):(28 + y * 2)]), 16))
                y = y + i + 1

        List_db_dns_in["QTYPE"] = in_message[(28 + z * 2):(32 + z * 2)]
        List_db_dns_in["QCLASS"] = in_message[(32 + z * 2):(36 + z * 2)]

        List_db_dns_in["List_db_dns_in"] = in_message
        List_db_dns_out = {}
        List_db_dns_out["ID"] = List_db_dns_in["ID"]
        List_db_dns_out["QR"] = "1"  # 0-requst , 1 answer
        List_db_dns_out["OPCODE"] = List_db_dns_in["OPCODE"]  # 0- standart requst and variant
        List_db_dns_out["AA"] = List_db_dns_in["AA"]  # Code answer
        List_db_dns_out["TC"] = List_db_dns_in["TC"]  # TrunCation
        List_db_dns_out["RD"] = "1"  # Recursion
        List_db_dns_out["RA"] = "1"  # Recursion Available
        List_db_dns_out["Z"] = "000"  # Reservation
        l = (int((List_db_dns_in.get("QNAME")[0:2]), 16))
        qname = (List_db_dns_in.get("QNAME")[2: 2 + l * 2])
        while True:
            if (List_db_dns_in.get("QNAME")[2 + l * 2:4 + l * 2]) == "00":
                break
            else:
                m = int(List_db_dns_in.get("QNAME")[2 + l * 2:4 + l * 2], 16)
                qname = qname + "2e" + (List_db_dns_in.get("QNAME")[4 + l * 2:4 + (l + m) * 2])
                l = l + m + 1


        requst = session.query(DNS).filter(DNS.NAME == qname).first()
        if requst is not None:
            #print("Yes")
            List_db_dns_out["RCODE"] = "0000"  # Code answer(0,1,2,3,4,5,6-15)
            List_db_dns_out["QDCOUNT"] = List_db_dns_in["QDCOUNT"]  # 1-requst
            List_db_dns_out["ANCOUNT"] = requst.ANCOUNT  # Code answer 1  one  count db
            # List_db_dns_out["NSCOUNT"]= requst.dns_id  # format data xxxx
            List_db_dns_out["NSCOUNT"] = List_db_dns_in["NSCOUNT"]  # numba write name servis available  #default 0000
            List_db_dns_out["ARCOUNT"] = List_db_dns_in["ARCOUNT"]  # numba write recurs additionally
            List_db_dns_out["QNAME"] = List_db_dns_in["QNAME"]
            List_db_dns_out["QTYPE"] = List_db_dns_in["QTYPE"]
            List_db_dns_out["QCLASS"] = List_db_dns_in["QCLASS"]
            Header_1 = List_db_dns_out.get("QR") + List_db_dns_out.get("OPCODE") + List_db_dns_out.get(
                "AA") + List_db_dns_out.get("TC") + List_db_dns_out.get("RD")
            Header_2 = List_db_dns_out.get("RA") + List_db_dns_out.get("Z") + List_db_dns_out.get("RCODE")
            Header_1_1 = Header_1[0:4]
            Header_1_2 = Header_1[4:8]
            Header_2_1 = Header_2[0:4]
            Header_2_2 = Header_2[4:8]
            List_db_dns_out["Header"] = str(int((Header_1_1), 2)) + str(int((Header_1_2), 2)) \
                                        + str(int((Header_2_1), 2)) + str(int((Header_2_2), 2))
            List_db_dns_out["NAME"] = "C00C"  # format Message compression 44
            List_db_dns_out["TYPE"] = requst.TYPE
            List_db_dns_out["CLASS"] = requst.CLASS
            List_db_dns_out["TTL"] = requst.TTL
            List_db_dns_out["RDLENGTH"] = requst.RDLENGTH
            List_db_dns_out["RDATA"] = requst.RDATA
        else:
            #print("no")
            List_db_dns_out["RCODE"] = "0010"  # Code answer(0,1,2,3,4,5,6-15) Server failure
            List_db_dns_out["QDCOUNT"] = List_db_dns_in["QDCOUNT"]  # 1-requst
            List_db_dns_out["ANCOUNT"] = "0000"  # Code answer 1  one  count db
            # List_db_dns_out["NSCOUNT"]= requst.dns_id  # format data xxxx
            List_db_dns_out["NSCOUNT"] = List_db_dns_in["NSCOUNT"]  # numba write name servis available  #default 0000
            List_db_dns_out["ARCOUNT"] = List_db_dns_in["ARCOUNT"]  # numba write recurs additionally
            List_db_dns_out["QNAME"] = List_db_dns_in["QNAME"]
            List_db_dns_out["QTYPE"] = List_db_dns_in["QTYPE"]
            List_db_dns_out["QCLASS"] = List_db_dns_in["QCLASS"]
            Header_1 = List_db_dns_out.get("QR") + List_db_dns_out.get("OPCODE") + List_db_dns_out.get(
                "AA") + List_db_dns_out.get("TC") \
                       + List_db_dns_out.get("RD")
            Header_2 = List_db_dns_out.get("RA") + List_db_dns_out.get("Z") + List_db_dns_out.get("RCODE")
            Header_1_1 = Header_1[0:4]
            Header_1_2 = Header_1[4:8]
            Header_2_1 = Header_2[0:4]
            Header_2_2 = Header_2[4:8]
            List_db_dns_out["Header"] = str(int((Header_1_1), 2)) + str(int((Header_1_2), 2)) \
                                        + str(int((Header_2_1), 2)) + str(int((Header_2_2), 2))
            List_db_dns_out["NAME"] = "C00C"  # format Message compression 44
            List_db_dns_out["TYPE"] = "0001"
            List_db_dns_out["CLASS"] = "0001"
            List_db_dns_out["TTL"] = "0000"
            List_db_dns_out["RDLENGTH"] = "0004"
            List_db_dns_out["RDATA"] = "00000000"

        session.commit()
        message_db_dns_out = List_db_dns_out.get("ID") + List_db_dns_out.get("Header") + List_db_dns_out.get("QDCOUNT") \
                             + List_db_dns_out.get("ANCOUNT") + List_db_dns_out.get("NSCOUNT")\
                             + List_db_dns_out.get("ARCOUNT") + List_db_dns_out.get("QNAME") + List_db_dns_out.get("QTYPE")\
                             + List_db_dns_out.get("QCLASS") + List_db_dns_out.get("NAME") + List_db_dns_out.get("TYPE")\
                             + List_db_dns_out.get("CLASS") + List_db_dns_out.get("TTL") + List_db_dns_out.get("RDLENGTH")\
                             + List_db_dns_out.get("RDATA")


        return message_db_dns_out


