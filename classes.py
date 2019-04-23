"""Classes du jeu de pacman"""

import pygame
from pygame.locals import * 
from constantes import *

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
				elif sprite=='v':
					fenetre.blit(vide, (x,y))
				num_case += 1
			num_ligne += 1

			
			
			
			
class Perso:
	"""Classe permettant de créer un personnage"""
	def __init__(self, droite, gauche, haut, bas, niveau):
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

	
	
	def deplacer(self, direction):
		"""Methode permettant de déplacer le personnage"""
		
		#Déplacement vers la droite
		if direction == 'droite':
			#Pour ne pas dépasser l'écran, s'arrêter si on rencontre un coin bas gauche, un coin haut gauche ou une colonne.
			if  self.case_x < (nombre_sprite_largeur - 1)  and self.niveau.structure[self.case_y][self.case_x+1] != 'C' and self.niveau.structure[self.case_y][self.case_x+1] != '1' and self.niveau.structure[self.case_y][self.case_x+1] != '2':
				#Image dans la bonne direction
				self.direction = self.droite
				#Déplacement d'une case
				self.case_x+=1
				#Calcul de la position "réelle" en pixel
				self.x = self.case_x * taille_sprite
		
		#Déplacement vers la gauche
		if direction == 'gauche':
			if self.case_x > 0 and  self.niveau.structure[self.case_y][self.case_x-1] != 'C' and  self.niveau.structure[self.case_y][self.case_x-1] != '3' and  self.niveau.structure[self.case_y][self.case_x-1] != '4':
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
			elif self.direction==self.droite and self.case_x < (nombre_sprite_largeur - 1)  and self.niveau.structure[self.case_y][self.case_x+1] != 'C' and self.niveau.structure[self.case_y][self.case_x+1] != '1' and self.niveau.structure[self.case_y][self.case_x+1] != '2':
				self.case_x += 1
				self.x = self.case_x * taille_sprite 

