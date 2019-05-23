

import pygame
from pygame.locals import * 
from constantes import *
import random

class Niveau:
	"""Classe permettant de créer un niveau"""
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0
	
	
	def generer(self):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""	
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau

	def victoire(self):#victoire si il n'y a plus rien à manger
		V=True
		for x in range (nombre_sprite_largeur):
			for y in range (nombre_sprite_longueur):
				if self.structure[y][x]=='p'or self.structure[y][x]=='G':
					V=False
		
	
	def afficher(self, fenetre):
		#on appelle L=ligne C=colonne les murs, 1=coin hd, 2= coin bd,3=coin bg, 4=coin hg
		# v=vide, p=point. Le labyrinthe étant faux, il faut intervertir 3 et 1 ainsi que 2 et 4
		"""Méthode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyée par generer()"""
		#Chargement des images (seule celle d'arrivée contient de la transparence)
		imageligne = pygame.image.load(image_ligne).convert()
		colonne= pygame.image.load(image_colonne).convert()
		coin_1= pygame.image.load(image_coin_1).convert()
		coin_2= pygame.image.load(image_coin_2).convert()
		coin_3= pygame.image.load(image_coin_3).convert()
		coin_4= pygame.image.load(image_coin_4).convert()
		point = pygame.image.load(image_point).convert()
		vide = pygame.image.load(image_vide).convert_alpha()
		gomme =pygame.image.load(image_gomme).convert()
		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'L':		   
					fenetre.blit(imageligne, (x,y))
				elif sprite == 'C':		  
					fenetre.blit(colonne, (x,y))
				elif sprite == '1':		   
					fenetre.blit(coin_3, (x,y))
				elif sprite == '2':
					fenetre.blit(coin_4, (x,y))
				elif sprite== '3':
					fenetre.blit(coin_1, (x,y))
				elif sprite=='4':
					fenetre.blit(coin_2, (x,y))
				elif sprite=='p':
					fenetre.blit(point, (x,y))
				elif sprite=='G':
					fenetre.blit(gomme,(x,y))
				elif sprite=='v':
					fenetre.blit(vide, (x,y))
				num_case += 1
			num_ligne += 1

			

class fruit:
	def __init__(self,score,case_x,case_y):
		self.score=score
		self.case_x=case_x
		self.case_y=case_y			
			
			
