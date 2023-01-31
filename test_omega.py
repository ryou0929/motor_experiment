from module import *

if __name__ == '__main__':
    try:
        while 1:

            # setup()
            # B3M_setTor(0,-700)
            print(B3M_readCmd(0, 'theta'))
            time.sleep(0.1)
    except:
        reData = B3M_Write_CMD(0x00, 0x02, 0x28)
    b3m.close()
