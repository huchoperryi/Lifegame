import numpy as np
import console
from scene import *
from PIL import Image
import ui, io
from time import sleep

import LifegameObject

class LifegameField():


	def __init__(self, w, h):

		self.width = w
		self.height = h
		self.field = np.zeros((self.height, self.width), dtype=bool)
		self.gen = 0

	def update(self):

		self.newcells = np.zeros((self.height, self.width),dtype=int)

		self.judgeCells2 = np.ones((self.height, self.width), dtype=int) * 2

		self.judgeCells3 = np.ones((self.height, self.width), dtype=int) * 3

		self.workCellsXpls = np.roll(self.field, 1, axis=1).astype(dtype=int)
		self.workCellsXmns = np.roll(self.field, -1, axis=1).astype(dtype=int)
		self.workCellsYpls = np.roll(self.field, 1, axis=0).astype(dtype=int)
		self.workCellsYmns = np.roll(self.field, -1, axis=0).astype(dtype=int)
		self.workCellsXplsYpls = np.roll(self.workCellsXpls, -1, axis=0)
		self.workCellsXplsYmns = np.roll(self.workCellsXpls, 1, axis=0)
		self.workCellsXmnsYpls = np.roll(self.workCellsXmns, -1, axis=0)
		self.workCellsXmnsYmns = np.roll(self.workCellsXmns, 1, axis=0)

		self.sumCells = \
			self.workCellsXmns + \
			self.workCellsXpls + \
			self.workCellsYmns + \
			self.workCellsYpls + \
			self.workCellsXmnsYmns + \
			self.workCellsXmnsYpls + \
			self.workCellsXplsYmns + \
			self.workCellsXplsYpls

		self.judgeResult2 = np.equal(self.sumCells, self.judgeCells2)

		self.judgeResult3 = np.equal(self.sumCells, self.judgeCells3)

		self.judgeResult2int = self.judgeResult2.astype(dtype=int)

		self.surviveCell = np.logical_and(self.judgeResult2, self.field)

		self.surviveCellint = self.surviveCell.astype(dtype=int)

		self.newcells = np.logical_or(self.judgeResult3, self.surviveCell)

		self.gen = self.gen + 1
		return self.newcells

	def show(self):

		for i in range(self.height):
			for j in range(self.width):
				if self.field[i][j] == True:
					print('*', end='')
				else:
					print('-', end='')
			print('')
		print('')


	def fieldImg(self):

		self.img = Image.fromarray((1 - self.field.astype(dtype=np.uint8)) * 255)

		return self.img

	def mySetObject(self, orgX, orgY, object):
		lenX = len(object[0])
		lenY = len(object)
		orgY = self.height - orgY

		for j in range(lenY):
			for i in range(lenX):
				self.field[orgY - lenY + j][orgX + i] = \
					object[j][i]


	def myGlider(self):

		return ((0,1,0),
						(0,0,1),
						(1,1,1))

	def myAcorn(self):

		return ((0, 1, 0, 0, 0, 0, 0),
						(0, 0, 0, 1, 0, 0, 0),
						(1, 1, 0, 0, 1, 1, 1))

	def myDieHard(self):

		return ((0, 0, 0, 0, 0, 0, 0, 1, 0, 0),
						(0, 1, 1, 0, 0, 0, 0, 0, 0, 0),
						(0, 0, 1, 0, 0, 0, 1, 1, 1, 0))

	def myRpentomino(self):

		return ((0, 1, 1),
						(1, 1, 0),
						(0, 1, 0))

	def myGridergun(self):
		return(
		(0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0),
		(0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,1,0,0,0,0, 0,0,0,0,0,0,0,0),
		(0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,1,0,1,0,0,0,0, 0,0,0,0,0,0,0,0),
		(0,0,0,0,0,0,0,0,0,0, 0,0,0,1,1,0,0,0,0,0, 0,1,1,0,0,0,0,0,0,0, 0,0,0,0,0,1,1,0),
		(0,0,0,0,0,0,0,0,0,0, 0,0,1,0,0,0,1,0,0,0, 0,1,1,0,0,0,0,0,0,0, 0,0,0,0,0,1,1,0),
		(0,1,1,0,0,0,0,0,0,0, 0,1,0,0,0,0,0,1,0,0, 0,1,1,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0),
		(0,1,1,0,0,0,0,0,0,0, 0,1,0,0,0,1,0,1,1,0, 0,0,0,1,0,1,0,0,0,0, 0,0,0,0,0,0,0,0),
		(0,0,0,0,0,0,0,0,0,0, 0,1,0,0,0,0,0,1,0,0, 0,0,0,0,0,1,0,0,0,0, 0,0,0,0,0,0,0,0),
		(0,0,0,0,0,0,0,0,0,0, 0,0,1,0,0,0,1,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0),
		(0,0,0,0,0,0,0,0,0,0, 0,0,0,1,1,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0),
		(0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0))

