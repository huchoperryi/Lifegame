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

class MyScene(Scene):
	
	def setup(self):
		self.flgStop = False
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
		self.field_node = SpriteNode(texture, anchor_point=(0,0), position=(0, self.intLowerMargin))

		self.add_child(self.field_node)
		
		self.lblGen = LabelNode(str(self.field.gen), font=('Helvetica', 12))
		self.lblGen.anchor_point = (0,0)
		
		self.add_child(self.lblGen)
		
		self.lblPoplation = LabelNode(str(self.field.field.sum()), font=('Helvetica', 12))
		self.lblPoplation.anchor_point = (0,0)
		self.lblPoplation.position = (70, 0)
		self.add_child(self.lblPoplation)
		
		self.lblMsg = LabelNode(str(self.size[0]) + ':' + str(self.size[1]), font=('Helvetica', 12))
		self.lblMsg.anchor_point = (0,0)
		self.lblMsg.position = (180, 0)
		self.add_child(self.lblMsg)
		
		self.posPartX = LabelNode(\
			'posPartX', 
			font=('Haelvetica', 12),
			anchor_point=(0,0),
			position=(0,15),
			parent=self)
		self.posPartY = LabelNode(\
			'posPartY', 
			font=('Haelvetica', 12),
			anchor_point=(0,0),
			position=(50,15),
			parent=self)
		
		'''
		#test
		part_img = Image.fromarray((1 - LifegameObject1_1.data2bool(LifegameObject1_1.Glidergun).astype(dtype=np.uint8)) * 255)
		part_img.show()
		pilimgfile = io.BytesIO()
		part_img.save(pilimgfile, format='png')
		bytes_img = pilimgfile.getvalue()
		uiimg = ui.Image.from_data(bytes_img)
		texture = Texture(uiimg)
		self.parts_node = SpriteNode(texture, anchor_point=(0,0), position=(0,45), z_position=1)
		self.add_child(self.parts_node)
		'''

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
		self.field_node = SpriteNode(texture, anchor_point=(0,0), position=(0, self.intLowerMargin))

		self.add_child(self.field_node)
		#print(self.field.gen)
		#print(self.field.gen)
		
		self.lblGen.text = 'Gen.: ' + str(self.field.gen)
		self.lblPoplation.text = 'Poplation: ' + str(self.field.field.sum())

	def touch_began(self, touch):
		x, y = touch.location
		#self.flgStop = not(self.flgStop)
		
		if y < 50:
			if self.size.x - 50 < x :
				self.parts_node.remove_from_parent()
				self.modeEdit = False
				self.flgStop = False
				self.field.mySetObject(self.parts_node.position[0],self.parts_node.position[1] - self.intLowerMargin, self.object_add)
			if x < 50 and self.modeEdit == False:
				
				self.modeEdit = True
				self.flgStop = True
				#draw object
				self.object_add = LifegameObject.data2bool(LifegameObject.Glidergun).astype(dtype=np.uint8)
				part_img = Image.fromarray((1 - self.object_add) * 128 + 63)
				pilimgfile = io.BytesIO()
				part_img.save(pilimgfile, format='png')
				bytes_img = pilimgfile.getvalue()
				uiimg = ui.Image.from_data(bytes_img)
				texture = Texture(uiimg)
				self.parts_node = SpriteNode(texture, anchor_point=(0,0), position=self.size / 2, z_position=1)
				self.add_child(self.parts_node)
				
				self.parts_node.margin = self.parts_node.size * 0.4
				
				self.modeEdit = True
				
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

	run(MyScene(), PORTRAIT, show_fps=True)
