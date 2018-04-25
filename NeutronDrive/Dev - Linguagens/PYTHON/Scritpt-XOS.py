import ipaddress
"""
def gw_p2p(ip):
    print ("")
    print ("BLOCO: %s" % ip)
    print ("")
    for i in ip.hosts():
        s = str(i)
        x = s.split('.')
        z = int(x[-1])

        if z % 2 == 1:
            j = '.'.join(x)
            print ("%s GATEWAY" %  j)
        if z % 2 == 0:
            j = '.'.join(x)
            print ("%s P2P" % j)
"""
def ip_gw(ip):
    for i in ip.hosts():
        s = str(i)
        x = s.split('.')
        z = int(x[-1])
        if z % 2 == 1:
            j = '.'.join(x)
            return j

def ip_p2p(ip):
    for i in ip.hosts():
        s = str(i)
        x = s.split('.')
        z = int(x[-1])
        if z % 2 == 0:
            j = '.'.join(x)
            return j

def portas_tag():
    l = []
    ports = ""
    conc = '' #para concatenar com ports
    i = 1
    while True:
        portas_tagged = int(input("Quais portas serão TAG? (0 faz parar)"))   
        if portas_tagged == 0:
            break
        i = i + 1
        l.append(portas_tagged)
    for x in l:
        if x == l[-1]:
            ports = ("%d" % x)
        else:
            ports = ("%s" % (x) + ", ") #python 3..
        conc += str(ports)
    return conc

def portas_untag():
    l2 = []
    ports2 = ""
    conc2 = '' #para concatenar com ports
    i = 1
    while True:
        portas_untagged = int(input("Quais portas serão UNTAG? (0 faz parar)"))   
        if portas_untagged == 0:
            break
        i = i + 1
        l2.append(portas_untagged)
    for x in l2:
        if x == l2[-1]:
            ports2 = ("%d" % x)
        else:
            ports2 = ("%s" % (x) + ", ") #python 3..
        conc2 += str(ports2)
    return conc2

sw_nome = input("Digite o nome do SW: ")
qtde_portas = int(input("Quantas portas possui o SWITCH? "))
desig = input("Digite o designador: ")
desc = input("Digite o nome do cliente: ")

vlan_ger_nome = ("GER-%s" % desig)
vlan_ger_tag = int(input("Digite a TAG da VLAN de GERENCIA: "))

ip_ger = ipaddress.ip_network(input("Digite o BLOCO IP de GERENCIA: "))
portas_tag_ger = portas_tag()
portas_untag_ger = portas_untag()


vlan_int_nome = ("INT-%s" % desig)
vlan_int_tag = int(input("Digite a TAG da VLAN de P2P: "))

ip_int = ipaddress.ip_network(input("Digite o BLOCO IP de P2P: "))
bloco_ip = ipaddress.ip_network(input("Digite o BLOCO IP ROTEADO: "))
portas_tag_int = portas_tag()
portas_untag_int = portas_untag()

print ("")
print ("")
print ("====================================================")
print ("COPIE ESSAS INFORMAÇÕES E COLE NO SW")
print ("====================================================")
print ("")
print ("")
print ("configure snmp sysName %s" % sw_nome)
print ("configure timezone -180")
print ("enable jumbo-frame ports all")
print ("configure snmp add community readonly s1m_isp")
print ("configure vlan default delete ports all")
print ("configure VR-Default delete ports 1-%d" % qtde_portas)
print ("configure ports 1-%d display-string LIVRE" % qtde_portas)
print ("disable ports all")
print ("enable ports %s, %s" % (portas_tag_ger,portas_untag_ger))
print ("configure vlan Mgmt ipaddress 192.168.1.1/24")
print ("disable snmp community private")
print ("disable snmp community public")
print ("configure snmpv3 add community s1m_isp name s1m_isp user v1v2c_ro")
print ("create account admin sitecnet")
print ("335-pbsitec")


print ("")

print ("create vlan %s tag %d" %(vlan_ger_nome, vlan_ger_tag))
print ("configure vlan %s description %s" % (vlan_ger_nome, desc))
print ("configure vlan %s ipaddress %s/30" % (vlan_ger_nome, ip_p2p(ip_ger)))
print ("enable ipforwarding vlan %s" % vlan_ger_nome)
print ("configure iproute add default %s" % ip_gw(ip_ger))
if not portas_tag_ger:
    ("")
else:
    print ("")
    print ("configure vlan %s add ports %s tagged" % (vlan_ger_nome, portas_tag_ger), end='')
