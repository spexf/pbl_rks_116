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
