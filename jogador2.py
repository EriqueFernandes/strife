import pygame
from pygame import mixer
from pygame.locals import *

pygame.init()
mixer.init()

largura = 1200
altura = 700
relogio = pygame.time.Clock()

tela = pygame.display.set_mode((largura, altura))
fundo = pygame.transform.scale(pygame.image.load('fundo.jpg'), (largura, altura))
fonte = pygame.font.Font("fonte_letra.ttf", 100)
fonte_pontos = pygame.font.Font("fonte_letra.ttf", 40)

pygame.mixer.music.load("audios/musica.mp3")
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1, 0.0, 3000)
pancada_som = pygame.mixer.Sound("audios/pancada.mp3")
pancada_som.set_volume(0.75)
espada_som = pygame.mixer.Sound("audios/espada.mp3")
espada_som.set_volume(0.75)

cont_inicial = 3
ultima_cont = pygame.time.get_ticks()
pontos = [0,0]
final_rodada = False
round_over_cooldown = 2000

def texto(texto, fonte, cor, x, y):
    txt = fonte.render(texto, True, cor)
    tela.blit(txt, (x, y))

class Personagem():
    def __init__(self, player, x, y, som):
        self.player = player
        self.rect = pygame.Rect((x,y,100, 200))
        self.alt_pulo = 0
        self.pulo = False
        self.atacando = False
        self.attack_cooldown = 0
        self.som_ataque = som
        self.num_ataque = 0
        self.vida = True

    def movimentacao(self, alvo):
        velocidade = 10
        gravidade = 2
        x = 0
        y = 0
        self.num_ataque = 0
        key = pygame.key.get_pressed()
        
        if self.atacando == False and self.vida == True and final_rodada == False:
            if self.player == 2:
                if key[pygame.K_LEFT]:
                    x = -velocidade
                if key[pygame.K_RIGHT]:
                    x = velocidade
                if key[pygame.K_UP] and self.pulo == False:
                    self.alt_pulo = -30
                    self.pulo = True
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.ataque(alvo)
                    if key[pygame.K_KP1]:
                        self.num_ataque = 1
                    if key[pygame.K_KP2]:
                        self.num_ataque = 2

        self.alt_pulo += gravidade
        y += self.alt_pulo

        if self.rect.left + x < 0:
            x = -self.rect.left
        if self.rect.right + x > largura:
            x = largura - self.rect.right
        if self.rect.bottom + y > altura -50:
            self.alt_pulo = 0
            self.pulo = False
            y = altura -50 - self.rect.bottom

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += x
        self.rect.y += y

    def ataque(self, alvo):
        if self.attack_cooldown == 0:
            self.atacando = True
            self.som_ataque.play()
            area_ataque = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
            if area_ataque.colliderect(alvo.rect):
                print('ok') # tirar print
            pygame.draw.rect(tela, (255, 0, 0), area_ataque)

    def img_jogador(self, tela):
        pygame.draw.rect(tela, (50, 170, 50), self.rect)

jogador_1 = Personagem(1, 200, 450, pancada_som)
jogador_2 = Personagem(2, 700, 450, espada_som)

while True:

    relogio.tick(30)
    tela.blit(fundo, (0, 0))
    jogador_1.img_jogador(tela)
    jogador_2.img_jogador(tela)
    texto("P1: " + str(pontos[0]), fonte_pontos, (255, 0, 0), 50, 60)
    texto("P2: " + str(pontos[1]), fonte_pontos, (255, 0, 0), 1050, 60)

    if cont_inicial <= 0:
        jogador_2.movimentacao(jogador_1)
    else:
        texto(str(cont_inicial), fonte, (255,0,0), largura / 2, altura / 4)
        if (pygame.time.get_ticks() - ultima_cont) >= 1000:
            cont_inicial -= 1
            ultima_cont = pygame.time.get_ticks()

    if final_rodada == False:
        if jogador_1.vida == False:
            pontos[1] += 1
            final_rodada = True
            time_final_rodada = pygame.time.get_ticks()

        elif jogador_2.vida == False:
            pontos[0] += 1
            final_rodada = True
            time_final_rodada = pygame.time.get_ticks()
    else:
        texto(str('Vitória!'), fonte, (255, 0, 0), largura / 2, altura / 4)
        if pygame.time.get_ticks() - time_final_rodada > round_over_cooldown:
            final_rodada = False
            cont_inicial = 3
            jogador_1 = Personagem(1, 200, 450, pancada_som)
            jogador_2 = Personagem(2, 700, 450, espada_som)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    
    pygame.display.flip()