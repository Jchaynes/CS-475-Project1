import textwrap
import collections
import string

inputFiles  = [   'ciphertext_3' , #not shift, frequencies between ~2-4,3,5,8, vigenere? MUST BE STREAM
                #   'ciphertext_8' , #decrypted, not shift, normal frequency, vigenere, key "APP"
                #   'ciphertext_13', #decrypted, shift 14
                #   'ciphertext_18', #decrypted, not shift normal frequency, permutation, 10x4 grid
                #   'ciphertext_23', #Decrypted, transform 8x3 grid #not shift, normal freqeuency
                #   'ciphertext_28'  #decrypted, not shift, frequencies between ~2-4, ~5-7, probably key length 8,vigenere, key found
                 ]


cipherTexts = []

#Frequent Characters from wikipedia

englishLetterFrequencies = { 'A' : 8.20, 'B':1.50, 'C':2.80,'D':4.30,
                            'E':13.00,'F':2.20,'G':2.00,'H':6.10,
                            'I':7.00,'J':0.15,'K':0.77,'L':4.00,
                            'M':2.40,'N':6.70,'O':7.50,'P':1.90,
                            'Q':0.095,'R':6.00,'S':6.30,'T':9.10,
                            'U':2.80,'V':0.98,'W':2.40,'X':0.15,
                            'Y':2.00,'Z':0.074}

searchWords = ['THE','AND','CAPTIAN','FINS','SHIP','ATTACK','PLANE','SHARK']


def charCount(text):
    chars = dict.fromkeys(string.ascii_uppercase,0)
    for c in text:
            chars[c] += 1
    length = len(text)
    if(length > 0):
        for char in chars:
            frequency = chars[char]/length * 100
            chars[char] = round(frequency,2)
    return chars

def shiftCipher(text,shift):
    shiftedText = ''
    for c in text:
        shiftedChar = chr(shiftChar(c,shift))
        shiftedText += shiftedChar

    # for word in searchWords:
    #     if shiftedText.find(word) > 0:
    #         print("Possible Caesar Shift found %s. Shift: %d " % (word, shift))
    #         print(shiftedText.lower())
    #         return
    return shiftedText

def shiftChar(c,shift):
    return (ord(c) - 65 - shift) % 26 + 65

def testStream(text,shift=0):
    prevChar = text[0] 
    # prevChar = chr(shiftChar(prevChar, shift))
    charValues = [prevChar]
    charValue = 0
    # print(text[:10])
    #for stream cipher, we will assume first letter is unencrypted, each subsequent letter is shifted by the an amount including the previous letter ciphertext value.
    for c in text[1:20]:
        # normalizeShift = (ord(prevChar) - ord('A') + shift) % 26
        # normalizeShift = ord(prevChar) - 65
        # normalizeShift = shiftChar(c, ord(prevChar) - 65)
        # if normalizeShift < 0:
        #     normalizeShift *= -1
        #     normalizeShift %= 26
        # print("Shifting letter by normalized shift of ", normalizeShift - 65)
        # charValue = shiftChar(c, normalizeShift)
        # char = chr(charValue) 
       # print("charValue is %d")
        # charValues.append(char)
        diff = (ord(c) - ord(prevChar) - shift) % 26
        if diff < 0:
            diff += 26
        #print("Old Letter might have been : ", chr(diff+65))
        char = chr(diff + 65)
        charValues.append(char) 
        # print("Current Step: %c, %c, %d" % (prevChar, c, diff))
        prevChar = c
    #print(''.join(charValues))
    # print(charCount(''.join(charValues)))
    return ''.join(charValues)

def plaintextShiftStream(text, shift=0):
    #Unshift each nth character in sequence by the unshifted n-1 character plaintext value.
    normalizeShift = (ord(text[0]) - shift - 65) % 26 + ord('A')
    prevChar = chr(normalizeShift)
    charValues = [prevChar]
    for c in text[1:]:
        diff = ord(c) - ord(prevChar)
        
        if diff < 0:
            diff += 26
        char = chr(diff + 65)
        charValues.append(char)
       # print("PrevChar: %c\tdiff:  %d\tchar: %c" % (prevChar, diff, c))
        prevChar = char
    return ''.join(charValues)

def vigenereKeyLengthTest(text):
    shift = 1
    length = len(text)
    coincidences = {}
    while(shift < length):
        count = 0
        for i in range(0, length):
            if i + shift < length-1:
                #if text[i:i+2] == text[i + shift:i+shift+2]:
                if text[i] == text[i + shift]:
                    count += 1
        coincidences[shift]= count
        shift += 1
        
    outString = ""
    for c in coincidences:
        outString+= ' ' + str(coincidences[c]) + ','
        if c % 5 == 0:
            outString += '\n'
    print(outString)

def vigenereBinLetters(text,keyLength):
    #After testing for key length, bin letters together to look at frequencies.
    length = len(text)
    charBins = collections.defaultdict(list)
    binTotals = [0] * keyLength

    for i in range(0, length):
        binTotals[i%keyLength] += 1 
        charBins[i % keyLength].append(text[i])
    print("English Frequencies: \n", englishLetterFrequencies)
    print("")
    for i in range(0, keyLength):
        print(charCount(charBins[i]))
        
def gramSearch(text, wordSize):
    grams = {}
    for c in range(len(text)-wordSize):
        searchWord = text[c:c+wordSize]
        if searchWord not in grams:
            grams[searchWord] = 1
        else:
            #print("Found word grouping of %d:%s" % (wordSize, searchWord))
            grams[searchWord] += 1
    dupGrams = []
    for word in grams:
        if grams[word] > 1:
            dupGrams.append(word)
    for word in dupGrams:
        index = 0
        while index < len(text):
            #print("%s:%d" % (word, grams[word]))
            index = text.find(word,index)
            if(index == -1):
                break
            print("Index of repeat  %s in ciphertext: %d" % ( word, index))
            
            index += 1
        #break
        