class PACMAN:
	"""Classe permettant de créer un personnage"""
	def __init__(self, droite, gauche, haut, bas, niveau,score):

		#Sprites du personnage
		self.droite = pygame.image.load(droite).convert_alpha()
		self.gauche = pygame.image.load(gauche).convert_alpha()
		self.haut = pygame.image.load(haut).convert_alpha()
		self.bas = pygame.image.load(bas).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 15
		self.case_y = 23
		self.x = 15*taille_sprite
		self.y = 23*taille_sprite
		#Direction par défaut
		self.direction = self.droite
		#Niveau dans lequel le personnage se trouve 
		self.niveau = niveau
		#score accumulé
		self.score=score
	
	
	def deplacer(self, direction):
		"""Methode permettant de déplacer le personnage"""
		
		#Déplacement vers la droite
		if direction == 'droite':
			#Pour ne pas dépasser l'écran, s'arrêter si on rencontre un coin bas gauche, un coin haut gauche ou une colonne.
			if  self.case_x < (nombre_sprite_largeur - 1)  and self.niveau.structure[self.case_y][self.case_x+1] != 'C' and self.niveau.structure[self.case_y][self.case_x+1] != '1' and self.niveau.structure[self.case_y][self.case_x+1] != '2'  and self.niveau.structure[self.case_y][self.case_x+1] != 'L':
				#Image dans la bonne direction
				self.direction = self.droite
				#Déplacement d'une case
				self.case_x+=1
				#Calcul de la position "réelle" en pixel
				self.x = self.case_x * taille_sprite
			
			elif self.case_x==nombre_sprite_largeur-1:
				self.case_x+=1
				self.case_x= self.case_x%30
				self.x=self.case_x*taille_sprite

		#Déplacement vers la gauche
		if direction == 'gauche':
			if self.case_x > 0 and  self.niveau.structure[self.case_y][self.case_x-1] != 'C' and  self.niveau.structure[self.case_y][self.case_x-1] != '3' and  self.niveau.structure[self.case_y][self.case_x-1] != '4' and self.niveau.structure[self.case_y][self.case_x-1] != 'L':
				self.direction = self.gauche
				self.case_x -= 1
				self.x = self.case_x * taille_sprite


		
		#Déplacement vers le haut
		if direction == 'haut':
			if self.case_y > 0 and self.niveau.structure[self.case_y-1][self.case_x] != 'L' and self.niveau.structure[self.case_y-1][self.case_x] != '1' and self.niveau.structure[self.case_y-1][self.case_x] != '4':
				self.direction = self.haut
				self.case_y -= 1
				self.y = self.case_y * taille_sprite


		
		#Déplacement vers le bas
		if direction == 'bas':
			if self.case_y < (nombre_sprite_longueur -1) and self.niveau.structure[self.case_y+1][self.case_x] != 'L' and self.niveau.structure[self.case_y+1][self.case_x] != '3' and self.niveau.structure[self.case_y+1][self.case_x] != '2':
				self.direction = self.bas
				self.case_y += 1
				self.y = self.case_y * taille_sprite


		#déplacement standard
		if direction== 'standard':
			if self.direction== self.bas and self.case_y < (nombre_sprite_longueur -1) and self.niveau.structure[self.case_y+1][self.case_x] != 'L' and self.niveau.structure[self.case_y+1][self.case_x] != '3' and self.niveau.structure[self.case_y+1][self.case_x] != '2':
				self.case_y += 1
				self.y = self.case_y * taille_sprite 

			elif self.direction==self.haut and self.case_y > 0 and self.niveau.structure[self.case_y-1][self.case_x] != 'L' and self.niveau.structure[self.case_y-1][self.case_x] != '4' and self.niveau.structure[self.case_y-1][self.case_x] != '1':
				self.case_y -= 1
				self.y = self.case_y * taille_sprite 

			elif self.direction== self.gauche and self.case_x > 0 and  self.niveau.structure[self.case_y][self.case_x-1] != 'C' and  self.niveau.structure[self.case_y][self.case_x-1] != '3' and  self.niveau.structure[self.case_y][self.case_x-1] != '4':
				self.case_x -= 1
				self.x = self.case_x * taille_sprite 

			elif self.direction== self.gauche and self.case_x == 0:
				self.case_x-=1
				self.case_x=self.case_x%30
				self.x=self.case_x*taille_sprite

			elif self.direction==self.droite and self.case_x < (nombre_sprite_largeur - 1)  and self.niveau.structure[self.case_y][self.case_x+1] != 'C' and self.niveau.structure[self.case_y][self.case_x+1] != '1' and self.niveau.structure[self.case_y][self.case_x+1] != '2':
				self.case_x += 1
				self.x = self.case_x * taille_sprite 

			elif self.direction == self.droite and self.case_x == nombre_sprite_largeur-1:
				self.case_x+=1
				self.case_x= self.case_x%30
				self.x=self.case_x*taille_sprite

	def eatFruit(self, fruit):
		self.score=self.score+ fruit.score

	def eatGum(self):
		self.score += 2
		



