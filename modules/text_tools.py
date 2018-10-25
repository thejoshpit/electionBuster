# Need a base alphabet for the first set of mangling functions
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"

#sometimes "y" because it makes kevin angry
vowels = "aeiouy"


alt_alphabets = [ 	'abcdefghijklmnopqrstuvwxyz1234567890',
			'abcdefgh1jklmnopqrstuvwxyz1234567890',
			'abcdefghijkimnopqrstuvwxyz1234567890',
			'abcdefghljklmnopqrstuvwxyz1234567890',
			'abcdefghijklmn0pqrstuvwxyz1234567890',
			'abcdefghijklmnopqrstuvwxyz123456789o',
			'abcdefghijklmmopqrstuvwxyz1234567890',
			'abcdefghijklnnopqrstuvwxyz1234567890',
			'abcd3fghijklmnopqrstuvwxyz1234567890',
			'Аbcdefghijklmnopqrstuvwxyz1234567890', # homographic Cyrillic А
			'аbcdefghijklmnopqrstuvwxyz1234567890', # homographic Cyrillic а
			'Ӓbcdefghijklmnopqrstuvwxyz1234567890', # homographic Cyrillic Ӓ
			'ӓbcdefghijklmnopqrstuvwxyz1234567890', # homographic Cyrillic ӓ
			'Αbcdefghijklmnopqrstuvwxyz1234567890', # homographic Greek Α
			'abcdefghijklmnОpqrstuvwxyz1234567890', # homographic Cyrillic О
			'abcdefghijklmnоpqrstuvwxyz1234567890', # homographic Cyrillic о
			'abcdefghijklmnоpqrstuvwxyz1234567890', # homographic Greek о
			'abcdefghijklmnopqrsΤuvwxyz1234567890',	# homographic Greek Τ
			'abcdefghijklmnopqrsТuvwxyz1234567890',	# homographic Cyrillic Т
			'abcdefghijklΜnopqrstuvwxyz1234567890',	# homographic Greek Μ
			'abcdefghijklМnopqrstuvwxyz1234567890',	# homographic Cyrillic М
			'abcdefghijklmnoРqrstuvwxyz1234567890',	# homographic Cyrillic Р
			'abcdefghijklmnoРqrstuvwxyz1234567890',	# homographic Cyrillic Р
			'abcdefghijklmnopqrstuvwxyz12e4567890']

tlds = ['.com', '.net', '.me' , '.org', '.net', '.biz', '.info', '.us', '.cm' ]

def removeDups(numbers):
    newlist = []
    for number in numbers:
        if number not in newlist:
            newlist.append(number)
    return newlist


# This function returns strings with each character missing
# ['oshua', 'jshua', 'johua', 'josua', 'josha', 'joshu']
def skipLetter(s):
    kwds = []

    for i in range(1, len(s) + 1):
        kwds.append(s[:i - 1] + s[i:])
    return kwds


# This function subsitutes the wrong vowell for each letter
# 'aoshua', 'boshua', 'coshua', 'doshua'
def wrongVowel(s):
    kwds = []
    for i in range(0, len(s)):
        for letter in vowels:
            if s[i] in vowels:
                for vowel in vowels:
                    s_list = list(s)
                    s_list[i] = vowel
                    kwd = "".join(s_list)
                    kwds.append(kwd)
    return kwds


# This function inserts each alphabetic character into each place in a word
# ['ajoshua', 'jjoshua', 'jooshua', 'josshua', 'joshhua', 'joshuua', 'joshuaa']
def doubleLetter(s):
    kwds = []
    for i in range(0, len(s) + 1):
        kwds.append(s[:i] + s[i - 1] + s[i:])

    return kwds


# This function inserts each alphabetic character into each place in a word
# 'jaoshua', 'jnoshua', 'josthua', 'joshuza', 'joshua2'
def insertLetter(s):
    kwds = []

    for i in range(0, len(s)):
        for char in alphabet:
            kwds.append(s[:i + 1] + char + s[i + 1:])

    return kwds


# This function reverses each letter
# ['ojshua', 'jsohua', 'johsua', 'josuha', 'joshau']
def reverseLetter(s):
    kwds = []
    for i in range(0, len(s)):
        letters = s[i - 1:i + 1:1]
        if len(letters) != 2:
            continue

        reverse_letters = letters[1] + letters[0]
        kwds.append(s[:i - 1] + reverse_letters + s[i + 1:])

    return kwds


# 'aoshua', josh9a', 'josqua', 'jzshua'
def substitution(s):
    kwds = []

    for i in range(0, len(s)):
        for letter in alphabet:
            kwd = s[:i] + letter + s[i + 1:]
            kwds.append(kwd)

    return kwds

def stringAndStrip(input):
    input = str(input)
    input = input.rstrip()
    return input
