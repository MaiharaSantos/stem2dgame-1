import pygame
import math
from Configuracoes import *
from Obstaculo import *
from Vida import *
from Impulsionador import *
from Tiro import *
import os
vec = pygame.math.Vector2

class Jogador():
    def __init__(self, game):
        self.x = X_CHAO
        self.y = Y_CHAO
        self.carregarImagemPersonagem(game)
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)  # retangulo de colisoes
        self.rect.center = (self.x + self.largura/2, self.y + self.altura/2)
        self.pos = vec(self.x + self.largura/2, self.y + self.altura/2)
        self.vel = vec(0.0, 0.0)
        self.acc = vec(0.0, 0.0)

    # carrega a imagem do personagem de acordo com a escolha do usuario
    def carregarImagemPersonagem(self, game):
        self.imagemF = pygame.image.load(os.path.join('Imagens', 'personagem_principal_FEC_1.png'))
        self.imagemD = pygame.image.load(os.path.join('Imagens', 'personagem_principal_DIR_1.png'))
        self.imagemE = pygame.image.load(os.path.join('Imagens', 'personagem_principal_ESQ_1.png'))
        # carregar imagens para modo invencivel
        self.imagemInvencivelF = pygame.image.load(os.path.join('Imagens', 'personagem_principal_invencivel_FEC_1.png'))
        self.imagemInvencivelD = pygame.image.load(os.path.join('Imagens', 'personagem_principal_invencivel_DIR_1.png'))
        self.imagemInvencivelE = pygame.image.load(os.path.join('Imagens', 'personagem_principal_invencivel_ESQ_1.png'))

        # vetor com as imagens
        if game.ehInvencivel == False:
            self.images = [self.imagemF, self.imagemD, self.imagemE]
            self.imagem = self.imagemE
        elif game.ehInvencivel == True:
            self.images = [self.imagemInvencivelF, self.imagemInvencivelD, self.imagemInvencivelE]
            self.imagem = self.imagemInvencivelE


    # esse metodo atualiza as posicoes do jogador para que ele pule
    def pular(self, game):
        if self.pos.y == Y_CHAO:
            self.vel.y = VELOC_INICIAL_PULO
            self.acc.y = ACE_GRAV
            if len(game.obstaculos):
                self.acc.y = 0.014* game.obstaculos[0].vel * game.obstaculos[0].vel
                self.vel.y = -2.5 * game.obstaculos[0].vel
            if len(game.inimigos):
                self.acc.y = 0.014* game.inimigos[0].vel * game.inimigos[0].vel
                self.vel.y = -2.5 * game.inimigos[0].vel

    # esse metodo faz com que o jogador dispare seu poder
    def atirar(self, game):
        game.tiros.append(Tiro(self.x + self.largura, 0.93*self.pos.y, 'A', -10 - game.dvel))


    # verifica o comando dado pelo usuario e em que estado o jogador esta (pulando, parado, se movendo lateralmente ou atirando)
    # e chama o metodo correspondente para atualizar as posicoes do jogador
    def atualizar(self, game):
        # Equações de Movimento
        dt = 1

        # Atualizar velocidade e posição do jogador
        self.vel.y += self.acc.y*dt
        self.pos += self.vel*dt
        self.rect.midbottom = self.pos

        if self.pos.y >= (Y_CHAO):
            self.pos.y = (Y_CHAO)
            self.vel.y = 0



    # desenha o jogador na tela com a imagem correspondente ao seu estado atual
    def desenhar(self, game, tela):

        # gerar efeito gradual no pulo
        if self.pos.y == (Y_CHAO):
            self.imagem = self.images[0]
        elif self.pos.y < (Y_CHAO) and self.pos.y > (0.95*Y_CHAO):
            self.imagem = self.images[1]
        else:
            self.imagem = self.images[2]
        if not tela.batalha:
            if self.pos.y == Y_CHAO and tela.time % 12 < 3:
                self.imagem = self.images[0]
            elif self.pos.y == Y_CHAO and tela.time % 12 < 6:
                self.imagem = self.images[1]
            elif self.pos.y == Y_CHAO and tela.time % 12 < 9:
                self.imagem = self.images[2]
            elif self.pos.y == Y_CHAO and tela.time % 12 < 12:
                self.imagem = self.images[1]


        game.janela.blit(self.imagem, (self.rect.left, self.rect.top))
        pygame.draw.rect(game.janela, (255, 0, 0), self.rect, 2)