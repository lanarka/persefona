from cryptography.fernet import Fernet
key = b'0StHs9vdDCqL4EP1PC2lzs_PhODj4f2Rxx6dkn7QnFA='

fernet = Fernet(key)

fh = open('test_in.txt', 'r', encoding='iso-8859-1')
msg = fh.read()
fh.close()

arr = msg.split("\n\n")
msg = arr[1]
msg = bytes(msg, 'utf-8')

decMessage = fernet.decrypt(msg).decode()
print('DONE:', decMessage)
