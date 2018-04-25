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

def net_mask(ip):
    i = ip.with_netmask
    s = str(i)
    x = s.split('/')
    return x[1]

rb_nome = input("Digite o nome do RB: ")
portas_bridge = int(input("Quantas portas na bridge? "))
desig = input("Digite o designador: ")
vlan_ger_nome = ("GER-%s" % desig)
vlan_ger_tag = int(input("Digite a TAG da VLAN de GERENCIA: "))
ip_ger = ipaddress.ip_network(input("Digite o BLOCO IP de GERENCIA: "))

vlan_int_nome = ("INT-%s" % desig)
vlan_int_tag = int(input("Digite a TAG da VLAN de P2P: "))
ip_int = ipaddress.ip_network(input("Digite o BLOCO IP de P2P: "))
bloco_ip = ipaddress.ip_network(input("Digite o BLOCO IP ROTEADO: "))

print("")
print("")
print("")
print("interface vlan add name=%s vlan-id=%d interface=ether1" % (vlan_ger_nome,vlan_ger_tag))
print("interface vlan add name=%s vlan-id=%d interface=ether1" % (vlan_int_nome,vlan_int_tag))
print("")
      
print("interface bridge add name=BRIDGE1")

for i in range (2,portas_bridge+2):
    print("interface bridge port add interface=ether%d bridge=BRIDGE1" % i)
    i+=1

print("")

print("ip address add address=%s  netmask=%s interface=%s" % (ip_p2p(ip_ger), net_mask(ip_ger), vlan_ger_nome))
print("ip address add address=%s  netmask=%s interface=%s" % (ip_p2p(ip_int), net_mask(ip_int), vlan_int_nome))
print("ip address add address=%s  netmask=%s interface=BRIDGE1" % (ip_gw(bloco_ip), net_mask(bloco_ip)))
print("")

print("ip route vrf add routing-mark=VRF-CLIENTE route-distinguisher=10:10 interfaces=%s,BRIDGE1" % vlan_int_nome )
print("ip route add gateway=%s" % ip_gw(ip_ger))
print("ip route add gateway=%s routing-mark=VRF-CLIENTE" % ip_gw(ip_int))
print("")
      
print("snmp community add name=s1m_isp")
print("snmp set enabled=yes trap-community=s1m_isp trap-version=2")
print("system identity set name=%s" % rb_nome)

print("password new-password=linpus-20500 confirm-new-password=linpus-20500 old-password=")

print("")
