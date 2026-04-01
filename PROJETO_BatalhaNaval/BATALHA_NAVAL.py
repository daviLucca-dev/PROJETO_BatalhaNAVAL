import pygame
import sys

pygame.init()
pygame.display.set_caption("BATALHA NAVAL")

#Caminho
caminho = r"C:\Users\44840610827\Documents\DaviLucca\Lógica\PROJETO_BatalhaNaval"

#Som Background
pygame.mixer.music.load(f"{caminho}\\Song_background.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

#Som barco


qtd_coluna = 8
qtd_linha = 5

OFFSET = 40

# Tela
largura = 80 * qtd_coluna + OFFSET + 20
altura = 80 * qtd_linha + 120



tela = pygame.display.set_mode((largura, altura))
fonte = pygame.font.Font(f"{caminho}\\PressStart2P.ttf", 20)

# Fundo
fundo = pygame.image.load(f"{caminho}\\FUNDO_MAR.webp")
fundo = pygame.transform.scale(fundo, (largura, altura))
escurecimento = 80
overlay = pygame.Surface((largura, altura))
overlay.fill((0, 0, 0))
overlay.set_alpha(escurecimento)

# Imagens
navio = pygame.image.load(f"{caminho}\\navio.png")
explosao = pygame.image.load(f"{caminho}\\explosao.png")
agua = pygame.image.load(f"{caminho}\\agua.png")
erro = pygame.image.load(f"{caminho}\\erro.png")

navio = pygame.transform.scale(navio, (80, 80))
explosao = pygame.transform.scale(explosao, (80, 80))
agua = pygame.transform.scale(agua, (80, 80))
erro = pygame.transform.scale(erro, (40, 40))

#Imagem venceu
lyra_venceu = pygame.image.load(f"{caminho}\\lyra_venceu.png")
kael_venceu = pygame.image.load(f"{caminho}\\kael_venceu.png")

lyra_venceu = pygame.transform.scale(lyra_venceu, (largura, altura))
kael_venceu = pygame.transform.scale(kael_venceu, (largura, altura))

# Musica
som_explosão = pygame.mixer.Sound(f"{caminho}\\explosao.wav")
som_explosão.set_volume(0.8)
som_vitoria = pygame.mixer.Sound(f"{caminho}\\victory.wav")
som_vitoria.set_volume(1)
som_vitoria_tocando = False
som_navio = pygame.mixer.Sound(f"{caminho}\\Barco_sound.wav")
som_navio.set_volume(0.8)
som_error = pygame.mixer.Sound(f"{caminho}\\error_sound.wav")
som_error.set_volume(0.8)

# Campos
campo1 = [[0 for _ in range(qtd_coluna)] for _ in range(qtd_linha)]
campo2 = [[0 for _ in range(qtd_coluna)] for _ in range(qtd_linha)]

# Controle
estado = "jogador1"
navios = 0
jogador = 1
tempo_inicio, tempo_ataque = 0, 0

qtd_navio = 4

ataque_em_andamento = False


while True:
    tela.blit(fundo, (0, 0))
    tela.blit(overlay, (0, 0))

    for evento in pygame.event.get(): #retorna todos os eventos ocorridos
        if evento.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN: 
            x, y = pygame.mouse.get_pos()

            linha = (y - OFFSET) // 80
            coluna = (x - OFFSET) // 80

            if linha < 0 or coluna < 0:
                continue

            if linha < qtd_linha and coluna < qtd_coluna:

                if estado == "jogador1":
                    if campo1[linha][coluna] == 0:
                        campo1[linha][coluna] = 1
                        navios += 1
                        som_navio.play()

                    if navios == qtd_navio:
                        estado = "mostrar1"
                        tempo_inicio = pygame.time.get_ticks()

                elif estado == "jogador2":
                    if campo2[linha][coluna] == 0:
                        campo2[linha][coluna] = 1
                        navios += 1
                        som_navio.play()

                    if navios == qtd_navio:
                        estado = "mostrar2"
                        tempo_inicio = pygame.time.get_ticks()

                elif estado == "jogo" and not ataque_em_andamento:

                    ataque_em_andamento = True
                    tempo_ataque = pygame.time.get_ticks()

                    if jogador == 1:
                        if campo2[linha][coluna] in [2, -1]:
                            ataque_em_andamento = False
                            continue
                        if (campo2[linha][coluna] == 1):
                            campo2[linha][coluna] = 2
                            som_explosão.play()  
                        else:
                            campo2[linha][coluna] = -1
                            som_error.play()

                    else:
                        if campo1[linha][coluna] in [2, -1]:
                            ataque_em_andamento = False
                            continue
                        if (campo1[linha][coluna] == 1):
                            campo1[linha][coluna] = 2
                            som_explosão.play()   
                        else:
                            campo1[linha][coluna] = -1
                            som_error.play()

            print(f"{linha}, {coluna} ")
            

    # Números das posições
    for j in range(qtd_coluna):
        texto = fonte.render(str(j), True, (255,255,255))
        tela.blit(texto, (j * 80 + OFFSET + 30, 5))

    for i in range(qtd_linha):
        texto = fonte.render(str(i), True, (255,255,255))
        tela.blit(texto, (5, i * 80 + OFFSET + 30))

    # STATUS: qtd de navios
    rest1 =[]
    for p in campo1: #p: posição
        for item in p:
            if item == 1:
                rest1.append(item)
    rest2 =[]
    for p in campo2:
        for item in p:
            if item == 1:
                rest2.append(item)


    navios_rest1 = len(rest1)
    navios_rest2 = len(rest2)
    

    # Campo
    for i in range(qtd_linha):
        for j in range(qtd_coluna):
            x = j * 80 + OFFSET
            y = i * 80 + OFFSET

            if estado in ["jogador1", "mostrar1"]:
                valor = campo1[i][j]
            elif estado in ["jogador2", "mostrar2"]:
                valor = campo2[i][j]
            else:
                if jogador == 1:
                    valor = campo2[i][j] 
                else:
                    valor = campo1[i][j]
    
                if valor == 1:
                    valor = 0

            #define cada icone!
            #.blit desenha onde você quer
            if valor == 0:
                tela.blit(agua, (x, y))
            elif valor == 1:
                tela.blit(navio, (x, y))
            elif valor == 2:
                tela.blit(explosao, (x, y))
            elif valor == -1:
                agua_trans = agua.copy()
                agua_trans.set_alpha(100)
                tela.blit(agua_trans, (x, y))
                tela.blit(erro, (x+20, y+20))

            pygame.draw.rect(tela, (50,50,50), (x,y,80,80), 1)

    #tamanho do placar
    painel_x = 40
    painel_y = qtd_linha * 80 + 50
    painel_largura = largura - 80
    painel_altura = 60

    pygame.draw.rect(tela, (20,20,20), (painel_x, painel_y, painel_largura, painel_altura))
    pygame.draw.rect(tela, (200,200,200), (painel_x, painel_y, painel_largura, painel_altura), 2)

    #placar
    if estado == "jogo":
        fonte_pla = pygame.font.Font(f"{caminho}\\PressStart2P.ttf", 15)
        turno_txt = f"Turno: Jogador {jogador}"
        info_txt = f"J1: {navios_rest1} navios  |  J2: {navios_rest2} navios"

        tela.blit(fonte_pla.render(turno_txt, True, (255,255,0)), (painel_x + 20, painel_y + 10))
        tela.blit(fonte_pla.render(info_txt, True, (255,255,255)), (painel_x + 20, painel_y + 35))

    else:
        mensagens = {
            "jogador1": "Jogador 1 - Posicione",
            "mostrar1": "Memorize J1",
            "jogador2": "Jogador 2 - Posicione",
            "mostrar2": "Memorize J2"
        }

        msg = mensagens.get(estado, "")
        tela.blit(fonte.render(msg, True, (255,255,255)), (painel_x + 20, painel_y + 15))

    #tempo de diferença
    if estado == "mostrar1" and pygame.time.get_ticks() - tempo_inicio > 2000:
        estado = "jogador2"
        navios = 0

    if estado == "mostrar2" and pygame.time.get_ticks() - tempo_inicio > 2000:
        estado = "jogo"

    if ataque_em_andamento and pygame.time.get_ticks() - tempo_ataque > 1000:
        ataque_em_andamento = False
        if (jogador == 1):
            jogador = 2
        else:
            jogador = 1 

    #vencedor
    if estado == "jogo":
        if navios_rest2 == 0:
            pygame.mixer.music.stop()
            som_vitoria.play()
            som_vitoria_tocando = True
            estado = "fim"

        elif navios_rest1 == 0:
            pygame.mixer.music.stop()
            som_vitoria.play()
            som_vitoria_tocando = True
            estado = "fim"
        
    if estado == "fim":
        if navios_rest2 == 0:
            tela.blit(lyra_venceu)
        elif navios_rest1 == 0:
            tela.blit(kael_venceu)

    

    pygame.display.flip()
