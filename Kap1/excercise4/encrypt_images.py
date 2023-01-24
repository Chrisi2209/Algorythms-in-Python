import sys
import os

from secrets import token_bytes

def random_key(length: int) -> int:
    tb: bytes = token_bytes(length)
    return int.from_bytes(tb, "big")

def encrypt(data: bytes) -> tuple[bytes, bytes]:
    key: bytes = random_key(len(data))
    data_int = int.from_bytes(data, "big")

    encrypted = data_int ^ key
    
    return encrypted, key


def decrypt(encrypted: bytes, key: bytes) -> bytes:
    decrypted: int = encrypted ^ key
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, "big")

    return bytes(temp)


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        print("please input path as argument!")
        return

    if path == "del":
        if len(sys.argv) != 3:
            print("please enter path to normal png file second")
            return
        
        path = sys.argv[2]
        path_to_encrypted = os.path.splitext(path)[0] + "_encrypted" + ".bin"
        path_to_key = os.path.splitext(path)[0] + "_key" + ".bin"
        path_to_decrypted = os.path.splitext(path)[0] + "_decrypted" + ".png"
        try:
            os.remove(path_to_encrypted)
        except FileNotFoundError:
            print("no encrypted file")
        
        try:
            os.remove(path_to_key)
        except FileNotFoundError:
            print("no key file")

        try:
            os.remove(path_to_decrypted)
        except FileNotFoundError:
            print("no decrypted file")
        
        return


    # convert to absolute path
    path = os.path.abspath(path)

    # check for path existance
    if not os.path.exists(path):
        print("path not found")
        return

    if os.path.splitext(path)[1] == ".bin":
        if len(sys.argv) != 3:
            print("please enter key as second argument")
            return
        
        key_path = sys.argv[2]
        
        with open(path, "rb") as f:
            encrypted = f.read()
        
        with open(key_path, "rb") as f:
            key = f.read()
        

        decrypted = decrypt(int.from_bytes(encrypted, "big"), int.from_bytes(key, "big"))

        path_to_decrypted = os.path.splitext(path)[0][:-10] + "_decrypted" + ".png"
        with open(path_to_decrypted, "wb") as f:
            f.write(decrypted)

        print("decrypted to", path_to_decrypted)
        return


    # check for image
    if os.path.splitext(path)[1] != ".png":
        print("file has to be png or encrypted bin!")
        return
        


    

    # get image content
    with open(path, "rb") as img:
        data: bytes = img.read()

    # encrypt
    encrypted, key = encrypt(data)
    # decrypt
    decrypted = decrypt(encrypted, key)

    # success or not
    if data == decrypted:
        print("successfully encrypted")
    else:
        print("encryption failed")
        return

    path_to_encrypted = os.path.splitext(path)[0] + "_encrypted" + ".bin"
    with open(path_to_encrypted, "wb") as f:
        f.write(encrypted.to_bytes((encrypted.bit_length() + 7) // 8, "big"))

    path_to_key = os.path.splitext(path)[0] + "_key" + ".bin"
    with open(path_to_key, "wb") as f:
        f.write(key.to_bytes((key.bit_length() + 7) // 8, "big"))


    

if __name__ == "__main__":
    main()
