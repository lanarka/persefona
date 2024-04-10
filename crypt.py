from cryptography.fernet import Fernet
key = b'0StHs9vdDCqL4EP1PC2lzs_PhODj4f2Rxx6dkn7QnFA='

message = "Hello Geeks! This is my secret message."

fernet = Fernet(key)
msg = fernet.encrypt(message.encode())
x=msg.decode()

print('0123456789001234567890\n\n')
print(x)
print('\n\n0123456')