def charToAlphaPos(letter):
    return ord(letter) - 65 % 26 

def vigenereDecrypt(text,key):
    keyIndex = 0
    decryptedText = ""
    for c in text:
        decryptedText += chr(shiftChar(c,charToAlphaPos(key[keyIndex % len(key)])))
        keyIndex += 1
    return decryptedText

def untransform(text,numRows, numColumns):

    groups = []
    index = 0
    groupLength = numRows * numColumns
    # numGroups = len(text) / groupLength
    #take every nth character in groupings of the number of columns apart for number of columns * number of rows characters, until end of text
    #reassemble groupings from each step in sequence to get text back out.
    resultText = ""
    #while len(resultText) < len(text):
        
       
       # for c in text[index:index+groupLength]:
    for block in range(0, len(text),groupLength):
        #print(block)
        groups.append(text[block:block+groupLength])

         #   resultText += c #resultText.join(c)
         #   print(resultText)
    #print(groups)
    for group in groups:
        decipheredBlockText = ""
        # print("Processing group: " , group)
        index = 0
        #Case for last group being shorter than groupLength, avoids index out of bounds
        if(len(group) < groupLength):
            # while(len(decipheredBlockText) < len(group)):
            #     if(index >= len(group)):
            #         index = index % len(group) + 1
            #         decipheredBlockText += group[index]
            #         index += numRows
            decipheredBlockText = group
        else: 
            while(len(decipheredBlockText) < groupLength):
                if(index >= groupLength):
                    index = index % groupLength + 1
                decipheredBlockText += group[index]
                index += numRows
    #         while index < groupLength:
    #             resultText += group[index]
    
            #print(decipheredBlockText)
        resultText += decipheredBlockText
        #print(decipheredBlockText)
    #print("Result of untransform: " , resultText)
    return resultText        
    
def verifyEnglish(text, mode):
    foundWords = 0
    for word in searchWords:
        if text.find(word) > 0:
            foundWords += 1
    if(foundWords >= 3):
        print("Possible decryption found. %s. " % (mode))
        print(text.lower())


def main():
    for inFile in inputFiles:
        print(inFile)
        f = open(inFile, 'r')
        line = f.readline().strip('\n')
        f.close()
        cipherTexts.append(line)
        
        plainshiftBrute = "BVFWQWFU"
        # streamdecrypt = testStream(line,0)
        for i in range(0,26):
            # print(shiftCipher(streamdecrypt,i))
            # print(plaintextShiftStream(line,i))
            # resultText = plaintextShiftStream(line,i)
            resultText = testStream(line,i)
            print(resultText)
            
            for i in range(0,26):
                verifyEnglish(shiftCipher(resultText,i),"Stream")
                # print(shiftCipher(resultText,i))
        # print(line)
        # print(charCount(line))

        #Test strings for possible stream encryption Algorithm - both plaintext are "BULLFROG"
        # streambrute = "BVGRWNBH"
        # print(plaintextShiftStream(plainshiftBrute, 0))
        # print(testStream(streambrute,0))
        
        #TEST STRING FOR untransform Algorithm "THEQUICKBROWNFOXJUMPEDOVERTHELAZYDOG, in a 4x3 box permutation"
        
        #untransform("TQCRHUKOEIBWNXMDFJPOOUEVEHADREZOTLYG",4,3)
     
        #Any transform less than 2 x 2 is trivial to decrypt, assume at least 2 x 2
        # i = 1
        # LIMIT = 15
        # while i <= LIMIT:
        #     for j in range(2,16):
        #         result = untransform(line,i,j)
        #         verifyEnglish(result, "transform %d %d" %(i,j))
        #     i += 1
     

        #CiperText 3 Settings#Must be the stream cipher
        # print(charCount(line))
        # # streamNormalizedText = testStream(line,0)
        # streamResult = testStream(line)
        # for shift in range(1,26):
        #     streamshiftTest = shiftCipher(streamResult,shift)
        #     #print(streamshiftTest)
        #     # print(charCount(streamshiftTest))
        #     verifyEnglish(streamshiftTest,"stream shift")
        # gramSearch(line[:1000],5)

        #END CIPHERTEXT 3 SETTINGS#

        
        #CipherText 8 Settings

        #gramSearch(line[:1000],3)
        #vigenereKeyLengthTest(line)
        #vigenereBinLetters(line,3)
        #decrypted_8Text = vigenereDecrypt(line,"APP")
        #print(decrypted_8Text.lower())

        #END CIPHERTEXT 8#


        #CipherText 13 Settings
        
        # for shift in range(1,26):
        #     decryptedText = shiftCipher(line,shift)
        #     verifyEnglish(decryptedText,"Shift %d" %(shift))
        
        #END CIPHERTEXT 13#

        #CIPHERTEXT 18 SETTINGS

        #untransformed_18 = untransform(line,10,4)
        #print(untransformed_18.lower())
        
        #END CIPHERTEXT 18

        #CIPHERTEXT 23 Settings

        # decrypted23Text = untransform(line,8,3)
        # print(decrypted23Text.lower())

        #END CIPHERTEXT23

        #CipherText 28 Settings
        
        #gramSearch(line[:1000],3)
        #vigenereBinLetters(line,8)
        #decrypted-28Text = (vigenereDecrypt(line, "UFYUVSFE"))
        #print("Decrypted Frequencies: ")
        #print(decrypted-28Text)

main()
