import config_auto
options = """\n\nPHAM NGOC ANH - Netmiko in Python\n\tWelcome to VnPro!\n Hay chon chuc nang ma ban muon.\n
    1 - Xem thông tin thiết bị.
    2 - Cấu hình Interface (R).
    3 - Cấu hình Trunking (SW)
    4 - Cấu hình VLAN (SW).
    ...
    e - Exit."""

while True:
    print(options)
    option = input("Chọn chức năng: ")
    if option == '1':
        config_auto.info_device()
    elif option == '2':
        config_auto.config_int()
    elif option == '3':
        config_auto.config_tru()
    elif option == '4':
        config_auto.config_vlan()    
    elif option == 'e':
        break
    else:
        print("Nhập sai!")

