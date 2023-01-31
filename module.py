import serial
import time
import datetime


b3m = serial.Serial('COM4', baudrate=115200,
                    parity=serial.PARITY_NONE, timeout=0.5)


def log(log_dir, *data):
    with open(log_dir, "a") as f:
        for i in range(len(data)):
            if isinstance(data[i], list):
                for j in range(len(data[i])):
                    f.write(str(data[i][j]) + "\t")
            else:
                f.write(str(data[i]))
        f.write('\n')


def setup():
    # b3m = serial.Serial('COM6', baudrate=9600,parity=serial.PARITY_NONE, timeout=2)
    ###毎回これやる################################
    reData = B3M_Write_CMD(0x00, 0x02, 0x28)
    time.sleep(0.5)
    #位置制御モードに設定 (角度を指定して動作するモードです)
    reData = B3M_Write_CMD(0x00, 0x0A, 0x28)
    time.sleep(0.5)
    # 軌道生成タイプ：Even (直線補間タイプの位置制御を指定)
    reData = B3M_Write_CMD(0x00, 0x01, 0x29)
    time.sleep(0.5)
    # ゲインプリセット：No.0 (PIDのプリセットゲインを位置制御モード用に設定)
    reData = B3M_Write_CMD(0x00, 0x02, 0x5C)
    time.sleep(0.5)
    # 動作モード：Normal （Freeの状態からトルクオン）
    reData = B3M_Write_CMD(0x00, 0x08, 0x28)
    time.sleep(0.5)
    ################################################
    # print('セットアップ完了')


def B3M_Write_CMD(servo_id, TxData, Address):
    # 送信コマンドを作成
    txCmd = [0x08,  # SIZE
             0x04,  # CMD
             0x00,  # OPTION
             servo_id,  # ID
             TxData,  # DATA
             Address,  # ADDRRESS
             0x01]  # COUNT

    # チェックサムを用意
    checksum = 0
    for i in txCmd:
        checksum += i

    # リストの最後にチェックサムを挿入する
    txCmd.append(checksum & 0xff)

    # WRITEコマンドを送信
    b3m.write(txCmd)

    # サーボからの返事を受け取る
    rxCmd = b3m.read(5)

    # もしリスト何になにも入っていなかったら正常に受信できていないと判断
    if len(rxCmd) == 0:
        return False

    # 問題なければ返事を返す
    return True


def B3M_setPos(servo_id, pos, time):

    # 送信コマンドを作成
    txCmd = [0x09,  # SIZE
             0x06,  # CMD
             0x00,  # OPTION
             servo_id,  # ID
             pos & 0xff,  # DATA
             pos >> 8 & 0xff,
             time & 0xff,
             time >> 8 & 0xff]

    # チェックサムを用意
    checksum = 0
    for i in txCmd:
        checksum += i

    # リストの最後にチェックサムを挿入する
    txCmd.append(checksum & 0xff)

    # WRITEコマンドを送信
    b3m.write(txCmd)

    # サーボからの返事を受け取る
    rxCmd = b3m.read(7)
    print(rxCmd[5] << 8 | rxCmd[6])
    # もしリスト何になにも入っていなかったら正常に受信できていないと判断
    if len(rxCmd) == 0:
        return False

    # 問題なければ返事を返す
    return True


def B3M_setTor(servo_id, Tor):
    # 送信コマンドを作成
    txCmd = [0x09,  # SIZE
             0x04,  # CMD
             0x00,  # OPTION
             servo_id,  # ID
             Tor & 0xFF,  # DATA
             Tor >> 8 & 0xFF,
             0x3C,
             0x01]

    # チェックサムを用意
    checksum = 0
    for i in txCmd:
        checksum += i

    # リストの最後にチェックサムを挿入する
    txCmd.append(checksum & 0xff)

    # WRITEコマンドを送信
    b3m.write(txCmd)
    time.sleep(0.1)

    # サーボからの返事を受け取る
    rxCmd = b3m.read(5)
    # もしリスト何になにも入っていなかったら正常に受信できていないと判断
    if len(rxCmd) == 0:
        print("fuck")
        return False

    # 問題なければ返事を返す
    return True


