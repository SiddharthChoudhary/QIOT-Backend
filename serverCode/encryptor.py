from Crypto.Cipher import AES
import os
import csv
# import pandas as pd
# from pandas import DataFrame as df

KEY_COUNT =43

class encryptor(object):
    def __init__(self):
        # self.keys = pd.read_csv('keys_binary.csv', names=['refid', 'keys'], index_col=0, dtype={1:'str'})
        self.IV = b'EncryptionOf16By'
        
    def concat_keys(self, sample_keys):
        # key=''
        # for row in sample_keys.iterrows():
        #     key += row[1]
        # return self.bitstring_to_bytes(key[0][:128])
        pass
    
    def bitstring_to_bytes(self, s):
        return int(s, 2).to_bytes((len(s)+7) // 8, byteorder='big')
    
    def get_random_key(self):
        '''get a random set of keys from the key pool'''
        # sample_keys = self.keys.sample(KEY_COUNT)
        # refid = sample_keys.index.values.tolist()
        # key = self.concat_keys(sample_keys)
        # return refid, key
        pass
    
    def readCSVfile(self,startPosition):
        with open('keys_binary.csv') as csvfile:
            readCSVfile = csv.reader(csvfile, delimiter=',')
            temporaryIndex = 0
            temporaryString = ''
            for row in readCSVfile:
                if(temporaryIndex >= startPosition and temporaryIndex-startPosition >= 0 and temporaryIndex-startPosition < 43):
                    temporaryString = temporaryString+row[1]
                temporaryIndex+=1
                # print(row[0])
                # print(row[1])
            key = temporaryString[0:128]
        return self.bitstring_to_bytes(key)

    def find_key(self, refid):
        # sample_refid = df(refid, columns=['id'])
        # sample_key = pd.merge(sample_refid, self.keys, left_on='id', right_on='refid', how='inner')
        # sample_key = sample_key.set_index('id')
        # key = self.concat_keys(sample_key)
        # return key
        pass
    
    def encrypt_file(self,startPosition,filename):
        chunk_size = 64*1024
        output_file = filename+".enc"
        key = self.readCSVfile(startPosition)
        IV = b'EncryptionOf16By'
        file_size = str(os.path.getsize(filename)).zfill(16)
        encryptor = AES.new(key, AES.MODE_CBC, IV)
        with open(filename, 'rb') as inputfile:
            with open(output_file, 'wb') as outf:
                outf.write((file_size.encode('utf-8')))
                outf.write(IV)
                while True:
                    chunk = inputfile.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' '.encode('utf-8')*(16 - len(chunk)%16)
                    outf.write(encryptor.encrypt(chunk))

    def decrypt_file(self,startPosition,filename):
        chunk_size = 64*1024
        output_file = "decrypted_"+filename[:-4]
        key = self.readCSVfile(startPosition)
        with open(filename, 'rb') as inf:
            filesize = int(inf.read(16))
            IV = inf.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, IV)
            with open(output_file, 'wb') as outf:
                while True:
                    chunk = inf.read(chunk_size)
                    if len(chunk)==0:
                        break
                    outf.write(decryptor.decrypt(chunk))
                outf.truncate(filesize)
    

    def encrypt_data(self, name, startPosition):
        #to extract the name before .jpg
        name = name.split('.jpg')[0]
        key  = self.readCSVfile(startPosition)
        encryptor = AES.new(key, AES.MODE_CBC, self.IV)
        name = name.rjust(16, " ")
        return encryptor.encrypt(name)   

    def decrypt_data(self, enc_data, startPosition):
        print('The data is ', enc_data)
        key  = self.readCSVfile(startPosition)
        decryptor = AES.new(key, AES.MODE_CBC, self.IV)
        data = decryptor.decrypt(enc_data)
        return data.strip()
