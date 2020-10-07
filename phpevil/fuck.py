from random import shuffle


def php_change(str, add=True):
	other = list(" !\"#$%&'()*+,-./:;<=>?[\]^_@`{|}~")
	str1 = ""
	str2 = ""
	for each in str:
		shuffle(other)
		find = False
		for _0 in other:
			if (find):
				break
			for _1 in other:
				if (bin(ord(_0) ^ ord(_1))[2:] == bin(ord(each))[2:]):
					if (add):
						if (_0 == '\'' or _0 == '\"' or _0 == '\\'): str1+='\\'
						if (_1 == '\'' or _1 == '\"' or _1 == '\\'): str2+='\\'
					str1 += _0
					str2 += _1
					find = True
					break
		if (not find):
			str1 += each
			str2 += chr(0)

	result = "(\'" + str1 + "\'^\'" + str2 + "\')"

	print(result)
	return result


if __name__ == '__main__':
	while True:
		php_change(str(input("Input:")))
