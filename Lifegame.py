import numpy as np
import console
from scene import *
from PIL import Image
import ui, io
from time import sleep
import math

from LifegameObject import data2bool, lifegame_object

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

	
class button(ShapeNode):
	
	def __init__(self, pos_btn, w, h, 
		btn_color='#c4e6ff',
		str_text='', str_symbol=''):
		
		#set button base
		super().__init__(
			path=ui.Path.rounded_rect(0,0,w,h,5),
			anchor_point=(0,0),
			color=btn_color,
			position=pos_btn
			)
		#set text on button
		if str_text != '':
			self.Label = LabelNode(
				str_text,
				anchor_point=(0,0.5),
				position=(5,h / 2),
				color='black',
				parent=self
				)
		#set symbol on button
		if str_symbol != '':
			self.symbol = SpriteNode(
				str_symbol,
				position=(w / 2, h / 2),
				parent=self)


def BaseButton(intId, bgcolor, strSymbol):
	
	width = 45
	height = 50
	margin = 1
	
	_button = button(
		(intId * width, 0),
		width-margin,
		height,
		btn_color=bgcolor,
		str_text='',
		str_symbol=strSymbol)
		
	return _button
	
	
class btnObjectSelect(SpriteNode):
	
	def __init__(self, intId, bgcolor='#a0a0a0', strLabel='test'):
		width = 300
		height = 40
		r = 5
		margin = 1
		label_size = 25
		
		self.bak = ShapeNode(\
			path = ui.Path.rounded_rect(\
			0,0,
			width, height - margin,
			r),
			color=bgcolor,
			anchor_point=(0,0),
			position=(0, intId * height + 50),
			z_position=1,
			parent=self)
		
		self.strLabel = LabelNode(
			strLabel,
			font=('Helvetica', label_size),
			anchor_point=(0,0.5),
			position=(10, intId * height + 50 + height / 2),
			z_position=5,
			color='black',
			parent=self)
			
		
