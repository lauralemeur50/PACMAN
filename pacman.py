#!/usr/bin/python3
# -*- coding: Utf-8 -*

"""
jeu pacman
"""

import pygame
from pygame.locals import *
import os

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


SCORE=0#ICIIIIIII
continuer_game_over=0
continuer_accueil=1#iciii


while continuer:	
	#Chargement et affichage de l'écran d'accueil
	accueil = pygame.image.load(image_accueil).convert()
	fenetre.blit(accueil, (0,0))

	#Rafraichissement
	pygame.display.flip()

	#On remet ces variables à 1 à chaque tour de boucle
	continuer_jeu = 1


	#BOUCLE D'ACCUEIL
	while continuer_accueil:
	
		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(1)
	
		for event in pygame.event.get():
		
			#Si l'utilisateur quitte, on met les variables 
			#de boucle à 0 pour n'en parcourir aucune et fermer
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				continuer_accueil = 0
				continuer_jeu = 0
				continuer = 0
				#Variable de choix du niveau
				choix = 0
				
			elif event.type == MOUSEBUTTONDOWN and event.button == 1 and 250<event.pos[1] < 330 and 40<event.pos[0]<280:
				continuer_accueil = 0 #on quitte l'accueil
				choix= 'labyrinthe.txt' #On définit le niveau à charger
			
			
				
			
		

	#on vérifie que le joueur a bien fait un choix de niveau
	#pour ne pas charger s'il quitte
	if choix != 0:
		
		#défintion du score
		score =0
		
		#Chargement du fond
		fond = pygame.image.load(image_accueil).convert()

		#Génération d'un niveau à partir d'un fichier
		niveau = Niveau(choix)
		niveau.generer()
		niveau.afficher(fenetre)
		
		
		#Création de pacman
		pacman = PACMAN("pacman_d.png", "pacman_g.png", 
		"pacman_h.png", "pacman_b.png", niveau, score)
		
		#Création du fantôme
		fantome_blinky= ghost("blinky", 0, 10, "blinky.png", "fantome_bleu.png", pacman, 'gauche', 14, 15)
		fantome_clyde=ghost("clyde", 0, 30, "clyde.png", "fantome_bleu.png", pacman, 'gauche', 13, 15)
		fantome_inky=ghost('inky',0, 20, 'inky.png','fantome_bleu.png', pacman, 'gauche', 15, 15)
		fantome_pinky=ghost('pinky',0, 40, 'pinky.png','fantome_bleu.png',pacman,'gauche', 16, 15)

		#affichage du score
		pygame.display.set_caption(str(pacman.score))



				
	#BOUCLE DE JEU
	while continuer_jeu==1:
		continuer_accueil=0#ICIIIIIII
	
		#Limitation de vitesse de la boucle
		pygame.time.Clock().tick(5)

	
		liste_event=pygame.event.get()


		if liste_event != []:

			event=liste_event[0]

		
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
						pacman.eatGum()

					elif niveau.structure[pacman.case_y][pacman.case_x]=='G':
						pacman.eatGum()

						fantome_blinky.Blue()
						fantome_clyde.Blue()
						fantome_inky.Blue()
						fantome_pinky.Blue()


						 # Si pacman se trouve sur la meme case qu'un fantome normal  --> game over

					if (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1


						# si pacman se trouve en décalé d'un fantome normal et qu'il se croise --> game over

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche) or (fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche ) or (fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='droite ' and pacman.direction==pacman.gauche) or (fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite' and pacman.direction==pacman.gauche)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite) or (fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite ) or (fantome_inky.case_x == pacman.case_x+11 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='gauche ' and pacman.direction==pacman.droite) or (fantome_clyde.case_x == pacman.case_x+11 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche' and pacman.direction==pacman.droite)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas ' and pacman.direction==pacman.haut) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas' and pacman.direction==pacman.haut)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut ' and pacman.direction==pacman.bas) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y+1 and fantome_clyde.direction=='haut' and pacman.direction==pacman.bas)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1



					# si pacman se trouve sur la meme case qu'un fantome bleu --> il le mange

					if ((fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y):

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					# si pacman se trouve en décalé d'un fantome bleu et qu'ils se croisent --> il le mange

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite'  and pacman.direction==pacman.gauche:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x+1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche'  and pacman.direction==pacman.droite:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas'  and pacman.direction==pacman.haut:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y+1 == pacman.case_y and fantome_clyde.direction=='haut'  and pacman.direction==pacman.bas:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite


					if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					if (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					if (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x+1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite		


					#on affiche du vide à la place de la gomme que pacman a mangé
					niveau.structure[pacman.case_y][pacman.case_x]='v'

				elif event.key == K_LEFT:
					pacman.deplacer('gauche')
					if niveau.structure[pacman.case_y][pacman.case_x]=='p':
						pacman.eatGum()

					elif niveau.structure[pacman.case_y][pacman.case_x]=='G':
						pacman.eatGum()

						fantome_blinky.Blue()
						fantome_clyde.Blue()
						fantome_inky.Blue()
						fantome_pinky.Blue()

					if (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche) or (fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche ) or (fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='droite ' and pacman.direction==pacman.gauche) or (fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite' and pacman.direction==pacman.gauche)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite) or (fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite ) or (fantome_inky.case_x == pacman.case_x+11 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='gauche ' and pacman.direction==pacman.droite) or (fantome_clyde.case_x == pacman.case_x+11 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche' and pacman.direction==pacman.droite)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas ' and pacman.direction==pacman.haut) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas' and pacman.direction==pacman.haut)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut ' and pacman.direction==pacman.bas) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y+1 and fantome_clyde.direction=='haut' and pacman.direction==pacman.bas)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					if (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite'  and pacman.direction==pacman.gauche:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x+1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche'  and pacman.direction==pacman.droite:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas'  and pacman.direction==pacman.haut:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y+1 == pacman.case_y and fantome_clyde.direction=='haut'  and pacman.direction==pacman.bas:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite


					if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					if (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					if (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x+1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite	

					#on affiche du vide à la place de la gomme que pacman a mangé
					niveau.structure[pacman.case_y][pacman.case_x]='v'

				elif event.key == K_UP:
					pacman.deplacer('haut')
					if niveau.structure[pacman.case_y][pacman.case_x]=='p':
						pacman.eatGum()

					elif niveau.structure[pacman.case_y][pacman.case_x]=='G':
						pacman.eatGum()

						fantome_blinky.Blue()
						fantome_clyde.Blue()
						fantome_inky.Blue()
						fantome_pinky.Blue()

					if (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche) or (fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche ) or (fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='droite ' and pacman.direction==pacman.gauche) or (fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite' and pacman.direction==pacman.gauche)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite) or (fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite ) or (fantome_inky.case_x == pacman.case_x+11 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='gauche ' and pacman.direction==pacman.droite) or (fantome_clyde.case_x == pacman.case_x+11 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche' and pacman.direction==pacman.droite)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas ' and pacman.direction==pacman.haut) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas' and pacman.direction==pacman.haut)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut ' and pacman.direction==pacman.bas) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y+1 and fantome_clyde.direction=='haut' and pacman.direction==pacman.bas)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					if (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite'  and pacman.direction==pacman.gauche:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x+1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche'  and pacman.direction==pacman.droite:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas'  and pacman.direction==pacman.haut:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y+1 == pacman.case_y and fantome_clyde.direction=='haut'  and pacman.direction==pacman.bas:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite


					if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					if (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					if (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x+1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite	


						#on affiche du vide à la place de la gomme que pacman a mangé
					niveau.structure[pacman.case_y][pacman.case_x]='v'

				elif event.key == K_DOWN:
					pacman.deplacer('bas')	
					if niveau.structure[pacman.case_y][pacman.case_x]=='p':
						pacman.eatGum()

					elif niveau.structure[pacman.case_y][pacman.case_x]=='G':
						pacman.eatGum()

						fantome_blinky.Blue()
						fantome_clyde.Blue()
						fantome_inky.Blue()
						fantome_pinky.Blue()


					if (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche) or (fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche ) or (fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='droite ' and pacman.direction==pacman.gauche) or (fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite' and pacman.direction==pacman.gauche)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite) or (fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite ) or (fantome_inky.case_x == pacman.case_x+11 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='gauche ' and pacman.direction==pacman.droite) or (fantome_clyde.case_x == pacman.case_x+11 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche' and pacman.direction==pacman.droite)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas ' and pacman.direction==pacman.haut) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas' and pacman.direction==pacman.haut)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut ' and pacman.direction==pacman.bas) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y+1 and fantome_clyde.direction=='haut' and pacman.direction==pacman.bas)):

						SCORE=pacman.score
						game_over = pygame.image.load('calque_game_over.png').convert_alpha()
						fenetre.blit(game_over, (61,130))
						pygame.display.set_caption(str(SCORE))
						pygame.display.flip()
						continuer_jeu=0
						continuer_accueil=0
						continuer_game_over=1

					if (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite'  and pacman.direction==pacman.gauche:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x+1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche'  and pacman.direction==pacman.droite:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas'  and pacman.direction==pacman.haut:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite

					elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y+1 == pacman.case_y and fantome_clyde.direction=='haut'  and pacman.direction==pacman.bas:

						fantome_clyde.case_x=13
						fantome_clyde.case_y=15
						fantome_clyde.decompte_bleu=0
						fantome_clyde.decompte=40
						fantome_clyde.x=fantome_clyde.case_x*taille_sprite
						fantome_clyde.y=fantome_clyde.case_y*taille_sprite


					if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_blinky.case_x=14
						fantome_blinky.case_y=15
						fantome_blinky.decompte_bleu=0
						fantome_blinky.decompte=40
						fantome_blinky.x=fantome_blinky.case_x*taille_sprite
						fantome_blinky.y=fantome_blinky.case_y*taille_sprite

					if (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_pinky.case_x=15
						fantome_pinky.case_y=15
						fantome_pinky.decompte_bleu=0
						fantome_pinky.decompte=40
						fantome_pinky.x=fantome_pinky.case_x*taille_sprite
						fantome_pinky.y=fantome_pinky.case_y*taille_sprite

					if (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='droite' and pacman.direction==pacman.gauche:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x+1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='gauche' and pacman.direction==pacman.droite:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas' and pacman.direction==pacman.haut:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite

					elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut' and pacman.direction==pacman.bas:

						fantome_inky.case_x=16
						fantome_inky.case_y=15
						fantome_inky.decompte_bleu=0
						fantome_inky.decompte=40
						fantome_inky.x=fantome_inky.case_x*taille_sprite
						fantome_inky.y=fantome_inky.case_y*taille_sprite	




					#on affiche du vide à la place de la gomme que pacman a mangé
					niveau.structure[pacman.case_y][pacman.case_x]='v'
					
		

		pacman.deplacer('standard')






#Si pacman rencontre un fantôme 

		if (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y)):

			SCORE=pacman.score
			game_over = pygame.image.load('calque_game_over.png').convert_alpha()
			fenetre.blit(game_over, (61,130))
			pygame.display.set_caption(str(SCORE))
			pygame.display.flip()
			continuer_jeu=0
			continuer_accueil=0
			continuer_game_over=1

		elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche) or (fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche ) or (fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='droite ' and pacman.direction==pacman.gauche) or (fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite' and pacman.direction==pacman.gauche)):

			SCORE=pacman.score
			game_over = pygame.image.load('calque_game_over.png').convert_alpha()
			fenetre.blit(game_over, (61,130))
			pygame.display.set_caption(str(SCORE))
			pygame.display.flip()
			continuer_jeu=0
			continuer_accueil=0
			continuer_game_over=1

		elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite) or (fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite ) or (fantome_inky.case_x == pacman.case_x+11 and fantome_inky.case_y == pacman.case_y and fantome_inky.direction=='gauche ' and pacman.direction==pacman.droite) or (fantome_clyde.case_x == pacman.case_x+11 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche' and pacman.direction==pacman.droite)):

			SCORE=pacman.score
			game_over = pygame.image.load('calque_game_over.png').convert_alpha()
			fenetre.blit(game_over, (61,130))
			pygame.display.set_caption(str(SCORE))
			pygame.display.flip()
			continuer_jeu=0
			continuer_accueil=0
			continuer_game_over=1

		elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas ' and pacman.direction==pacman.haut) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas' and pacman.direction==pacman.haut)):

			SCORE=pacman.score
			game_over = pygame.image.load('calque_game_over.png').convert_alpha()
			fenetre.blit(game_over, (61,130))
			pygame.display.set_caption(str(SCORE))
			pygame.display.flip()
			continuer_jeu=0
			continuer_accueil=0
			continuer_game_over=1

		elif (fantome_clyde.decompte_bleu == 0) and ((fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas) or (fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas ) or (fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut ' and pacman.direction==pacman.bas) or (fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y+1 and fantome_clyde.direction=='haut' and pacman.direction==pacman.bas)):

			SCORE=pacman.score
			game_over = pygame.image.load('calque_game_over.png').convert_alpha()
			fenetre.blit(game_over, (61,130))
			pygame.display.set_caption(str(SCORE))
			pygame.display.flip()
			continuer_jeu=0
			continuer_accueil=0
			continuer_game_over=1

		if (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y:

			fantome_clyde.case_x=13
			fantome_clyde.case_y=15
			fantome_clyde.decompte_bleu=0
			fantome_clyde.decompte=40
			fantome_clyde.x=fantome_clyde.case_x*taille_sprite
			fantome_clyde.y=fantome_clyde.case_y*taille_sprite

		elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x-1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='droite'  and pacman.direction==pacman.gauche:

			fantome_clyde.case_x=13
			fantome_clyde.case_y=15
			fantome_clyde.decompte_bleu=0
			fantome_clyde.decompte=40
			fantome_clyde.x=fantome_clyde.case_x*taille_sprite
			fantome_clyde.y=fantome_clyde.case_y*taille_sprite

		elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x+1 and fantome_clyde.case_y == pacman.case_y and fantome_clyde.direction=='gauche'  and pacman.direction==pacman.droite:

			fantome_clyde.case_x=13
			fantome_clyde.case_y=15
			fantome_clyde.decompte_bleu=0
			fantome_clyde.decompte=40
			fantome_clyde.x=fantome_clyde.case_x*taille_sprite
			fantome_clyde.y=fantome_clyde.case_y*taille_sprite

		elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y == pacman.case_y-1 and fantome_clyde.direction=='bas'  and pacman.direction==pacman.haut:

			fantome_clyde.case_x=13
			fantome_clyde.case_y=15
			fantome_clyde.decompte_bleu=0
			fantome_clyde.decompte=40
			fantome_clyde.x=fantome_clyde.case_x*taille_sprite
			fantome_clyde.y=fantome_clyde.case_y*taille_sprite

		elif (fantome_clyde.decompte_bleu >0 ) and fantome_clyde.case_x == pacman.case_x and fantome_clyde.case_y+1 == pacman.case_y and fantome_clyde.direction=='haut'  and pacman.direction==pacman.bas:

			fantome_clyde.case_x=13
			fantome_clyde.case_y=15
			fantome_clyde.decompte_bleu=0
			fantome_clyde.decompte=40
			fantome_clyde.x=fantome_clyde.case_x*taille_sprite
			fantome_clyde.y=fantome_clyde.case_y*taille_sprite


		if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y:

			fantome_blinky.case_x=14
			fantome_blinky.case_y=15
			fantome_blinky.decompte_bleu=0
			fantome_blinky.decompte=40
			fantome_blinky.x=fantome_blinky.case_x*taille_sprite
			fantome_blinky.y=fantome_blinky.case_y*taille_sprite

		if (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x-1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='droite' and pacman.direction==pacman.gauche:

			fantome_blinky.case_x=14
			fantome_blinky.case_y=15
			fantome_blinky.decompte_bleu=0
			fantome_blinky.decompte=40
			fantome_blinky.x=fantome_blinky.case_x*taille_sprite
			fantome_blinky.y=fantome_blinky.case_y*taille_sprite

		elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x+1 and fantome_blinky.case_y == pacman.case_y and fantome_blinky.direction=='gauche' and pacman.direction==pacman.droite:

			fantome_blinky.case_x=14
			fantome_blinky.case_y=15
			fantome_blinky.decompte_bleu=0
			fantome_blinky.decompte=40
			fantome_blinky.x=fantome_blinky.case_x*taille_sprite
			fantome_blinky.y=fantome_blinky.case_y*taille_sprite

		elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y-1 and fantome_blinky.direction=='bas' and pacman.direction==pacman.haut:

			fantome_blinky.case_x=14
			fantome_blinky.case_y=15
			fantome_blinky.decompte_bleu=0
			fantome_blinky.decompte=40
			fantome_blinky.x=fantome_blinky.case_x*taille_sprite
			fantome_blinky.y=fantome_blinky.case_y*taille_sprite

		elif (fantome_blinky.decompte_bleu >0 ) and fantome_blinky.case_x == pacman.case_x and fantome_blinky.case_y == pacman.case_y+1 and fantome_blinky.direction=='haut' and pacman.direction==pacman.bas:

			fantome_blinky.case_x=14
			fantome_blinky.case_y=15
			fantome_blinky.decompte_bleu=0
			fantome_blinky.decompte=40
			fantome_blinky.x=fantome_blinky.case_x*taille_sprite
			fantome_blinky.y=fantome_blinky.case_y*taille_sprite

		if (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y:

			fantome_pinky.case_x=15
			fantome_pinky.case_y=15
			fantome_pinky.decompte_bleu=0
			fantome_pinky.decompte=40
			fantome_pinky.x=fantome_pinky.case_x*taille_sprite
			fantome_pinky.y=fantome_pinky.case_y*taille_sprite

		elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x-1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='droite' and pacman.direction==pacman.gauche:

			fantome_pinky.case_x=15
			fantome_pinky.case_y=15
			fantome_pinky.decompte_bleu=0
			fantome_pinky.decompte=40
			fantome_pinky.x=fantome_pinky.case_x*taille_sprite
			fantome_pinky.y=fantome_pinky.case_y*taille_sprite

		elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x+1 and fantome_pinky.case_y == pacman.case_y and fantome_pinky.direction=='gauche' and pacman.direction==pacman.droite:

			fantome_pinky.case_x=15
			fantome_pinky.case_y=15
			fantome_pinky.decompte_bleu=0
			fantome_pinky.decompte=40
			fantome_pinky.x=fantome_pinky.case_x*taille_sprite
			fantome_pinky.y=fantome_pinky.case_y*taille_sprite

		elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y-1 and fantome_pinky.direction=='bas' and pacman.direction==pacman.haut:

			fantome_pinky.case_x=15
			fantome_pinky.case_y=15
			fantome_pinky.decompte_bleu=0
			fantome_pinky.decompte=40
			fantome_pinky.x=fantome_pinky.case_x*taille_sprite
			fantome_pinky.y=fantome_pinky.case_y*taille_sprite

		elif (fantome_pinky.decompte_bleu >0 ) and fantome_pinky.case_x == pacman.case_x and fantome_pinky.case_y == pacman.case_y+1 and fantome_pinky.direction=='haut' and pacman.direction==pacman.bas:

			fantome_pinky.case_x=15
			fantome_pinky.case_y=15
			fantome_pinky.decompte_bleu=0
			fantome_pinky.decompte=40
			fantome_pinky.x=fantome_pinky.case_x*taille_sprite
			fantome_pinky.y=fantome_pinky.case_y*taille_sprite

		if (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y:

			fantome_inky.case_x=16
			fantome_inky.case_y=15
			fantome_inky.decompte_bleu=0
			fantome_inky.decompte=40
			fantome_inky.x=fantome_inky.case_x*taille_sprite
			fantome_inky.y=fantome_inky.case_y*taille_sprite

		elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x-1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='droite' and pacman.direction==pacman.gauche:

			fantome_inky.case_x=16
			fantome_inky.case_y=15
			fantome_inky.decompte_bleu=0
			fantome_inky.decompte=40
			fantome_inky.x=fantome_inky.case_x*taille_sprite
			fantome_inky.y=fantome_inky.case_y*taille_sprite

		elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x+1 and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='gauche' and pacman.direction==pacman.droite:

			fantome_inky.case_x=16
			fantome_inky.case_y=15
			fantome_inky.decompte_bleu=0
			fantome_inky.decompte=40
			fantome_inky.x=fantome_inky.case_x*taille_sprite
			fantome_inky.y=fantome_inky.case_y*taille_sprite

		elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y-1 and fantome_inky.direction=='bas' and pacman.direction==pacman.haut:

			fantome_inky.case_x=16
			fantome_inky.case_y=15
			fantome_inky.decompte_bleu=0
			fantome_inky.decompte=40
			fantome_inky.x=fantome_inky.case_x*taille_sprite
			fantome_inky.y=fantome_inky.case_y*taille_sprite

		elif (fantome_inky.decompte_bleu >0 ) and fantome_inky.case_x == pacman.case_x and fantome_inky.case_y == pacman.case_y+1 and fantome_inky.direction=='haut' and pacman.direction==pacman.bas:

			fantome_inky.case_x=16
			fantome_inky.case_y=15
			fantome_inky.decompte_bleu=0
			fantome_inky.decompte=40
			fantome_inky.x=fantome_inky.case_x*taille_sprite
			fantome_inky.y=fantome_inky.case_y*taille_sprite	



		#augmentation du score si pacman a mangé une gomme
		if niveau.structure[pacman.case_y][pacman.case_x]=='p':
			pacman.eatGum()


		#passage au mode bleu si pacman mange une grosse gomme
		if niveau.structure[pacman.case_y][pacman.case_x]=='G':

			fantome_blinky.Blue()
			fantome_clyde.Blue()
			fantome_inky.Blue()
			fantome_pinky.Blue()
		
		#sdéplacement du fantôme, en mode bleu dans le if, en mode normal dans le else
		if fantome_clyde.decompte_bleu>0:
			if (fantome_clyde.decompte_bleu % 2 ==0):
				fantome_clyde.Flee()
			fantome_clyde.decompte_bleu-=1

		elif fantome_clyde.decompte ==0:
			fantome_clyde.Chasing_clyde()

		else:
			fantome_clyde.decompte-=1
			
		if fantome_blinky.decompte_bleu>0:
			if (fantome_blinky.decompte_bleu % 2 ==0):
				fantome_blinky.Flee()
			fantome_blinky.decompte_bleu-=1

		elif fantome_blinky.decompte==0:
			fantome_blinky.Chasing_Blinky()
			
		else:
			fantome_blinky.decompte-=1

		if fantome_inky.decompte_bleu>0:
			if (fantome_inky.decompte_bleu % 2 ==0):
				fantome_inky.Flee()
			fantome_inky.decompte_bleu-=1

		elif fantome_inky.decompte==0:
			fantome_inky.Chasing_inky()

		else:
			fantome_inky.decompte-=1


		if fantome_pinky.decompte_bleu>0:
			if (fantome_pinky.decompte_bleu % 2 ==0):
				fantome_pinky.Flee()
			fantome_pinky.decompte_bleu-=1


		elif fantome_pinky.decompte==0:
			fantome_pinky.Chasing_pinky()

		else:
			fantome_pinky.decompte-=1





		

		#on affiche du vide à la place de la gomme que pacman a mangé
		niveau.structure[pacman.case_y][pacman.case_x]='v'

		#affichage du nouveau score
		pygame.display.set_caption(str(pacman.score))
		#Affichages aux nouvelles positions
		fenetre.blit(fond, (0,0))
		niveau.afficher(fenetre)
		fenetre.blit(pacman.direction, (pacman.x, pacman.y)) #pacman.direction = l'image dans la bonne direction
		# si bleu, afficher image bleue

		if fantome_blinky.decompte_bleu>1:
			fenetre.blit(fantome_blinky.bleu, (fantome_blinky.x, fantome_blinky.y))
			
		else:
			fenetre.blit(fantome_blinky.image, (fantome_blinky.x, fantome_blinky.y))

		if fantome_clyde.decompte_bleu>1:
			fenetre.blit(fantome_clyde.bleu, (fantome_clyde.x, fantome_clyde.y))
		else:
			fenetre.blit(fantome_clyde.image, (fantome_clyde.x, fantome_clyde.y))

		if fantome_inky.decompte_bleu>1:
			fenetre.blit(fantome_inky.bleu, (fantome_inky.x, fantome_inky.y))
		else:
			
			fenetre.blit(fantome_inky.image, (fantome_inky.x, fantome_inky.y))
		pygame.display.flip()

		if fantome_pinky.decompte_bleu>1:
			fenetre.blit(fantome_pinky.bleu, (fantome_pinky.x, fantome_pinky.y))
		else:
			fenetre.blit(fantome_pinky.image, (fantome_pinky.x, fantome_pinky.y))
		pygame.display.flip()




		#Victoire: on a mangé tout le labyrinthe -> Retour à l'accueil
		niveau.victoire()
		if niveau.victoire==True:
			#afficher score
			continuer_jeu = 0
			continuer_accueil=1

	#BOUCLE DE GAME OVER #iciiii
	while continuer_game_over==1:
			game_over = pygame.image.load('calque_game_over.png').convert_alpha()
			fenetre.blit(game_over, (61,130))
			pygame.display.set_caption(str(SCORE))
			pygame.display.flip()
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					continuer_game_over=0
					continuer_accueil=1
