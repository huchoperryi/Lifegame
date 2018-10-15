import numpy as np
from PIL import Image

lifegame_object = {
	'Glider':
	['010',
	 '001',
	 '111'],
	'Acorn':
	['0100000',
	 '0001000',
	 '1100111'],
	'Diehard':
	['0000000100',
	 '0110000000',
	 '0010001110'],
	'Rpentomino':
	['011',
	 '110',
	 '010'],
	'Glidergun':
	['00000000000000000000000000000000000000',
	 '00000000000000000000000001000000000000',
	 '00000000000000000000000101000000000000',
	 '00000000000001100000011000000000000110',
	 '00000000000010001000011000000000000110',
	 '01100000000100000100011000000000000000',
	 '01100000000100010110000101000000000000',
	 '00000000000100000100000001000000000000',
	 '00000000000010001000000000000000000000',
	 '00000000000001100000000000000000000000',
	 '00000000000000000000000000000000000000'],
	'BlankBox':
	['1001001001',
	 '0000000000',
	 '0000000000',
	 '1000000001',
	 '0000000000',
	 '0000000000',
	 '1000000001',
	 '0000000000',
	 '0000000000',
	 '1001001001'],
	'Galaxy':
	['111111011',
	 '111111011',
	 '000000011',
	 '110000011',
	 '110000011',
	 '110000011',
	 '110000000',
	 '110111111',
	 '110111111'],
	'LightWeightSpaceship':
	['01001',
	 '10000',
	 '10001',
	 '11110'],
	'MiddleWeightSpaceship':
	['000100',
	 '010001',
	 '100000',
	 '100001',
	 '111110']
}

Glider = \
	['010',
	 '001',
	 '111']

Acorn = \
	['0100000',
	 '0001000',
	 '1100111']

DieHard = \
	['0000000100',
	 '0110000000',
	 '0010001110']

Rpentomino = \
	['011',
	 '110',
	 '010']

Glidergun = \
	['00000000000000000000000000000000000000',
	 '00000000000000000000000001000000000000',
	 '00000000000000000000000101000000000000',
	 '00000000000001100000011000000000000110',
	 '00000000000010001000011000000000000110',
	 '01100000000100000100011000000000000000',
	 '01100000000100010110000101000000000000',
	 '00000000000100000100000001000000000000',
	 '00000000000010001000000000000000000000',
	 '00000000000001100000000000000000000000',
	 '00000000000000000000000000000000000000']
	 
def data2bool(s, rotate=0, mirror=''):
	
	height = len(s)
	width = len(s[0])
	bool_s = np.zeros((height, width),dtype=bool)
	
	for h in range(height):
		if len(s[h]) != width:
			print('List shape error')
			bool_s = ''
			break
			
		for w in range(width):
			if s[h][w] == '1':
				bool_s[h][w] = True
			else:
				bool_s[h][w] = False
				
	
	if rotate == 0:
		pass		
	elif rotate == 90:
		bool_s = bool_s.T[::-1]
	elif rotate ==180:
		bool_s = bool_s[::-1, ::-1]
	elif rotate == 270:
		bool_s = bool_s.T[:, ::-1]
	else:
		print('rotate parameter error')
		bool_s = []
		
	if mirror == '':
		pass
	elif mirror == 'h':
		bool_s = bool_s[:, ::-1]
	elif mirror == 'v':
		bool_s = bool_s[::-1]
		
	return bool_s
	
def show_data(booldata):
	
		pil_image = Image.fromarray((1 - booldata.astype(dtype=np.uint8)) * 255)
		
		pil_image = pil_image.resize((pil_image.size[0] * 2, pil_image.size[1] * 2))
		pil_image.show()
		
if __name__ == '__main__': 
	data = lifegame_object['Glidergun']
	
	#print(data)
	data_bool = data2bool(data)
	'''
	print(data_bool)
	show_data(data_bool)
	data_bool = data2bool(data, rotate=90)
	show_data(data_bool)
	data_bool = data2bool(data, rotate=180)
	show_data(data_bool)
	data_bool = data2bool(data, rotate=180, mirror='h')
	show_data(data_bool)
	'''
	#print(data_bool)
	pil_image = Image.fromarray((1-np.uint8(data_bool))*255, mode='L')
	pil_image.convert('1').show()
	#pilimgfile = io.BytesIO()
	pil_image.convert('1').save('./test.png', format='png')
	#data_bool = data2bool(data, rotate=5)
	#show_data(data_bool)
