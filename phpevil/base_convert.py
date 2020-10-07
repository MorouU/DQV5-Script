# 没啥好说的

func="base_convert(%d,%d,%d)"
dicts=list("".join([chr(_) for _ in range(48,58)])+"".join([chr(_) for _ in range(97,123)]))

def check(s):
	global dicts
	return int(max(("|".join([str(dicts.index(_)) for _ in list(s)])).split("|")))+1
	

if __name__ == '__main__':
	frombase=10
	# tobase= [转换的底数]
	
	while True:
		try:
			s=input("Input string:")
			tobase=check(s)
			print(func%(int(s,tobase),frombase,tobase))
		except KeyboardInterrupt:
			break
		except Exception:
			print('error!')
			continue
