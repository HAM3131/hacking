with open('DownUnderCTF/rev/theAllFathersWisdom/the-all-fathers-wisdom', 'rb') as file:
    binary = file.read()

print(len(binary))
for i in range(10):
    print(binary[i*100:(i+1)*100])

if binary.find(b'DUCTF')!=-1:
    print(binary.find(b'DUCTF')!=-1)
else:
    print("Not found :(")