if not portas_untag_ger:
    ("")    
else:
    print ("")
    print ("configure vlan %s add ports %s untagged" % (vlan_ger_nome, portas_untag_ger), end='')
print ("")
print ("")


print ("create vlan %s tag %d" %(vlan_int_nome, vlan_int_tag))
print ("configure vlan %s description %s" % (vlan_ger_nome, desc))


if not portas_tag_int:
    ("")
else:
    print ("")
    print ("configure vlan %s add ports %s tagged" % (vlan_int_nome, portas_tag_int), end='')
if not portas_untag_int:
    ("")    
else:
    print ("")
    print ("configure vlan %s add ports %s untagged" % (vlan_int_nome, portas_untag_int), end='')

print ("")

print ("exit")
print ("")
print ("LOGAR COM O USUÁRIO SITECNET E SENHA DEFAULT")
print ("")
print ("")



###########################################################################################

import serial

ser = serial.Serial("/dev/ttyUSB0")

ser.write(bytearray("configure snmp sysName %s \n" % sw_nome, 'utf-8'))
ser.write(bytearray("configure snmp sysName %s \n" % sw_nome, 'utf-8'))
ser.write(bytearray("configure timezone -180 \n", 'utf-8'))
ser.write(bytearray("enable jumbo-frame ports all \n", 'utf-8'))
ser.write(bytearray("configure snmp add community readonly s1m_isp \n", 'utf-8'))
ser.write(bytearray("configure vlan default delete ports all \n", 'utf-8'))
ser.write(bytearray("configure VR-Default delete ports 1-%d \n" % qtde_portas, 'utf-8'))
ser.write(bytearray("configure ports 1-%d display-string LIVRE \n" % qtde_portas, 'utf-8'))
ser.write(bytearray("disable ports all \n", 'utf-8'))
ser.write(bytearray("enable ports %s, %s \n" % (portas_tag_ger,portas_untag_ger), 'utf-8'))
ser.write(bytearray("configure vlan Mgmt ipaddress 192.168.1.1/24 \n", 'utf-8'))
ser.write(bytearray("disable snmp community private \n", 'utf-8'))
ser.write(bytearray("disable snmp community public \n", 'utf-8'))
ser.write(bytearray("configure snmpv3 add community s1m_isp name s1m_isp user v1v2c_ro \n", 'utf-8'))
ser.write(bytearray("configure iproute add default \n", 'utf-8'))
ser.write(bytearray("create account admin sitecnet \n", 'utf-8'))
ser.write(bytearray("335-pbsitec \n", 'utf-8'))
ser.write(bytearray("335-pbsitec \n", 'utf-8'))

ser.write(bytearray("create vlan %s tag %d \n" %(vlan_ger_nome, vlan_ger_tag), 'utf-8'))
ser.write(bytearray("configure vlan %s description %s \n" % (vlan_ger_nome, desc), 'utf-8'))
ser.write(bytearray("configure vlan %s ipaddress %s/30 \n" % (vlan_ger_nome, ip_p2p(ip_ger)), 'utf-8'))
ser.write(bytearray("enable ipforwarding vlan %s \n" % vlan_ger_nome, 'utf-8'))
ser.write(bytearray("configure iproute add default %s \n" % ip_gw(ip_ger), 'utf-8'))
if not portas_tag_ger:
    ser.write(bytearray("\n"))
else:
    ser.write(bytearray("configure vlan %s add ports %s tagged \n" % (vlan_ger_nome, portas_tag_ger), 'utf-8'))
if not portas_untag_ger:
    ser.write(bytearray("\n"))
else:
    ser.write(bytearray("configure vlan %s add ports %s untagged \n" % (vlan_ger_nome, portas_untag_ger), 'utf-8'))
print ("")

ser.write(bytearray("create vlan %s tag %d \n" %(vlan_int_nome, vlan_int_tag), 'utf-8'))
ser.write(bytearray("configure vlan %s description %s \n" % (vlan_int_nome, desc), 'utf-8'))

if not portas_tag_int:
    ser.write(bytearray("\n"))
else:
    ser.write(bytearray("configure vlan %s add ports %s tagged \n" % (vlan_int_nome, portas_tag_int), 'utf-8'))
if not portas_untag_int:
    ser.write(bytearray("\n"))
else:
    ser.write(bytearray("configure vlan %s add ports %s untagged \n" % (vlan_int_nome, portas_untag_int), 'utf-8'))

ser.write(bytearray("exit \n", 'utf-8'))
