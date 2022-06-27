from xmlrpc.client import Boolean
import pygame
import os 
pygame.font.init()


####################################################################################################

#criando a interface do jogo
LARGURA, ALTURA = 900, 500 # 2) definindo a altura e largura
JANELA = pygame.display.set_mode((LARGURA,ALTURA))#1) dentro dos parenteses é onde coloca o tamanho da janela
pygame.display.set_caption("Joguinho com PyGame")
FPS = 60 # 8) definindo a quantidade de fps do jogo
NAVE_AMARELA = pygame.image.load(os.path.join('assets','spaceship_yellow.png'))
NAVE_VERMELHA = pygame.image.load(os.path.join('assets','spaceship_red.png'))
NAVE_AMARELA_TAMANHO = pygame.transform.rotate(pygame.transform.scale(NAVE_AMARELA, (55,40)),90) # 10) definindo o tamanho 
NAVE_VERMELHA_TAMANHO = pygame.transform.rotate(pygame.transform.scale(NAVE_VERMELHA, (55,40)), 270) # 10) definindo o tamanho 
BORDER = pygame.Rect(LARGURA//2 - 5, 0, 10,ALTURA)# 12) !!!
BLACK = (0,0,0)
#new
projeteis_vel = 7
amarelo_projeteis = []
vermelho_projeteis = []
num_projeteis = 3
AMARELO_HIT = pygame.USEREVENT + 1
VERMELHO_HIT = pygame.USEREVENT + 2
projetil_azul = (0, 8, 242)
projetil_verm = (255, 3, 3)
SPACE_BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets",'universe.jpg')),(LARGURA,ALTURA))
vida_vermelho = 5
vida_amarelo = 5
fonte_letra = pygame.font.SysFont('Consolas', 40)
fonte_letra_ganhador = pygame.font.SysFont('Consolas', 100)



#####################################################################################################


#new!!
def design_da_janela(vermelha, amarela,amarelo_projeteis,vermelho_projeteis,vida_amarelo,vida_vermelho): 
    JANELA.blit(SPACE_BG,(0,0))
    #JANELA.fill((255,255,255)) # 5) colorindo a tela (dentro da main primeiro)
    pygame.draw.rect(JANELA,BLACK, BORDER) #!!!!!
    JANELA.blit(NAVE_AMARELA_TAMANHO, (amarela.x, amarela.y)) # 9) permite que a gente coloque alumas coisas na superfície do jogo // antes : (NAVE_AMARELA_TAMANHO, (300,100))
    JANELA.blit(NAVE_VERMELHA_TAMANHO,(vermelha.x, vermelha.y)) # antes : (NAVE_VERMELHA_TAMANHO,(700, 100))


    vermelho_vida_texto = fonte_letra.render("VIDA : " + str(vida_vermelho),1,(255,255,255))
    amarelo_vida_texto = fonte_letra.render("VIDA : " + str(vida_amarelo),1,(255,255,255))
    JANELA.blit(vermelho_vida_texto,(LARGURA - vermelho_vida_texto.get_width()-10,10))
    JANELA.blit(amarelo_vida_texto,(10, 10))

    for bullet in vermelho_projeteis :
        pygame.draw.rect(JANELA, projetil_verm, bullet)

    for bullet in amarelo_projeteis :
        pygame.draw.rect(JANELA, projetil_azul, bullet)


    pygame.display.update()# 6) atualizando a janela (dentro da main primeiro)

#new3
def projeteis(amarela,vermelha,vermelho_projeteis,amarelo_projeteis):
    for bullet in amarelo_projeteis :
        bullet.x += projeteis_vel
        if vermelha.colliderect(bullet):
            pygame.event.post(pygame.event.Event(VERMELHO_HIT))
            amarelo_projeteis.remove(bullet)
        elif bullet.x > LARGURA :
            amarelo_projeteis.remove(bullet)

    for bullet in vermelho_projeteis :
        bullet.x -= projeteis_vel
        if amarela.colliderect(bullet):
            pygame.event.post(pygame.event.Event(VERMELHO_HIT))
            vermelho_projeteis.remove(bullet)
        elif bullet.x < 0:
            vermelho_projeteis.remove(bullet)

def ganhador_(text):
    texto_ganhador = fonte_letra_ganhador.render(text,1,(255,255,255))
    JANELA.blit(texto_ganhador,(LARGURA//2- texto_ganhador.get_width()/2, ALTURA/2 - texto_ganhador.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
####################################################################################################

def main (): # 3) aqui nessa função onde vai ser o event loop, verificando colisões, atualizar a pontuação, ficar atualizando o jogo.
    vermelha = pygame.Rect(700,300,55,40) # para fazer a movimentação
    amarela = pygame.Rect(100,300,55,40)
 
    vida_vermelho = 5
    vida_amarelo = 5
    ganhador = ''

    frames = pygame.time.Clock() # definindo quantas atualizações por segundo
    rodando = True
    while rodando :
        frames.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False 
            #new#2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(amarelo_projeteis) < num_projeteis:
                    bullet = pygame.Rect(amarela.x + amarela.width, amarela.y + amarela.height//2, 10,5) # posição.x, posição.y, tamanho.width, tamanho.height
                    amarelo_projeteis.append(bullet)
                if event.key == pygame.K_RSHIFT and len(vermelho_projeteis)< num_projeteis:
                    bullet = pygame.Rect(vermelha.x, vermelha.y + vermelha.height//2, 10,5) # posição.x, posição.y, tamanho.width, tamanho.height
                    vermelho_projeteis.append(bullet)
            
            if event.type == VERMELHO_HIT:
                vida_vermelho -= 1
            if event.type == AMARELO_HIT:
                vida_amarelo -= 1
        if vida_amarelo <= 0:
            ganhador = "VERMELHO GANHOU"
        if vida_vermelho <= 0:
            ganhador = "AMARELO GANHOU"
        
        if ganhador != "":
            ganhador_(ganhador)
            break
        # 7) criar uma função para apenas a parte do design
        #vermelha.x += 1 
        keys_pressed = pygame.key.get_pressed() # 11) !!!
        if keys_pressed[pygame.K_a] and amarela.x - 5 > 0:
            amarela.x -= 5 # velocidade
        if keys_pressed[pygame.K_d] and amarela.x + 5 + amarela.width < BORDER.x:
            amarela.x += 5
        if keys_pressed[pygame.K_w] and amarela.y - 5 > 0:
            amarela.y -= 5
        if keys_pressed[pygame.K_s] and amarela.y + 5 + amarela.height < ALTURA - 5 :
            amarela.y += 5
        
        if keys_pressed[pygame.K_RIGHT]:
            vermelha.x += 5
        if keys_pressed[pygame.K_LEFT] and vermelha.x - 5 > BORDER.x + BORDER.width:
            vermelha.x -= 5
        if keys_pressed[pygame.K_UP] and vermelha.y - 5 > 0:
            vermelha.y -= 5
        if keys_pressed[pygame.K_DOWN] and vermelha.y + 5 + vermelha.height < ALTURA - 15 :
            vermelha.y += 5
        design_da_janela(vermelha,amarela,amarelo_projeteis,vermelho_projeteis,vida_amarelo,vida_vermelho)
        projeteis(amarela,vermelha,vermelho_projeteis,amarelo_projeteis)
              
    pygame.quit()
####################################################################################################



if __name__ == "__main__" : # 4)só vai rodar o jogo se rodar o arquivo diretamente
    main()
