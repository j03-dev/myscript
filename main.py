import sys

from myscript.exploit import Exploit, text_asci

__author__ = "Nomeniavo Joe"
__version__ = 1.0


def main():
    print(text_asci)
    run = True
    while run:
        try:
            input_ = input("\nexploit >> ").split()
            if input_:
                if input_[0] in Exploit.command:
                    result = getattr(globals()['Exploit'](), input_[0])(input_)
        except KeyboardInterrupt:
            sys.exit(1)


if __name__ == "__main__":
    main()