def B3M_readCmd(servo_id, str):
    """theta,omega"""
    # 送信コマンドを作成
    Address = 0
    length = 2
    if str == "theta":
        Address = 0x2C
        length = 2

    elif str == "omega":
        Address = 0x32
        length = 2

    txCmd = [0x07,  # SIZE
             0x03,  # CMD
             0x00,  # OPTION
             servo_id,  # ID
             Address,  # DATA
             length]

    # チェックサムを用意
    checksum = 0
    for i in txCmd:
        checksum += i

    # リストの最後にチェックサムを挿入する
    txCmd.append(checksum & 0xff)

    # WRITEコマンドを送信
    b3m.write(txCmd)

    rxCmd = b3m.read(7)
    Value = [rxCmd[4], rxCmd[5]]

    # データの範囲にマイナスが含まれる場合
    if (Address == 0x05  # 最小位置制御
        or Address == 0x07  # 最大位置制御
        or Address == 0x09  # 中央値オフセット
        or Address == 0x0B  # MCU温度リミット
        or Address == 0x0E  # モーター温度リミット
        or Address == 0x2A  # 目標位置
        or Address == 0x2C  # 現在位置
        or Address == 0x2E  # 前回のサンプリングの位置
        or Address == 0x30  # 目標速度
        or Address == 0x32  # 現在速度
        or Address == 0x34  # 前回のサンプリングの速度
        or Address == 0x3C  # 目標トルク
        or Address == 0x44  # 現在のMCU温度
            or Address == 0x46):  # 現在のモーター温度

        kazu = int.from_bytes(Value, 'little', signed=True)

    # データの範囲がプラスのみの場合
    else:
        kazu = int.from_bytes(Value, 'little')

    # サーボからの返事を受け取る
    # rxCmd = b3m.read(7)
    # if rxCmd[5] >= 2**7:
    #     rx_5 = rxCmd[5] -pow(2,7)
    #     kazu = rx_5 << 8 | rxCmd[4]
    #     kazu *= -1
    # else:
    #     kazu = rxCmd[5] << 8 | rxCmd[4]

    # もしリスト何になにも入っていなかったら正常に受信できていないと判断
    if len(rxCmd) == 0:
        print("fuck")
        return False

    if str == "theta":
        theta = kazu / 100
        if(180 < theta):
            theta -= 360
        elif theta < -180:
            theta += 360
        return theta
    elif str == "omega":
        return kazu/100


if __name__ == '__main__':
    # COMポートを開くco
    servo_id = 0
    b3m = serial.Serial('COM5', baudrate=115200,
                        parity=serial.PARITY_NONE, timeout=0.5)
    # B3Mサーボが動作するまでの準備
    # 動作モード：Free (動作モードと特性を設定するため、設定書き換え中の誤動作を防止するため脱力にしておく)
    reData = B3M_Write_CMD(0x00, 0x02, 0x28)

    #位置制御モードに設定 (角度を指定して動作するモードです)
    reData = B3M_Write_CMD(0x00, 0x02, 0x28)

    # 軌道生成タイプ：Even (直線補間タイプの位置制御を指定)
    reData = B3M_Write_CMD(0x00, 0x01, 0x29)

    # ゲインプリセット：No.0 (PIDのプリセットゲインを位置制御モード用に設定)
    reData = B3M_Write_CMD(0x00, 0x00, 0x5C)

    # 動作モード：Normal （Freeの状態からトルクオン）
    reData = B3M_Write_CMD(0x00, 0x00, 0x28)
    # WRITEコマンド
    # メモリーマップ(RAM)のアドレス指定でデバイスのRAM上に書き込みます。

    # #b3mを終了
    b3m.close()