class BaseButton(SpriteNode):
	
	
	
	def __init__(self, intId, bgcolor, strSymbol):
		
		width = 45
		height = 50
		r = 5
		margin = 1
		
		self.bak = ShapeNode(\
			path = ui.Path.rounded_rect(\
				0,0,
				width - margin, height,
				r),
			color=bgcolor,
			anchor_point=(0,0),
			position=(intId * width, 0),
			parent=self)
			
		self.Symbol = SpriteNode(
			strSymbol,
			anchor_point=(0.5,0.5),
			position=(intId * width + (width - margin) / 2,height /2),
			z_position=1.0,
			parent=self)

class PartsFloat(SpriteNode):
	
	def __init__(self, data_object, **kwargs):
		
		#set parameter
		self.mirror = ''
		self.data_object = data_object
		self.degree= 0
		
		#draw object
		self.blAddObject = LifegameObject.data2bool(data_object).astype(dtype=np.uint8)
		part_img = Image.fromarray((1 - self.blAddObject) * 128 + 63)
		pilimgfile = io.BytesIO()
		part_img.save(pilimgfile, format='png')
		bytes_img = pilimgfile.getvalue()
		uiimg = ui.Image.from_data(bytes_img)
		texture = Texture(uiimg)
		SpriteNode.__init__(self,
			texture,
			position=(100,100),
			anchor_point=(0,0),
			z_position=1,
			**kwargs)
		self.margin = self.size * 0.4
	
	def reverse_h(self, **kwargs):
		
		position = self.position
		
		self.remove_from_parent()
		
		if self.mirror == '':
			self.mirror = 'h'
			
		elif self.mirror == 'h':
			self.mirror = ''
			
		else:
			print('mirror parameter error ', self.mirror)
				
		#draw object
		self.blAddObject = LifegameObject.data2bool(self.data_object,mirror=self.mirror).astype(dtype=np.uint8)
		
		part_img = Image.fromarray((1 - self.blAddObject) * 128 + 63)
		pilimgfile = io.BytesIO()
		part_img.save(pilimgfile, format='png')
		bytes_img = pilimgfile.getvalue()
		uiimg = ui.Image.from_data(bytes_img)
		texture = Texture(uiimg)
		SpriteNode.__init__(self,
			texture,
			position=position,
			z_position=1,
			**kwargs)
		self.margin = self.size * 0.4
		
	def rotate_object(self, degAdd=0, **kwargs):
		
		self.degree = (self.degree + degAdd) % 360

		position = self.position
		
		self.remove_from_parent()
				
		#draw object
		self.blAddObject = LifegameObject.data2bool(\
		self.data_object,
		rotate=self.degree,
		mirror=self.mirror).astype(dtype=np.uint8)
		
		part_img = Image.fromarray((1 - self.blAddObject) * 128 + 63)
		
		pilimgfile = io.BytesIO()
		part_img.save(pilimgfile, format='png')
		bytes_img = pilimgfile.getvalue()
		uiimg = ui.Image.from_data(bytes_img)
		texture = Texture(uiimg)
		SpriteNode.__init__(self,
			texture,
			position=position,
			z_position=1,
			**kwargs)
		
		self.margin = self.size * 0.4
		
		
	def move_position(self, pos_move):
		self.position = self.position + pos_move
	
	
