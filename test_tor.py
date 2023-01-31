# import a
from module import *
if __name__ == '__main__':

    setup()
    B3M_setTor(0, -200)
    time.sleep(5)
    reData = B3M_Write_CMD(0x00, 0x02, 0x28)
    b3m.close()