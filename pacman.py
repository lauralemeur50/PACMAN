#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
jeu pacman
"""

import pygame
from pygame.locals import *

from classes import *
from constantes import *

pygame.init()

#Ouverture de la fenêtre Pygame (carré : largeur = hauteur)
fenetre = pygame.display.set_mode((cote_largeur, cote_longueur))
#Icone
icone = pygame.image.load(image_icone)
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption(titre_fenetre)

#BOUCLE PRINCIPALE
continuer = 1
while continuer:	
	#Chargement et affichage de l'écran d'accueil
	accueil = pygame.image.load(image_accueil).convert()
	fenetre.blit(accueil, (0,0))

	#Rafraichissement
	pygame.display.flip()

	#On remet ces variables à 1 à chaque tour de boucle
	continuer_jeu = 1
	continuer_accueil = 1

	#BOUCLE D'ACCUEIL
	while continuer_accueil:
	
		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(30)
	
		for event in pygame.event.get():
		
			#Si l'utilisateur quitte, on met les variables 
			#de boucle à 0 pour n'en parcourir aucune et fermer
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				continuer_accueil = 0
				continuer_jeu = 0
				continuer = 0
				#Variable de choix du niveau
				choix = 0
				
			#elif event.type == KEYDOWN and event. key == K_KP1:			
				#Lancement du niveau 1
			continuer_accueil = 0	#On quitte l'accueil
			choix = 'labyrinthe'		#On définit le niveau à charger
			
			#elif event.type == KEYDOWN and event.key == K_KP2:
				#Lancement du niveau 2
				#continuer_accueil=0	
				#mettre le deuxième labyrinthe quand on l'aura
				
			
		

	#on vérifie que le joueur a bien fait un choix de niveau
	#pour ne pas charger s'il quitte
	if choix != 0:
		
		#défintion du score
		score =0
		
		#Chargement du fond
		fond = pygame.image.load(image_fond).convert()

		#Génération d'un niveau à partir d'un fichier
		niveau = Niveau(choix)
		niveau.generer()
		niveau.afficher(fenetre)
		
		
		#Création de pacman
		pacman = PACMAN("pacman_d.png", "pacman_g.png", 
		"pacman_h.png", "pacman_b.png", niveau, score)
		
		#Création du fantôme
		fantome= ghost("blinky", "normal", "blinky.png", "fantome_bleu.png", pacman)

		#affichage du score
		pygame.display.set_caption(str(pacman.score))
		

				
	#BOUCLE DE JEU
	while continuer_jeu:
	
		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(8)

	
		for event in pygame.event.get():

		
			#Si l'utilisateur quitte, on met la variable qui continue le jeu
			#ET la variable générale à 0 pour fermer la fenêtre
			if event.type == QUIT:
				continuer_jeu = 0
				continuer = 0
		
			elif event.type == KEYDOWN:
				#Si l'utilisateur presse Echap ici, on revient seulement au menu
				if event.key == K_ESCAPE:
					continuer_jeu = 0
					
				#Touches de déplacement de pacman
				elif event.key == K_RIGHT:
					pacman.deplacer('droite')
					if niveau.structure[pacman.case_y][pacman.case_x]=='p':
						pacman.eatGum('petite')
					#on affiche du vide à la place de la gomme que pacman a mangé
					niveau.structure[pacman.case_y][pacman.case_x]='v'

				elif event.key == K_LEFT:
					pacman.deplacer('gauche')
					if niveau.structure[pacman.case_y][pacman.case_x]=='p':
						pacman.eatGum('petite')
					#on affiche du vide à la place de la gomme que pacman a mangé
					niveau.structure[pacman.case_y][pacman.case_x]='v'

				elif event.key == K_UP:
					pacman.deplacer('haut')
					if niveau.structure[pacman.case_y][pacman.case_x]=='p':
						pacman.eatGum('petite')
					#on affiche du vide à la place de la gomme que pacman a mangé
					niveau.structure[pacman.case_y][pacman.case_x]='v'

				elif event.key == K_DOWN:
					pacman.deplacer('bas')	
					if niveau.structure[pacman.case_y][pacman.case_x]=='p':
						pacman.eatGum('petite')
					#on affiche du vide à la place de la gomme que pacman a mangé
					niveau.structure[pacman.case_y][pacman.case_x]='v'
					
		#Si on a appuyé sur rien, pacman continue son chemin
		pacman.deplacer('standard')


		#le fantôme se déplace
		fantome.Chasing()


		#augmentation du score si pacman a mangé une gomme
		if niveau.structure[pacman.case_y][pacman.case_x]=='p':
			pacman.eatGum('petite')

		#on affiche du vide à la place de la gomme que pacman a mangé
		niveau.structure[pacman.case_y][pacman.case_x]='v'

		#affichage du nouveau score
		pygame.display.set_caption(str(pacman.score))
		#Affichages aux nouvelles positions
		fenetre.blit(fond, (0,0))
		niveau.afficher(fenetre)
		fenetre.blit(pacman.direction, (pacman.x, pacman.y)) #pacman.direction = l'image dans la bonne direction
		fenetre.blit(fantome.image, (fantome.x, fantome.y))
		pygame.display.flip()




		#Victoire -> Retour à l'accueil
		if choix=='labyrinthe' and pacman.score== 260:
			continuer_jeu = 0
			continuer_accueil=1
