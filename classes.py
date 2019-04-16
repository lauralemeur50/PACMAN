"""Classes du jeu de Labyrinthe Donkey Kong"""

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
		"""Méthode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyée par generer()"""
		#Chargement des images (seule celle d'arrivée contient de la transparence)
		mur = pygame.image.load(image_mur).convert()
		depart = pygame.image.load(image_depart).convert()
		
		#On parcourt la liste du niveau
		num_ligne = 0
		for ligne in self.structure:
			#On parcourt les listes de lignes
			num_case = 0
			for sprite in ligne:
				#On calcule la position réelle en pixels
				x = num_case * taille_sprite
				y = num_ligne * taille_sprite
				if sprite == 'm':		   #m = Mur
					fenetre.blit(mur, (x,y))
				elif sprite == 'd':		   #d = Départ
					fenetre.blit(depart, (x,y))
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
		self.rond= pygame.image.load(rond).convert_alpha()
		#Position du personnage en cases et en pixels
		self.case_x = 8
		self.case_y = 14
		self.x = 8*taille_sprite*10
		self.y = 14*taille_sprite*10
		#Direction par défaut
		self.direction = self.rond
		#Niveau dans lequel le personnage se trouve 
		self.niveau = niveau
	
	
	def deplacer(self, direction):
		"""Methode permettant de déplacer le personnage"""
		
		#Déplacement vers la droite
		if direction == 'droite':
			#Image dans la bonne direction
			self.direction = self.droite
			#Pour ne pas dépasser l'écran
			if  self.case_x < (nombre_sprite_cote - 1)  and self.niveau.structure[self.case_y][self.case_x+1] != 'm':
					#Déplacement d'une case
					self.case_x += 1
					#Calcul de la position "réelle" en pixel
					self.x = self.case_x * taille_sprite *10
					#Affichages aux nouvelles positions
					fenetre.blit(fond, (0,0))
					niveau.afficher(fenetre)
					fenetre.blit(pacman.direction, (pacman.x, pacman.y)) #pacman.direction = l'image dans la bonne direction
					pygame.display.flip()
					

		
		#Déplacement vers la gauche
		if direction == 'gauche':
			self.direction = self.gauche
			if self.case_x > 0 and  self.niveau.structure[self.case_y][self.case_x-1] != 'm':
					self.case_x -= 1
					self.x = self.case_x * taille_sprite *10
					#Affichages aux nouvelles positions
					fenetre.blit(fond, (0,0))
					niveau.afficher(fenetre)
					fenetre.blit(pacman.direction, (pacman.x, pacman.y)) #pacman.direction = l'image dans la bonne direction
					pygame.display.flip()

		
		#Déplacement vers le haut
		if direction == 'haut':
			self.direction = self.haut
			if self.case_y > 0 and self.niveau.structure[self.case_y-1][self.case_x] != 'm':
					self.case_y -= 1
					self.y = self.case_y * taille_sprite *10
					#Affichages aux nouvelles positions
					fenetre.blit(fond, (0,0))
					niveau.afficher(fenetre)
					fenetre.blit(pacman.direction, (pacman.x, pacman.y)) #pacman.direction = l'image dans la bonne direction
					pygame.display.flip()

		
		#Déplacement vers le bas
		if direction == 'bas':
			self.direction = self.bas
			if self.case_y < (nombre_sprite_cote - 1) and self.niveau.structure[self.case_y+1][self.case_x] != 'm':
					self.case_y += 1
					self.y = self.case_y * taille_sprite *10
					#Affichages aux nouvelles positions
					fenetre.blit(fond, (0,0))
					niveau.afficher(fenetre)
					fenetre.blit(pacman.direction, (pacman.x, pacman.y)) #pacman.direction = l'image dans la bonne direction
					pygame.display.flip()
					
					
		#déplacement standard
		if direction== 'standard':
			if self.direction== self.bas and self.case_y < (nombre_sprite_cote - 1) and self.niveau.structure[self.case_y+1][self.case_x] != 'm':
				self.case_y += 1
				self.y = self.case_y * taille_sprite *10
			elif self.direction==self.haut and self.case_y > 0 and self.niveau.structure[self.case_y-1][self.case_x] != 'm':
				self.case_y -= 1
				self.y = self.case_y * taille_sprite *10
			elif self.direction== self.gauche and self.case_x > 0 and  self.niveau.structure[self.case_y][self.case_x-1] != 'm':
				self.case_x -= 1
				self.x = self.case_x * taille_sprite *10
			elif self.direction==self.droite and self.case_x < (nombre_sprite_cote - 1)  and self.niveau.structure[self.case_y][self.case_x+1] != 'm':
				self.case_x += 1
				self.x = self.case_x * taille_sprite *10





