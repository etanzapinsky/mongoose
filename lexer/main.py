from lexer import lexer
import sys

if __name__ == "__main__":
    #while True:
    data = open(sys.argv[1], 'r')#raw_input(">>   ")
    lexer.test(data.read())
