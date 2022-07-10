def generate_public_key(P, G, A_private_key):
	try:
		public_key = int(pow(int(G), int(A_private_key), int(P)))
		return public_key
	except:
		return ''

def generate_key(P, A_private_key, B_public_key):	
	try:
		key = int(pow(int(B_public_key), int(A_private_key), int(P)))
		return key
	except:
		return ''
     