from string import ascii_uppercase as upper

class Caesar:

    def encrypt(self,plain,key):
        cipher = ''
        key = int(key)
        for i in str(plain.upper()):
            if i not in str(upper):
                cipher += i
            else:
                cipher += upper[(int(upper.find(i)) + key) % 26]
        return cipher

    def decrypt(self,cipher,key):
        plain = ''
        key = int(key)
        for i in str(cipher.upper()):
            if i not in str(upper):
                plain += i
            else:
                plain += upper[(int(upper.find(i)) - key) % 26]
        return plain


class Vigenere:
    def generate_vigenere_table(self):
        table = []
        for i in range(26):
            table.append([chr(((j + i) % 26) + 65) for j in range(26)])
        return table

    def encrypt(self,plain_text, key):
        plain_text = plain_text.upper().replace(" ", "")
        key = key.upper()
        vigenere_table = self.generate_vigenere_table()
        key_repeated = (key * (len(plain_text) // len(key))) + key[:len(plain_text) % len(key)]
        cipher_text = ''
        for i in range(len(plain_text)):
            row = ord(key_repeated[i]) - 65
            col = ord(plain_text[i]) - 65
            cipher_text += vigenere_table[row][col]
        return cipher_text

    def decrypt(self,cipher_text, key):
        cipher_text = cipher_text.upper().replace(" ", "")
        key = key.upper()
        vigenere_table = self.generate_vigenere_table()
        key_repeated = (key * (len(cipher_text) // len(key))) + key[:len(cipher_text) % len(key)]
        plain_text = ''
        for i in range(len(cipher_text)):
            row = ord(key_repeated[i]) - 65
            col = vigenere_table[row].index(cipher_text[i])
            plain_text += chr(col + 65)
        return plain_text
