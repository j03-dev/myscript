from myscript.exploit import Exploit, art_asci
import sys


def main():
	art_asci()
	run = True
	while run:
		try:
			input_ = input("\nexploit >> ").split()
			if input_:
				if input_[0] in Exploit.command:
					result = getattr(globals()['Exploit'](), input_[0])(input_)
		except KeyboardInterrupt:
			sys.exit(1)

main()
