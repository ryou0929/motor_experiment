from module import *
if __name__ == '__main__':
    omega_lst = []

    try:
        setup()
        for i in range(50):
            B3M_setTor(0, -200)
            omega = B3M_readCmd(0, 'omega')
            print(omega)
            omega_lst.append(omega)
            time.sleep(0.1)
            # 
    except:
        reData = B3M_Write_CMD(0x00, 0x02, 0x28)
    reData = B3M_Write_CMD(0x00, 0x02, 0x28)
    b3m.close()
    omega_mean = sum(omega_lst)/len(omega_lst)
    print(f'{omega_mean=}')