class MyScene(Scene):
	
	def setup(self):
		# Set parameter
		self.flgStop = True
		self.intLowerMargin = 50
		self.intUpperMargin = 150
		self.modeEdit = False
		self.field = LifegameField(self.size.x, self.size.y - self.intLowerMargin - self.intUpperMargin)

		self.field.mySetObject(180,330,self.field.myAcorn())
		
		#self.flgStop = True
		#for i in range(300):
		#	self.field.field[250][25 + i] = True

		#pil_img = Image.open('./grade.png')
		pil_img = self.field.fieldImg()

		pilimgfile = io.BytesIO()
		pil_img.save(pilimgfile, format='png')
		bytes_img = pilimgfile.getvalue()
		uiimg = ui.Image.from_data(bytes_img)
		texture = Texture(uiimg)

		# SpriteNodeを使い、スクリーンに追加する
		#self.field_node = SpriteNode(texture, position=self.size/2)
		self.field_node = SpriteNode(
			texture,
			anchor_point=(0,0),
			position=(0, self.intLowerMargin),
			parent=self)
		
		# add labels
		self.lblGen = LabelNode(
			str(self.field.gen),
			font=('Helvetica', 12),
			anchor_point=(0,0),
			z_position=2,
			color='blue',
			parent=self)
		
		self.lblPoplation = LabelNode(
			str(self.field.field.sum()),
			font=('Helvetica', 12),
			anchor_point=(0,0),
			position=(70,0),
			z_position=2,
			color='blue',
			parent=self
			)
		
		self.lblMsg = LabelNode(
			str(self.size[0]) + ':' + str(self.size[1]), font=('Helvetica', 12),
			anchor_point=(0,0),
			position=(180,0),
			z_position=2,
			color='blue',
			parent=self)
		
		self.posPartX = LabelNode(
			'posPartX', 
			font=('Helvetica', 12),
			anchor_point=(0,0),
			position=(0,15),
			z_position=2,
			color='blue',
			parent=self)
		self.posPartY = LabelNode(
			'posPartY', 
			font=('Helvetica', 12),
			anchor_point=(0,0),
			position=(50,15),
			z_position=2,
			color='blue',
			parent=self)
		
		#add control areas
		
		paras = (\
			(0, '#c4e6ff', 'iob:settings_32'),
			(1, '#a0a0a0', 'iob:arrow_left_a_32'),
			(2, '#a0a0a0', 'iob:arrow_down_a_32'),
			(3, '#a0a0a0', 'iob:arrow_up_a_32'),
			(4, '#a0a0a0', 'iob:arrow_right_a_32'),
			(5, '#a0a0a0', 'iob:arrow_swap_32'),
			(6, '#a0a0a0', 'iob:ios7_undo_32'),
			(7, '#a0a0a0', 'iob:arrow_right_b_32'))
		self.btnBase = []
		
		for para in paras:
			self.btn = BaseButton(*para)
			self.add_child(self.btn)
			self.btnBase.append(self.btn)
			#self.add_child(self.btn0)
		
	def partsPosDisp(self):
		
		self.posPartX.text = str(self.parts_node.position.x)
		self.posPartY.text = str(self.parts_node.position.y - self.intLowerMargin)
		
	def button0_push(self):
		
		self.modeEdit = True
		self.flgStop = True
		#draw object
		self.parts_node = PartsFloat(LifegameObject.Glidergun, parent=self)
		self.modeEdit = True
				
		for i in range(6):
			self.btnBase[i + 1].bak.color = '#c4e6ff'
			
		
	def button1_push(self):
		
		if self.modeEdit == True:
			#self.parts_node.position = self.parts_node.position + (-1, 0)
			self.parts_node.move_position((-1, 0))
		self.partsPosDisp()
	
	def button2_push(self):
		self.parts_node.move_position((0, -1))
		self.partsPosDisp()
	def button3_push(self):
		self.parts_node.move_position((0, 1))
		self.partsPosDisp()
	def button4_push(self):
		self.parts_node.move_position((2, 0))
		self.partsPosDisp()
	def button5_push(self):
		self.parts_node.reverse_h(parent=self)
	
	def button6_push(self):
		self.parts_node.rotate_object(parent=self,degAdd=90)
		
	def button7_push(self):
		
		if self.modeEdit == True:
			self.parts_node.remove_from_parent()
			self.modeEdit = False
			self.flgStop = False
			self.field.mySetObject(self.parts_node.position[0],self.parts_node.position[1] - self.intLowerMargin, self.parts_node.blAddObject)
		for i in range(6):
			self.btnBase[i + 1].bak.color = '#a0a0a0'
			
		self.flgStop = not self.flgStop
	
	def update(self):
		if not(self.flgStop):
			self.field_node.remove_from_parent()

			self.field.field = self.field.update()
			
		pil_img = self.field.fieldImg()

		pilimgfile = io.BytesIO()
		pil_img.save(pilimgfile, format='png')
		bytes_img = pilimgfile.getvalue()
		uiimg = ui.Image.from_data(bytes_img)
		texture = Texture(uiimg)

		# SpriteNodeを使い、スクリーンに追加する
		#self.field_node = SpriteNode(texture, position=self.size/2)
		self.field_node = SpriteNode(
			texture,
			anchor_point=(0,0),
			position=(0, self.intLowerMargin),
			parent=self)
		#print(self.field.gen)
		#print(self.field.gen)
		
		self.lblGen.text =\
			'Gen.: ' + str(self.field.gen)
		self.lblPoplation.text =\
			'Poplation: ' + str(self.field.field.sum())

	def touch_began(self, touch):
		x, y = touch.location
		#self.flgStop = not(self.flgStop)
		
		if y < 50:
			if self.size.x - 50 < x :
				
				pass
				'''
				self.parts_node.remove_from_parent()
				self.modeEdit = False
				self.flgStop = False
				self.field.mySetObject(self.parts_node.position[0],self.parts_node.position[1] - self.intLowerMargin, self.parts_node.blAddObject)
				'''
			
			if x < 45 and self.modeEdit == False:
				
				self.button0_push()
				
			elif 45 < x and x < 90:
				self.button1_push()
				
			elif 90 <= x and x < 135:
				self.button2_push()
			
			elif 135 <= x and x < 190:
				self.button3_push()
			
			elif 190 <= x and x < 225:
				self.button4_push()
			
			elif 225 <= x and x < 270:
				self.button5_push()
				
			elif 270 <= x and x < 315:
				self.button6_push()
				
			elif 315 <= x and x < 360:
				self.button7_push()
			
		else:
			pass
			
		if self.modeEdit == True:
			self.partsBase = self.parts_node.position
			self.touchBase = touch.location
			

	def touch_moved(self, touch):
		if self.modeEdit == True:
			touchMoved = touch.location
		
			d = touchMoved - self.touchBase
			target = self.partsBase + d
			
			target.x = int(max(- self.parts_node.margin.x, min(self.size.x + self.parts_node.margin.x, target.x)))
			target.y = int(max(-self.parts_node.margin.y, min(self.size.y + self.parts_node.margin.y, target.y)))
			self.parts_node.position = target
			
			self.posPartX.text = str(target.x)
			self.posPartY.text = str(target.y - self.intLowerMargin)
			#self.lblTouchMovedX.text = str(target.x)
			#self.lblTouchMovedY.text = str(target.y)

if __name__ =='__main__':

	run(MyScene(), PORTRAIT, show_fps=True, frame_interval=3)