class PartsFloat(SpriteNode):
	
	def __init__(self, data_object, **kwargs):
		
		#set parameter
		self.mirror = ''
		self.data_object = data_object
		self.degree= 0
		
		#draw object
		self.blAddObject = data2bool(data_object).astype(dtype=np.uint8)
		part_img = Image.fromarray((1 - self.blAddObject) * 255)
		pilimgfile = io.BytesIO()
		part_img.save(pilimgfile, format='png')
		bytes_img = pilimgfile.getvalue()
		uiimg = ui.Image.from_data(bytes_img)
		texture = Texture(uiimg)
		SpriteNode.__init__(self,
			texture,
			position=(100,100),
			anchor_point=(0,0),
			z_position=-1,
			**kwargs)
		self.margin = self.size * 0.4
	
	def reverse_h(self, **kwargs):
		
		position = self.position
		
		self.remove_from_parent()
		'''
		if self.mirror == '':
			self.mirror = 'h'
			
		elif self.mirror == 'h':
			self.mirror = ''
			
		else:
			print('mirror parameter error ', self.mirror)
		'''
		
		#draw object
		'''
		self.blAddObject = data2bool(self.data_object,mirror='h').astype(dtype=np.uint8)
		'''
		#print(self.data_object)
		self.blAddObject = self.blAddObject[:, ::-1]
		
		part_img = Image.fromarray((1 - self.blAddObject) * 255)
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
		
		self.data_object = self.blAddObject
		
	def rotate_object(self, degAdd=0, **kwargs):
		
		self.degree = (self.degree + degAdd) % 360

		position = self.position
		
		self.remove_from_parent()
				
		#draw object
		'''
		self.blAddObject = data2bool(\
		self.data_object,
		rotate=self.degree,
		mirror=self.mirror).astype(dtype=np.uint8)
		'''
		self.blAddObject = self.blAddObject.T[::-1]
		
		part_img = Image.fromarray((1 - self.blAddObject) * 255)
		
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
		self.flgObjectSelectButton = False
		self.ObjectSelectButtons = []
		self.field = LifegameField(self.size.x, self.size.y - self.intLowerMargin - self.intUpperMargin)
		self.mode = 'pause'
		# pause, run, edit, edit_select
		#self.field.mySetObject(180,330,data2bool(lifegame_object['Acorn']))

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
			z_position=-2,
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
			(7, '#c4e6ff', 'iob:arrow_right_b_32'))
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
		
		'''
		self.modeEdit = not self.modeEdit
		self.flgStop = True
		
		#draw object
		self.parts_node = PartsFloat(lifegame_object['Glidergun'], parent=self)
		'''
		
		if self.mode == 'pause':
			
			if self.flgObjectSelectButton == False:
				color = '#4ee6ff'
				paras = (\
					(0, color, ''),
					(1, color, ''),
					(2, color, ''),
					(3, color, ''),
					(4, color, ''),
					(5, color, ''),
					(6, color, ''),
					(7, color, ''),
					(8, color, ''),
					(9, color, ''),
					(10, color, ''),
					(11, color, ''))
				
				for para in paras:
					self.btnObjSlct = btnObjectSelect(*para)
					self.add_child(self.btnObjSlct)
					self.ObjectSelectButtons.append(self.btnObjSlct)
				
				object_list = list(lifegame_object.keys())
				
				for i in range(len(object_list)):
					self.ObjectSelectButtons[i].strLabel.text = object_list[i]
				
				#self.flgOjectSelectButton = True
				self.flgObjectSelectButton = True
				
			self.change_mode('edit_select')
			
		elif self.mode == 'edit_select':
			
			for btn in self.ObjectSelectButtons:
				btn.bak.remove_from_parent()
				btn.strLabel.remove_from_parent()
				#btn.removefromparent()
				#self.ObjectSelectButtons.remove(btn)
				
			self.ObjectSelectButtons =[]
				
			self.flgObjectSelectButton = False
			self.change_mode('pause')
			
		elif self.mode == 'edit':
			
			self.parts_node.remove_from_parent()
			self.modeEdit = False
			self.flgStop = False
			self.field.mySetObject(self.parts_node.position[0],self.parts_node.position[1] - self.intLowerMargin, self.parts_node.blAddObject)
			self.change_mode('pause')
			
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
		
		if self.mode == 'pause':
			#self.flgStop = False
			self.change_mode('run')
			
		elif self.mode == 'run':
			self.change_mode('pause')
			

	def selectbutton_push(self, x, y):
		
		int_button = math.floor((y - 50) / 40)
		
		self.parts_node = PartsFloat(lifegame_object[list(lifegame_object.keys())[int_button]], parent=self)
		
		for btn in self.ObjectSelectButtons:
				btn.bak.remove_from_parent()
				btn.strLabel.remove_from_parent()
				
		self.ObjectSelectButtons =[]
		
		self.flgObjectSelectButton = False
		self.change_mode('edit')

	def change_mode(self, mode):
		
		able = '#c4e6ff'
		enable = '#a0a0a0'
		
		if mode == 'run':
			
			self.btnBase[0].color = enable
			self.btnBase[1].color = enable
			self.btnBase[2].color = enable
			self.btnBase[3].color = enable
			self.btnBase[4].color = enable
			self.btnBase[5].color = enable
			self.btnBase[6].color = enable
			self.btnBase[7].color = able
			
			self.btnBase[7].symbol.texture = Texture('iob:pause_32')
			
			self.mode = 'run'
			
		elif mode == 'pause':
			
			self.btnBase[0].color = able
			self.btnBase[1].color = enable
			self.btnBase[2].color = enable
			self.btnBase[3].color = enable
			self.btnBase[4].color = enable
			self.btnBase[5].color = enable
			self.btnBase[6].color = enable
			self.btnBase[7].color = able
			
			self.btnBase[7].symbol.texture = Texture('iob:arrow_right_b_32')
			
			self.mode = 'pause'
			
		elif mode == 'edit_select':
			
			self.btnBase[0].color = able
			self.btnBase[1].color = enable
			self.btnBase[2].color = enable
			self.btnBase[3].color = enable
			self.btnBase[4].color = enable
			self.btnBase[5].color = enable
			self.btnBase[6].color = enable
			self.btnBase[7].color = enable
			
			self.mode = 'edit_select'
			
		elif mode == 'edit':
			
			self.btnBase[0].color = able
			self.btnBase[1].color = able
			self.btnBase[2].color = able
			self.btnBase[3].color = able
			self.btnBase[4].color = able
			self.btnBase[5].color = able
			self.btnBase[6].color = able
			self.btnBase[7].color = enable
			
			self.mode = 'edit'
			
		else:
			
			print('mode change wrong mode')
		
		self.lblMsg.text = 'Mode: ' + self.mode
		

	def update(self):
		if self.mode == 'run':
			
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
			z_position=-2,
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
			
			if x < 45:
				
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
			
		elif y < 500:
			
			if x < 300:
				if self.mode == 'edit_select':
					self.selectbutton_push(x, y)
					
				
		else:
			pass
			
		if self.mode == 'edit':
			self.partsBase = self.parts_node.position
			self.touchBase = touch.location
			

	def touch_moved(self, touch):
		if self.mode == 'edit':
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
