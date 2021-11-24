from netmiko import ConnectHandler
import msvcrt as m
import getpass

def checkIP(ip):
    octet=ip.split('.') 
    if len(octet) == 4:
        for i in range (4):
            if octet[i] < '0' or octet[i] > '255' or octet == '':
                return False
            else: return True
    else: return False

#----------------------------------------------------------------------------------------------------

ip_dev = input('Nhap ip cua thiet bi: ')
usn = input('Nhap username: ')
pw = getpass.getpass('Nhap password: ')
if checkIP(ip_dev) == True:
    info_dev = {
        'device_type':'cisco_ios',
        'ip': ip_dev,
        'username':usn,
        'password':pw,
        'secret':'cisco'
    }
    print('Ket noi thanh cong!\n')
else:
    print('Thong tin sai. Ban hay nhap lai.\n')
net_connect = ConnectHandler(**info_dev)
print(net_connect.find_prompt())

#-----------------------------------------------------------------------------------------------------
#XEM THÔNG TIN THIẾT BỊ
#-----------------------------------------------------------------------------------------------------

def info_device():
    net_connect = ConnectHandler(**info_dev)
    print("\t\n***Thong tin cua thiet bi***\n")
    print(net_connect.send_command('show arp'))

    print("\t\n***Trang thai cac cong***\n")
    print(net_connect.send_command('show ip interface brief'))

    dev_name = str(net_connect.find_prompt())

    if dev_name[0] == 'R':
        print("\t\n***Routing table***\n")
        print(net_connect.send_command('show ip route'))
    else:
        print("\t\n***VLAN***\n")
        print(net_connect.send_command('show vlan'))

#-----------------------------------------------------------------------------------------------------
#CẤU HÌNH INTERFACE
#-----------------------------------------------------------------------------------------------------

def config_int():
    net_connect = ConnectHandler(**info_dev)
    dict_int = {}
    while True:
        end = input('Nhấn Enter để tiếp tục hoặc end để kết thúc.\n')
        if end != 'end':
            int = input("Interface:\t")
            ip_int = input("IP address + Subnet mark:\t")
            dict_int.setdefault(int, ip_int)
        else:
            break

    net_connect.enable()
    for a in dict_int:
        int_ip = ["interface "+a, "no shut", "ip address "+dict_int[a],"exit"]
        print(net_connect.send_config_set(int_ip))
    print("\n\tDone!!!\n")
    print(net_connect.send_command("show ip int brief"))
    


#-----------------------------------------------------------------------------------------------------
#CẤU HÌNH TRUNKING
#-----------------------------------------------------------------------------------------------------

def config_tru():
    net_connect = ConnectHandler(**info_dev)
    list_tru = []
    while True:
        end = input('Nhấn Enter để tiep tuc hoặc end để kết thúc.\n')
        if end != 'end':
            int_tru = input("Interface:\t")
            list_tru.append(int_tru)
        else: break


    net_connect.enable()
    for b in list_tru:
        config_tru = ["interface "+b, "switchport trunk encapsulation dot1q","switchport mode trunk"]
        print(net_connect.send_config_set(config_tru))
    print("\n\tDone!!!\n")
    print(net_connect.send_command("show int trunk"))
    




#-----------------------------------------------------------------------------------------------------
#CẤU HÌNH VLAN
#-----------------------------------------------------------------------------------------------------

def config_vlan():
    net_connect = ConnectHandler(**info_dev)
    dict_vlan = {}
    list_int = {}
    while True:
        end = input('Nhấn Enter để tiếp tục hoặc end để kết thúc.\n')
        if end != 'end':
            vlan = input("VLAN:\t")
            vlan_name = input("Ten VLAN:\t")
            print('\nNhap interface ap dung VLAN - example: e0/1,e0/2,...\n')
            vlan_int = input("Nhap interface:\t")
            list_int.setdefault(vlan_int, vlan)
            dict_vlan.setdefault(vlan, vlan_name)
        else: break

    net_connect.enable()
    for c in dict_vlan:
        config_vlan = ["vlan "+ c, "name "+dict_vlan[c],"exit"]
        print(net_connect.send_config_set(config_vlan))
    for d in list_int:
        config_int_vlan = ["int range "+ d, "switchport mode access", "switchport access vlan "+list_int[d],"exit"]
        print(net_connect.send_config_set(config_int_vlan))
        
    print("\n\tDone!!!\n")
    print(net_connect.send_command("show vlan"))