class ghost :
	def __init__(self,name,decompte_bleu, decompte, image, imagebleue, perso, direction, départ_x, départ_y):
		self.name= name
		#Position du personnage en cases et en pixels
		self.case_x = départ_x
		self.case_y = départ_y
		self.x = self.case_x*taille_sprite
		self.y = self.case_y*taille_sprite
		#visuel du fantôme
		self.image= pygame.image.load(image).convert_alpha()
		self.bleu=pygame.image.load(imagebleue).convert_alpha()
		self.perso=perso
		self.score=100
		self.direction= direction
		#si decompte est nul, fantome en etat normal, sinon bleu
		self.decompte_bleu=decompte_bleu
		self.decompte=decompte

	def Chasing_clyde(self):

		#on commence à marquer le labyrinthe avec un parcours en largeur
		labyrinthe_marqué=[]
		labyrinthe_visité=[]
		for i in range (0, nombre_sprite_longueur):
			labyrinthe_marqué.append([1000]*nombre_sprite_largeur)
			labyrinthe_visité.append([0]*nombre_sprite_largeur)

		labyrinthe=self.perso.niveau.structure
		
		for i in range (0, nombre_sprite_longueur):
			for j in range (0, nombre_sprite_largeur):
				if labyrinthe[i][j]!='v' and labyrinthe[i][j] !='p':
					labyrinthe_visité[i][j]=1
				else:
					labyrinthe_visité[i][j]=0
		case_y=self.perso.case_y
		case_x=self.perso.case_x
		case=(case_y, case_x)
		labyrinthe_visité[case_y][case_x]=1
		à_visiter=[]
		labyrinthe_marqué[case_y][case_x]=0

		# on ajoute tous les voisins de la case à à_visiter puis on leur donne le score de la case
		if case_y+1 <nombre_sprite_longueur -1 and labyrinthe_visité[case_y+1][case_x]==0:
			à_visiter.append((case_y+1, case_x))
			labyrinthe_marqué[case_y+1][case_x]=0			
		if case_y-1>0 and labyrinthe_visité[case_y-1][case_x]==0:
			à_visiter.append((case_y-1, case_x))
			labyrinthe_marqué[case_y-1][case_x]=0
		if case_x-1>0 and labyrinthe_visité[case_y][case_x-1]==0:
			à_visiter.append((case_y, case_x-1))
			labyrinthe_marqué[case_y][case_x-1]=0
		if case_x+11< nombre_sprite_largeur -1 and labyrinthe_visité[case_y][case_x+1]==0:
			à_visiter.append((case_y, case_x+1))
			labyrinthe_marqué[case_y][case_x+1]=0 


		while à_visiter !=[]:

			(case_y, case_x)=à_visiter[0]
			à_visiter.remove((case_y, case_x))
			labyrinthe_visité[case_y][case_x]=1 #on indique qu'on a déjà visité cette case
			labyrinthe_marqué[case_y][case_x]+=1  #on augmente le score de la case de 1
			if case_y+1<nombre_sprite_longueur-1 and labyrinthe_visité[case_y+1][case_x]==0:
				à_visiter.append((case_y+1, case_x))
				labyrinthe_marqué[case_y+1][case_x]=labyrinthe_marqué[case_y][case_x]	
			if case_y -1 >0 and labyrinthe_visité[case_y-1][case_x]==0:
				à_visiter.append((case_y-1, case_x))
				labyrinthe_marqué[case_y-1][case_x]=labyrinthe_marqué[case_y][case_x]
			if case_x-1 >0 and labyrinthe_visité[case_y][case_x-1]==0:
				à_visiter.append((case_y, case_x-1))
				labyrinthe_marqué[case_y][case_x-1]=labyrinthe_marqué[case_y][case_x]
			if case_x+1<nombre_sprite_largeur-1 and labyrinthe_visité[case_y][case_x+1]==0:
				à_visiter.append((case_y, case_x+1))
				labyrinthe_marqué[case_y][case_x+1]=labyrinthe_marqué[case_y][case_x]

		#le labyrinthe étant marqué, on déplace le fantôme
		bas=labyrinthe_marqué[self.case_y+1][self.case_x]
		haut=labyrinthe_marqué[self.case_y-1][self.case_x]
		droite=labyrinthe_marqué[self.case_y][(self.case_x+1)%30]
		gauche=labyrinthe_marqué[self.case_y][(self.case_x-1)%30]
		if droite<=gauche and droite<=haut and droite <=bas:
			self.case_x+=1
			self.case_x= self.case_x%30
			self.x=self.case_x*taille_sprite
		elif gauche <= droite and gauche <= haut and gauche <= bas:
			self.case_x-=1
			self.case_x= self.case_x%30
			self.x=self.case_x*taille_sprite
		elif bas <= haut and bas <= gauche and bas <= droite:
			self.case_y+=1
			self.y=self.case_y*taille_sprite
		elif haut <= bas and haut <= droite and haut <= gauche:
			self.case_y-=1
			self.y=self.case_y*taille_sprite





	
	def Blue(self):
		self.decompte_bleu=40 #nombre de tours de boucle durant lesquels le fantome est bleu
	



	def Chasing_pinky(self):
		# sort du milieu
		if self.case_y==15 and (self.case_x==12 or self.case_x==13 or self.case_x==14 or self.case_x==15 or self.case_x==16 or self.case_x==17):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==14 and (self.case_x==12 or self.case_x==13 or self.case_x==14 or self.case_x==15 or self.case_x==16 or self.case_x==17):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==13 and (self.case_x==12 or self.case_x==13):
			self.case_x+=1
			self.x=self.case_x*taille_sprite
			self.direction='droite'
		elif self.case_y==13 and (self.case_x==16 or self.case_x==17):
			self.case_x-=1
			self.x=self.case_x*taille_sprite
			self.direction='gauche'
		elif self.case_y==13 and (self.case_x==14 or self.case_x==15):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==12 and (self.case_x==14 or self.case_x==15):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_x==nombre_sprite_largeur-1 and self.direction=='droite': #le fantome est dans le passage secret, il passe de l'autre cote:
			self.case_x=0
			self.x=self.case_x*taille_sprite
		elif self.case_x==0 and self.direction=='gauche':
			self.case_x==nombre_sprite_largeur-1
			self.x=self.case_x*taille_sprite
			
		else: #fait toujours le même mouvement: se déplace d'abord à droite, puis en bas , puis à gauche , puis en haut dans le quart haut gauche du plateau, et cet ordre tourne pour les autres quarts, ne peut repartir dans en sens inverse pour eviter de rester sur place
			Ml=3*nombre_sprite_largeur//2 #separation de la largeur
			ML=3*nombre_sprite_longueur//2 #separation de la longeur
			
			#1er quart du plateau
			if 0<=self.case_x<Ml and 0<=self.case_y<ML:# droite, sinon bas, sinon gauche, sinon haut
				if (self.perso.niveau.structure[self.case_y][self.case_x+1]=='p'or self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G') and self.direction !='gauche':#droite
					self.case_x= (self.case_x+1)%nombre_sprite_largeur
					self.x=self.case_x*taille_sprite
					self.direction='droite'
				elif (self.perso.niveau.structure[self.case_y+1][self.case_x]=='p'or self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G') and self.direction!='haut':#bas
					self.case_y= (self.case_y+1)%nombre_sprite_longueur
					self.y=self.case_y*taille_sprite
					self.direction='bas'
				elif (self.perso.niveau.structure[self.case_y][self.case_x-1]=='p'or self.perso.niveau.structure[self.case_y][self.case_x-1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x-1]=='G') and self.direction!='droite':#gauche
					self.case_x= (self.case_x-1)%nombre_sprite_largeur
					self.x=self.case_x*taille_sprite
					self.direction='gauche'
				elif (self.perso.niveau.structure[self.case_y-1][self.case_x]=='p'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='G') and self.direction!='bas':#haut
					self.case_y= (self.case_y-1)%nombre_sprite_longueur
					self.y=self.case_y*taille_sprite
					self.direction='haut'
			
			elif Ml<=self.case_x<nombre_sprite_largeur and 0<=self.case_y<ML: # quart haut droit: bas sinon gauche, sinon haut sinon droit
				if (self.perso.niveau.structure[self.case_y+1][self.case_x]=='p'or self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G') and self.direction!='haut':#bas
					self.case_y= (self.case_y+1)%nombre_sprite_longueur
					self.y=self.case_y*taille_sprite
					self.direction='bas'
				elif (self.perso.niveau.structure[self.case_y][self.case_x-1]=='p'or self.perso.niveau.structure[self.case_y][self.case_x-1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x-1]=='G') and self.direction!='droite':#gauche
					self.case_x= (self.case_x-1)%nombre_sprite_largeur
					self.x=self.case_x*taille_sprite
					self.direction='gauche'
				elif (self.perso.niveau.structure[self.case_y-1][self.case_x]=='p'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='G') and self.direction!= 'bas':#haut
					self.case_y= (self.case_y-1)%nombre_sprite_longueur
					self.y=self.case_y*taille_sprite
					self.direction='haut'
				elif (self.perso.niveau.structure[self.case_y][self.case_x+1]=='p'or self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G') and self.direction!='gauche':#droite
					self.case_x= (self.case_x+1)%nombre_sprite_largeur
					self.x=self.case_x*taille_sprite
					self.direction='droite'
			
			elif ML<=self.case_y<nombre_sprite_longueur and 0<=self.case_x<Ml: #quart bas gauche : droite puis haut puis gauche puis bas
				if (self.perso.niveau.structure[self.case_y][self.case_x+1]=='p'or self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G') and self.direction!='gauche':#droite
					self.case_x= (self.case_x+1)%nombre_sprite_largeur
					self.x=self.case_x*taille_sprite
					slef.direction='droite'
				elif (self.perso.niveau.structure[self.case_y-1][self.case_x]=='p'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='G') and self.direction!= 'bas':#haut
					self.case_y= (self.case_y-1)%nombre_sprite_longueur
					self.y=self.case_y*taille_sprite
					self.direction='haut'
				elif (self.perso.niveau.structure[self.case_y][self.case_x-1]=='p'or self.perso.niveau.structure[self.case_y][self.case_x-1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x-1]=='G') and self.direction!='droite':#gauche
					self.case_x= (self.case_x-1)%nombre_sprite_largeur
					self.x=self.case_x*taille_sprite
					self.direction='droite'
				elif (self.perso.niveau.structure[self.case_y+1][self.case_x]=='p'or self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G') and self.direction!='haut':#bas
					self.case_y= (self.case_y+1)%nombre_sprite_longueur
					self.y=self.case_y*taille_sprite
					self.direction='bas'
			
			elif ML<=self.case_y<nombre_sprite_longueur and Ml<=self.case_x<nombre_sprite_largeur : #quart bas droit: bas, gauche, haut, droit
				if (self.perso.niveau.structure[self.case_y+1][self.case_x]=='p'or self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G') and self.direction!='haut':#bas
					self.case_y= (self.case_y+1)%nombre_sprite_longueur
					self.y=self.case_y*taille_sprite
					self.direction='bas'
				elif (self.perso.niveau.structure[self.case_y][self.case_x-1]=='p'or self.perso.niveau.structure[self.case_y][self.case_x-1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x-1]=='G') and self.direction!='droite':#gauche
					self.case_x= (self.case_x-1)%nombre_sprite_largeur
					self.x=self.case_x*taille_sprite
					self.direction='gauche'
				elif (self.perso.niveau.structure[self.case_y-1][self.case_x]=='p'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='G') and self.direction!= 'bas':#haut
					self.case_y= (self.case_y-1)%nombre_sprite_longueur
					self.y=self.case_y*taille_sprite
					self.direction='haut'
				elif (self.perso.niveau.structure[self.case_y][self.case_x+1]=='p'or self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G') and self.direction!='gauche':#droite
					self.case_x= (self.case_x+1)%nombre_sprite_largeur
					self.x=self.case_x*taille_sprite
					self.direction='droite'

	def Chasing_inky(self):
		#inky se déplace de manière aléatoire ,1=bas, 2=haut,3=gauche,4=droite apres etre sorti du carré
		if self.case_y==15 and (self.case_x==12 or self.case_x==13 or self.case_x==14 or self.case_x==15 or self.case_x==16 or self.case_x==17):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==14 and (self.case_x==12 or self.case_x==13 or self.case_x==14 or self.case_x==15 or self.case_x==16 or self.case_x==17):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==13 and (self.case_x==12 or self.case_x==13):
			self.case_x+=1
			self.x=self.case_x*taille_sprite
			self.direction='droite'
		elif self.case_y==13 and (self.case_x==16 or self.case_x==17):
			self.case_x-=1
			self.x=self.case_x*taille_sprite
			self.direction='gauche'
		elif self.case_y==13 and (self.case_x==14 or self.case_x==15):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==12 and (self.case_x==14 or self.case_x==15):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_x==nombre_sprite_largeur-1 and self.direction=='droite': #le fantome est dans le passage secret, il passe de l'autre cote:
			self.case_x=0
			self.x=self.case_x*taille_sprite
		elif self.case_x==0 and self.direction=='gauche':
			self.case_x==nombre_sprite_largeur-1
			self.x=self.case_x*taille_sprite
			
		else:
			b=False
			while not b:
				if self.direction=='haut': #on va aleatoirement dans les directions possibles snas faire demi tour
					a=random.randint(1,3)
					if a==1 and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]== 'G'):
						self.case_y=(self.case_y-1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='haut'
						b=True
					elif a==2 and (self.perso.niveau.structure[self.case_y][self.case_x-1]=='v'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'p'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'G'):
						self.case_x=(self.case_x-1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='gauche'
						b=True
					elif a==3 and (self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='p' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G'):
						self.case_x=(self.case_x+1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='droite'
						b=True
				
				elif self.direction=='bas':
					a=random.randint(1,3)
					if a==1 and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'):
						self.case_y=(self.case_y+1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='bas'
						b=True
					elif a==2 and (self.perso.niveau.structure[self.case_y][self.case_x-1]=='v'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'p'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'G'):
						self.case_x=(self.case_x-1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='gauche'
						b=True
					elif a==3 and (self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='p' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G'):
						self.case_x=(self.case_x+1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='droite'
						b=True
				
				elif self.direction=='droite':
					a=random.randint(1,3)
					if a==1 and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]== 'G'):
						self.case_y=(self.case_y-1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='haut'
						b=True
					elif a==2 and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'):
						self.case_y=(self.case_y+1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='bas'
						b=True
					elif a==3 and (self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='p' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G'):
						self.case_x=(self.case_x+1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='droite'
						b=True
						
				elif self.direction=='gauche':
					a=random.randint(1,3)
					if a==1 and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]== 'G'):
						self.case_y=(self.case_y-1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='haut'
						b=True
					elif a==2 and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'):
						self.case_y=(self.case_y+1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='bas'
						b=True
					elif a==3 and (self.perso.niveau.structure[self.case_y][self.case_x-1]=='v'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'p'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'G'):
						self.case_x=(self.case_x-1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='gauche'
						b=True



	def Chasing_Blinky(self):

		#cas particulier de quand Blinky est dans la case départ, pour qu'il sorte sans accroche

		if self.case_y==15 and (self.case_x==12 or self.case_x==13 or self.case_x==14 or self.case_x==15 or self.case_x==16 or self.case_x==17):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'

		elif self.case_y==14 and (self.case_x==12 or self.case_x==13 or self.case_x==14 or self.case_x==15 or self.case_x==16 or self.case_x==17):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'

		elif self.case_y==13 and (self.case_x==12 or self.case_x==13):
			self.case_x+=1
			self.x=self.case_x*taille_sprite
			self.direction='droite'

		elif self.case_y==13 and (self.case_x==16 or self.case_x==17):
			self.case_x-=1
			self.x=self.case_x*taille_sprite
			self.direction='gauche'

		elif self.case_y==13 and (self.case_x==14 or self.case_x==15):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'

		elif self.case_y==12 and (self.case_x==14 or self.case_x==15):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'

		elif self.case_y==11 and self.case_x==14:
			self.case_x+=1
			self.x=self.case_x*taille_sprite
			self.direction='droite'

		elif self.case_y==11 and self.case_x==15:
			self.case_x+=1
			self.x=self.case_x*taille_sprite
			self.direction='droite'




	#fin des exceptions

		else:

			#calcule difference en abscisse et ordonnee et parcourt le chemin le plus long des differences en 1er
			dif_x= self.perso.case_x-self.case_x # abscisse de pacman - abscisse du fantômeme
			dif_y= self.perso.case_y-self.case_y #ordonnée de pacman - ordonnée du fantôme



			if dif_x<=0 and dif_y<=0: #le pacman est en haut à gauche pas rapport au fantôme


        #cas particulier de quand le fantôme est bloqué dans un coin

			# fin des cas particuliers

				if abs(dif_x)>=abs(dif_y): #il y plus de distance à parcourir en abscisse qu'en ordonnée


					if self.case_x>=0 and  self.direction != 'droite' and (self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'v' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'p' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'G'): #s'il y a du vide à gauche, on va à gauche
						self.case_x -= 1
						self.case_x= self.case_x%30
						self.x = self.case_x * taille_sprite
						self.direction='gauche'

					elif self.case_y>0 and self.direction != 'bas' and (self.perso.niveau.structure[self.case_y -1][self.case_x] == 'v' or self.perso.niveau.structure[self.case_y -1][self.case_x] == 'p' or self.perso.niveau.structure[self.case_y -1][self.case_x] == 'G') : #sinon, on veut aller en haut
						self.case_y-=1
						self.y=self.case_y*taille_sprite
						self.direction='haut'

					elif self.case_y<nombre_sprite_longueur-1 and self.direction != 'haut' and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'): #sinon, on va en bas
						self.case_y+=1
						self.y=self.case_y*taille_sprite
						self.direction='bas'

					elif self.case_x<nombre_sprite_largeur and self.direction != 'gauche' and (self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='G'): #sinon, on va à droite
						self.case_x+=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='droite'


				else:


					if self.case_y>0 and self.direction != 'bas' and (self.perso.niveau.structure[self.case_y -1][self.case_x] == 'v' or self.perso.niveau.structure[self.case_y -1][self.case_x] == 'p' or self.perso.niveau.structure[self.case_y -1][self.case_x] == 'G'): #sinon, on veut aller en haut
						self.case_y-=1
						self.y=self.case_y*taille_sprite
						self.direction='haut'
					elif self.case_x>=0 and  self.direction != 'droite' and (self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'v' or  self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'p' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'G'): #sinon, s'il y a du vide à gauche, on va à gauche
						self.case_x -= 1
						self.case_x= self.case_x%30
						self.x = self.case_x * taille_sprite
						self.direction='gauche'
					elif self.case_x<nombre_sprite_largeur and self.direction != 'gauche' and (self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='G'): #sinon, s'il y a du vide à droite on va à droite
						self.case_x+=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='droite'
					elif self.case_y<nombre_sprite_longueur-1 and self.direction != 'haut' and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'): #sinon, on va en bas
						self.case_y+=1
						self.y=self.case_y*taille_sprite
						self.direction='bas'



		
			elif dif_x<=0 and dif_y>=0: #le pacman est en bas à gauche du fantôme


				if abs(dif_x)>=abs(dif_y): #distance en abscisses plus importante




					if self.case_x >= 0 and self.direction!= 'droite' and (self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'v' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'p' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'G'): #on va à gauche
						self.case_x -= 1
						self.case_x= self.case_x%30
						self.x = self.case_x * taille_sprite
						self.direction='gauche'
					elif self.case_y< nombre_sprite_longueur and self.direction != 'haut' and (self.perso.niveau.structure[self.case_y +1][self.case_x] == 'v' or self.perso.niveau.structure[self.case_y +1][self.case_x] == 'p' or self.perso.niveau.structure[self.case_y +1][self.case_x] == 'G'): #on va en bas
						self.case_y+=1
						self.y=self.case_y*taille_sprite
						self.direction='bas'
					elif self.case_y>= 0 and self.direction != 'bas' and  (self.perso.niveau.structure[self.case_y -1][self.case_x] == 'v' or self.perso.niveau.structure[self.case_y -1][self.case_x] == 'p' or self.perso.niveau.structure[self.case_y -1][self.case_x] == 'G'): #on va en haut
						self.case_y-=1
						self.y=self.case_y*taille_sprite
						self.direction='haut'
					elif self.case_x<nombre_sprite_largeur and self.direction != 'gauche' and (self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='G'): #on va à droite
						self.case_x+=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='droite'


				else:  #distance en ordonnée plus importante


					if self.case_y< nombre_sprite_longueur-1 and self.direction != 'haut' and  (self.perso.niveau.structure[self.case_y +1][self.case_x] == 'v' or self.perso.niveau.structure[self.case_y +1][self.case_x] == 'p' or self.perso.niveau.structure[self.case_y +1][self.case_x] == 'G'): #on va en bas
						self.case_y+=1
						self.y=self.case_y*taille_sprite
						self.direction='bas'
					elif self.case_x >= 0 and self.direction != 'droite' and  (self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'v' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'p' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30] == 'G'): #on va à gauche
						self.case_x -= 1
						self.case_x= self.case_x%30
						self.direction='gauche'
						self.x = self.case_x * taille_sprite
					elif self.case_x < nombre_sprite_largeur and self.direction != 'gauche' and (self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='G'): #on va à droite
						self.case_x+=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='droite'
					elif self.case_y>0 and self.direction != 'bas' and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='G'): #on va en haut
						self.case_y-=1
						self.y=self.case_y*taille_sprite
						self.direction='haut'


			elif dif_y<=0 and dif_x>=0: #le pacman est en haut à droite par rapport au fantôme



				if  abs(dif_x)>abs(dif_y): #la distance à parcourir est plus grande en abscisses



					if self.case_x< nombre_sprite_largeur and self.direction != 'gauche' and (self.perso.niveau.structure[self.case_y ][(self.case_x+1)%30] == 'v' or self.perso.niveau.structure[self.case_y ][(self.case_x+1)%30] == 'p' or self.perso.niveau.structure[self.case_y ][(self.case_x+1)%30] == 'G'): #on va à droite
						self.case_x+=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='droite'
					elif self.case_y>0 and self.direction != 'bas' and  (self.perso.niveau.structure[self.case_y-1][self.case_x] == 'v' or self.perso.niveau.structure[self.case_y-1][self.case_x] == 'p' or self.perso.niveau.structure[self.case_y-1][self.case_x] == 'G'): #on va en haut
						self.case_y -= 1
						self.y = self.case_y * taille_sprite
						self.direction='haut'
					elif self.case_y <nombre_sprite_longueur-1 and self.direction != 'haut' and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'): #on va en bas
						self.case_y+=1
						self.y=self.case_y*taille_sprite
						self.direction='bas'
					elif self.case_x>=0 and self.direction != 'droite' and  (self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='G'): #on va à gauche
						self.case_x-=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='gauche'



				else:	#la distance à parcourir en ordonnée est plus grande


					if self.case_y>0 and self.direction !=  'bas' and  (self.perso.niveau.structure[self.case_y-1][self.case_x] == 'v' or self.perso.niveau.structure[self.case_y-1][self.case_x] == 'p' or self.perso.niveau.structure[self.case_y-1][self.case_x] == 'G'): #on va en haut
						self.case_y -= 1
						self.y = self.case_y * taille_sprite
						self.direction='haut'
					elif self.case_x< nombre_sprite_largeur and self.direction != 'gauche' and (self.perso.niveau.structure[self.case_y ][(self.case_x+1)%30] == 'v' or self.perso.niveau.structure[self.case_y ][(self.case_x+1)%30] == 'p' or self.perso.niveau.structure[self.case_y ][(self.case_x+1)%30] == 'G'): #on va à droite
						self.case_x+=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='droite'
					elif self.case_x>=0 and self.direction != 'droite' and (self.perso.niveau.structure[self.case_y ][(self.case_x-1)%30] == 'v' or self.perso.niveau.structure[self.case_y ][(self.case_x-1)%30] == 'p' or self.perso.niveau.structure[self.case_y ][(self.case_x-1)%30] == 'G'): #on va à gauche
						self.case_x-=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='gauche'
					elif self.case_y<nombre_sprite_longueur-1 and  self.direction != 'haut' and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'): # on va en bas
						self.case_y+=1
						self.y=self.case_y*taille_sprite
						self.direction='bas'



				
			elif dif_y>=0 and dif_x>=0: #le pacman est en bas à droite



				if abs(dif_x)>=abs(dif_y):  #la distance à parcourir est plus grande en abscisse



					if self.case_x<nombre_sprite_largeur and self.direction != 'gauche' and (self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='G'): #on va à droite
						self.case_x+=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='droite'

					elif self.case_y<nombre_sprite_longueur-1 and self.direction != 'haut' and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'): #on va en bas
						self.case_y+=1
						self.y=self.case_y*taille_sprite
						self.direction='bas'

					elif self.case_y>0 and self.direction != 'bas' and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='G'):  #on va en haut
						self.case_y-=1
						self.y=self.case_y*taille_sprite
						self.direction='haut'

					elif self.case_x>=0 and self.direction != 'droite' and (self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='G'):  #on va à gauche
						self.case_x-=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='gauche'



				else:   #la distance à parcourir est plus grande en ordonnée




					if self.case_y<nombre_sprite_longueur-1 and self.direction != 'haut' and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'): #on va en bas
						self.case_y+=1
						self.y=self.case_y*taille_sprite
						self.direction='bas'

					elif self.case_x<nombre_sprite_largeur and self.direction != 'gauche' and (self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x+1)%30]=='G'): #on va à droite
						self.case_x+=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='droite'

					elif self.case_x>=0 and self.direction != 'droite' and (self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='v' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='p' or self.perso.niveau.structure[self.case_y][(self.case_x-1)%30]=='G'): #on va à gauche
						self.case_x-=1
						self.case_x= self.case_x%30
						self.x=self.case_x*taille_sprite
						self.direction='gauche'

					elif self.case_y>0 and self.direction != 'bas' and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]=='G'): #on va en haut
						self.case_y-=1
						self.y=self.case_y*taille_sprite
						self.direction='haut'


						
	def Flee(self):
		#calcule difference en abscisse et ordonnee et s'éloigne dans la direction où l'ecart est le plus faible
		dif_x= self.perso.case_x-self.case_x
		dif_y= self.perso.case_y-self.case_y
		

		if self.case_y==15 and (self.case_x==12 or self.case_x==13 or self.case_x==14 or self.case_x==15 or self.case_x==16 or self.case_x==17):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==14 and (self.case_x==12 or self.case_x==13 or self.case_x==14 or self.case_x==15 or self.case_x==16 or self.case_x==17):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==13 and (self.case_x==12 or self.case_x==13):
			self.case_x+=1
			self.x=self.case_x*taille_sprite
			self.direction='droite'
		elif self.case_y==13 and (self.case_x==16 or self.case_x==17):
			self.case_x-=1
			self.x=self.case_x*taille_sprite
			self.direction='gauche'
		elif self.case_y==13 and (self.case_x==14 or self.case_x==15):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_y==12 and (self.case_x==14 or self.case_x==15):
			self.case_y-=1
			self.y=self.case_y*taille_sprite
			self.direction='haut'
		elif self.case_x==nombre_sprite_largeur-1 and self.direction=='droite': #le fantome est dans le passage secret, il passe de l'autre cote:
			self.case_x=0
		elif self.case_x==0 and self.direction=='gauche':
			self.case_x==nombre_sprite_largeur-1
			
		else:
			b=False
			while not b:
				if self.direction=='haut': #on va aleatoirement dans les directions possibles snas faire demi tour
					a=random.randint(1,3)
					if a==1 and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]== 'G'):
						self.case_y=(self.case_y-1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='haut'
						b=True
					elif a==2 and (self.perso.niveau.structure[self.case_y][self.case_x-1]=='v'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'p'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'G'):
						self.case_x=(self.case_x-1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='gauche'
						b=True
					elif a==3 and (self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='p' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G'):
						self.case_x=(self.case_x+1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='droite'
						b=True
				
				elif self.direction=='bas':
					a=random.randint(1,3)
					if a==1 and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'):
						self.case_y=(self.case_y+1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='bas'
						b=True
					elif a==2 and (self.perso.niveau.structure[self.case_y][self.case_x-1]=='v'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'p'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'G'):
						self.case_x=(self.case_x-1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='gauche'
						b=True
					elif a==3 and (self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='p' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G'):
						self.case_x=(self.case_x+1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='droite'
						b=True
				
				elif self.direction=='droite':
					a=random.randint(1,3)
					if a==1 and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]== 'G'):
						self.case_y=(self.case_y-1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='haut'
						b=True
					elif a==2 and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'):
						self.case_y=(self.case_y+1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='bas'
						b=True
					elif a==3 and (self.perso.niveau.structure[self.case_y][self.case_x+1]=='v' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='p' or self.perso.niveau.structure[self.case_y][self.case_x+1]=='G'):
						self.case_x=(self.case_x+1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='droite'
						b=True
						
				elif self.direction=='gauche':
					a=random.randint(1,3)
					if a==1 and (self.perso.niveau.structure[self.case_y-1][self.case_x]=='v'or self.perso.niveau.structure[self.case_y-1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y-1][self.case_x]== 'G'):
						self.case_y=(self.case_y-1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='haut'
						b=True
					elif a==2 and (self.perso.niveau.structure[self.case_y+1][self.case_x]=='v' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='p' or self.perso.niveau.structure[self.case_y+1][self.case_x]=='G'):
						self.case_y=(self.case_y+1)%nombre_sprite_largeur
						self.y=self.case_y*taille_sprite
						self.direction='bas'
						b=True
					elif a==3 and (self.perso.niveau.structure[self.case_y][self.case_x-1]=='v'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'p'or self.perso.niveau.structure[self.case_y][self.case_x-1]== 'G'):
						self.case_x=(self.case_x-1)%nombre_sprite_largeur
						self.x=self.case_x*taille_sprite
						self.direction='gauche'
						b=True