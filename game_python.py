from graphics import *
import pygame
import random

# Cria a janela inicial
win = GraphWin("IMHOTEP", 800, 600)

pygame.init()
pygame.font.init()
pygame.mixer.init() # Start nos sons

#pasta que contem os sons
s = 'sound'

#lista de Sons
hit = pygame.mixer.Sound(os.path.join(s, 'hit.wav'))
blockbreak = pygame.mixer.Sound(os.path.join(s, 'break.wav'))
go = pygame.mixer.Sound(os.path.join(s, 'gameover.wav'))
select = pygame.mixer.Sound(os.path.join(s, 'select.wav'))
music = pygame.mixer.music.load(os.path.join(s, 'maintheme.wav'))

#play background
pygame.mixer.music.play(-1)

# --------tela_start------------------------------------
win.setBackground(color_rgb(255, 255, 140))

yell = True
for inc_lin in range(0, 250, 25):
    for inc in range(0, 800, 40):
        ret = Rectangle(Point(0 + inc, 0 + inc_lin), Point(39 + inc, 24 + inc_lin))
        if yell:
            ret.setFill(color_rgb(255, 128, 0))
            yell = False
        else:
            ret.setFill(color_rgb(255, 153, 51))
            yell = True
        ret.draw(win)
    yell = not yell

tex1 = Text(Point(400, 350), 'IMHOTEP')
tex1.setTextColor("orange red")
tex1.setStyle("bold")
tex1.setSize(36)
tex1.draw(win)

barrinha = Line(Point(300, 530), Point(500, 530))
barrinha.setFill(color_rgb(50, 49, 45))
barrinha.setWidth(25)
barrinha.draw(win)

circlin = Circle(Point(350, 500), 15)
circlin.setFill(color_rgb(0, 0, 0))
circlin.draw(win)

text_botao = Text(Point(400, 532), 'START !')
text_botao.setTextColor("red")
text_botao.setStyle("bold")
text_botao.setSize(16)
text_botao.draw(win)

while True:
    ponto = win.getMouse()
    x = ponto.getX()
    y = ponto.getY()
    if x >= 250 and x <= 550 and y >= 500 and y <= 550:
        pygame.mixer.Sound.play(select)
        break

tex1.undraw()
barrinha.undraw()
circlin.undraw()
text_botao.undraw()

# ---------------tela_nome---------------------------------

quadrad = Rectangle(Point(0, 0), Point(800, 600))
quadrad.setFill(color_rgb(255, 255, 140))
quadrad.draw(win)

t0 = Text(Point(400, 125), 'IMHOTEP')
t0.setTextColor('orange red')
t0.setStyle('bold')
t0.setSize(30)
t0.draw(win)

l1 = Line(Point(0, 200), Point(800, 200))
l1.setWidth(3)
l1.draw(win)

l2 = Line(Point(0, 400), Point(800, 400))
l2.setWidth(3)
l2.draw(win)

t1 = Text(Point(150, 300), 'Digite seu nome :')
t1.setStyle('bold')
t1.setSize(18)
t1.draw(win)

nome = Entry(Point(400, 300), 30)
nome.setFill('white')
nome.setTextColor('black')
nome.setStyle('bold italic')
nome.draw(win)

botao = Rectangle(Point(350, 325), Point(450, 375))
botao.setFill('light gray')
botao.draw(win)

tex_botao = Text(Point(401, 352), 'PLAY !')
tex_botao.setStyle('bold')
tex_botao.draw(win)

while True:
    ponto = win.getMouse()
    x = ponto.getX()
    y = ponto.getY()
    if x >= 350 and x <= 450 and y >= 325 and y <= 375:
        pygame.mixer.Sound.play(select)
        break

print(t1)
print(nome.getText())

NAME = nome.getText()

nome.undraw()
tex_botao.undraw()
botao.undraw()
t1.undraw()
l1.undraw()
l2.undraw()
t0.undraw()

name = Text(Point(100, 575), "Nome: " + NAME)
name.setStyle('bold italic')
name.setSize(16)
name.draw(win)

# --------------------início do game--------------------------------------------

# Design
linha_superior = Line(Point(0, 40), Point(800, 40))
linha_superior.setWidth(10)
linha_superior.setFill(color_rgb(0, 0, 0))
linha_superior.draw(win)
# Design
linha_inferior = Line(Point(0, 550), Point(800, 550))
linha_inferior.setWidth(3)
linha_inferior.setFill(color_rgb(0, 0, 0))
linha_inferior.draw(win)

# Ball Design
col = 390
lin = 300
raio = 15
circulo = Circle(Point(col, lin), raio)
circulo.setFill(color_rgb(100, 100, 100))
circulo.draw(win)

# Gamescore UI
pts = 0
pontos = Text(Point(395, 575), "Pontos: " + str(pts))
pontos.setStyle('bold')
pontos.setSize(18)
pontos.draw(win)

# Design da barra (antes do primeiro input)
col_ini = 340
tamanho = 100
barra = Line(Point(col_ini, 530), Point(col_ini + tamanho, 530))
barra.setFill(color_rgb(50, 49, 45))
barra.setWidth(10)
barra.draw(win)

# Variaveis no Startup
jog = ["0", "0", "0", "0"]
reseting = False
comecar = False
restart = False
level = 1
broken = 0
difficulty = 8 - level
barramento = 7.5
xbrick = 5
ybrick = 60
bricks = {}
scopex_top_left = []
scopey_top_left = []
scopex_bottom_right = []
scopey_bottom_right = []
clock = .035  # Tempo entre uma atualizacao e outra do jogo
velocidade = 5  # velocidade da bola
start = True
continuar = True

while continuar:
    # Fisica do jogo

    # Aleatoriza a velocidade e direcao da bola no primeiro frame do jogo e cria os tijolinhos do lvl
    if start:
        difficulty = 8 - level
        for o in range(0, 200, 30):
            for i in range(0, 800, 50):
                index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                if restart:
                    bricks[index].undraw()
                scopex_top_left.clear()
                scopey_top_left.clear()
                scopex_bottom_right.clear()
                scopey_bottom_right.clear()
        for o in range(0, 200, 30):
            no_block = random.randrange(difficulty - 3, difficulty)
            for i in range(0, 800, 50):
                if no_block >= (i / 50) or no_block >= 15 - (i / 50):
                    index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                    bricks[index] = Rectangle(Point(0, 0), Point(0, 0))
                    bricks[index].draw(win)
                    scopex_top_left.append(0)
                    scopey_top_left.append(0)
                    scopex_bottom_right.append(0)
                    scopey_bottom_right.append(0)
                    broken += 1
                else:
                    index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                    bricks[index] = Rectangle(Point(xbrick + i, ybrick + o), Point(xbrick + 45 + i, ybrick + 25 + o))
                    vermelho = random.randrange(245, 255)
                    verde = random.randrange(120, 155)
                    azul = random.randrange(0, 75)
                    bricks[index].setFill(color_rgb(vermelho, verde, azul))
                    bricks[index].draw(win)
                    scopex_top_left.append(xbrick + i)
                    scopey_top_left.append(ybrick + o)
                    scopex_bottom_right.append(xbrick + 50 + i)
                    scopey_bottom_right.append(ybrick + 30 + o)
        passada = random.randrange(1, 10)

        circulo.undraw()
        col = 390
        lin = 300
        raio = 15
        circulo = Circle(Point(col, lin), raio)
        circulo.setFill(color_rgb(100, 100, 100))
        circulo.draw(win)

        barra.undraw()
        col_ini = 340
        tamanho = 100
        barra = Line(Point(col_ini, 530), Point(col_ini + tamanho, 530))
        barra.setFill(color_rgb(50, 49, 45))
        barra.setWidth(10)
        barra.draw(win)
        if level > 1:
            leveltext = Text(Point(400, 350), "Level: " + str(level))
            leveltext.draw(win)
        waitingforstart = Text(Point(400, 375), "Press SPACE to start")
        waitingforstart.draw(win)

        while comecar == False:
            tecla = win.checkKey()
            if tecla == "space":
                pygame.mixer.Sound.play(hit)
                comecar = True
                waitingforstart.undraw()
                if level > 1:
                    leveltext.undraw()
        restart = True
        start = False

    # Movimento da barra
    if (col_ini + 5) <= 701 and (col_ini - 5) >= -1 and reseting == False:
        col_ini = col_ini + barramento
        barra.undraw()
        barra = Line(Point(col_ini, 530), Point(col_ini + 100, 530))
        barra.setFill(color_rgb(50, 49, 45))
        barra.setWidth(10)
        barra.draw(win)
    elif (col_ini + 5) >= 701 and reseting == False:
        barramento = -barramento
        while (col_ini + 5) >= 701:
            col_ini = col_ini - 1
    elif (col_ini - 5) <= -1 and reseting == False:
        barramento = -barramento
        while (col_ini - 5) <= -1:
            col_ini = col_ini + 1

    # Reconhece quando a Bola bate nos tijolinhos da pagina
    for q in range(1, 112):
        if col >= scopex_top_left[q] - 5 and col <= scopex_bottom_right[q] + 5 and lin == scopey_bottom_right[q] + 5:
            bricks[q.__str__()].undraw()
            pygame.mixer.Sound.play(blockbreak)
            scopey_top_left[q] = 0
            scopex_top_left[q] = 0
            scopey_bottom_right[q] = 0
            scopex_bottom_right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            velocidade = -velocidade

        if col >= scopex_top_left[q] - 5 and col <= scopex_bottom_right[q] + 5 and lin == scopey_top_left[q] - 5:
            bricks[q.__str__()].undraw()
            pygame.mixer.Sound.play(blockbreak)
            scopey_top_left[q] = 0
            scopex_top_left[q] = 0
            scopey_bottom_right[q] = 0
            scopex_bottom_right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            velocidade = -velocidade

        if lin >= scopey_top_left[q] - 5 and lin <= scopey_bottom_right[q] + 5 and col == scopex_bottom_right[q] + 5:
            bricks[q.__str__()].undraw()
            pygame.mixer.Sound.play(blockbreak)
            scopey_top_left[q] = 0
            scopex_top_left[q] = 0
            scopey_bottom_right[q] = 0
            scopex_bottom_right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            passada = -passada

        if lin >= scopey_top_left[q] - 5 and lin <= scopey_bottom_right[q] + 5 and col == scopex_top_left[q] - 5:
            bricks[q.__str__()].undraw()
            pygame.mixer.Sound.play(blockbreak)
            scopey_top_left[q] = 0
            scopex_top_left[q] = 0
            scopey_bottom_right[q] = 0
            scopex_bottom_right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            passada = -passada
            
        if lin == scopey_top_left[q] and col == scopex_top_left[q] - 5:
            bricks[q.__str__()].undraw()
            scopey_top_left[q] = 0
            scopex_top_left[q] = 0
            scopey_bottom_right[q] = 0
            scopex_bottom_right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            passada = -passada
            velocidade = -velocidade

        if lin == scopey_bottom_right[q] + 5 and col == scopex_bottom_right[q] + 5:
            bricks[q.__str__()].undraw()
            scopey_top_left[q] = 0
            scopex_top_left[q] = 0
            scopey_bottom_right[q] = 0
            scopex_bottom_right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            passada = -passada
            velocidade = -velocidade

    # Reconhece quando a Bola bate na direita da pagina
    if (col + raio + passada) > 800:
        passada = -passada

    # Passa pro proximo level
    if broken >= 112:
        level += 1
        broken = 0
        velocidade = velocidade * 1.2
        barramento = barramento * 1.2
        start = True
        comecar = False

    # Reconhece quando a Bola bate na esquerda da pagina
    if (col - raio + passada) < 0:
        passada = -passada

    # Reconhece quando a Bola bate no topo da pagina
    if lin < 65:
        velocidade = -velocidade

    # Reconhece quando a Bola bate na barra (Player)
    if lin >= 515 and col > col_ini and col < (col_ini + tamanho) and lin <= 519:
        velocidade = -velocidade
        pygame.mixer.Sound.play(hit)

    # Criar tela de Game Over
    if lin > 550:
        pygame.mixer.Sound.play(go)
        reseting = True
        linha_superior.undraw()
        linha_inferior.undraw()
        circulo.undraw()
        pontos.undraw()
        barra.undraw()
        quadrado = Rectangle(Point(0, 0), Point(800, 600))
        quadrado.setFill("black")
        quadrado.draw(win)
        t = Text(Point(400, 125), "GAME OVER")
        t.setSize(22)
        t.setFill(color_rgb(255, 0, 0))
        t.setStyle('bold')
        t.draw(win)

        # ScoreBoard
        pontibulos = str(pts)
        jog.append(pontibulos.zfill(3) + " - " + NAME)
        jog.sort(reverse=True)

        borda = Rectangle(Point(200, 600), Point(600, 200))
        borda.setFill("gray")
        borda.setOutline("black")
        borda.draw(win)

        folha = Rectangle(Point(210, 600), Point(590, 210))
        folha.setFill("navy")
        folha.setOutline("gold")
        folha.draw(win)

        lin1 = Rectangle(Point(210, 310), Point(590, 300))
        lin1.setFill("gray")
        lin1.setOutline("gray")
        lin1.draw(win)
        pont1 = Text(Point(400, 280), jog[0])
        pont1.setSize(22)
        pont1.setFill("gold")
        pont1.setStyle('bold')
        pont1.draw(win)
        lin2 = Rectangle(Point(210, 400), Point(590, 410))
        lin2.setFill("gray")
        lin2.setOutline("gray")
        lin2.draw(win)
        pont2 = Text(Point(400, 380), jog[1])
        pont2.setSize(22)
        pont2.setFill("gold")
        pont2.setStyle('bold')
        pont2.draw(win)
        lin3 = Rectangle(Point(210, 500), Point(590, 510))
        lin3.setFill("gray")
        lin3.setOutline("gray")
        lin3.draw(win)
        pont3 = Text(Point(400, 480), jog[2])
        pont3.setSize(22)
        pont3.setFill("gold")
        pont3.setStyle('bold')
        pont3.draw(win)
        pont4 = Text(Point(400, 550), jog[3])
        pont4.setSize(22)
        pont4.setFill("gold")
        pont4.setStyle('bold')
        pont4.draw(win)
        lin = 300

        linha_superior.undraw()
        linha_inferior.undraw()
        circulo.undraw()
        pontos.undraw()
        barra.undraw()

    if tecla == "space" and reseting:
        pygame.mixer.Sound.play(hit)
        for o in range(0, 200, 30):
            for i in range(0, 800, 50):
                index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                bricks[index].undraw()
                scopex_top_left.clear()
                scopey_top_left.clear()
                scopex_bottom_right.clear()
                scopey_bottom_right.clear()
        name.undraw()
        quadrado.undraw()
        t.undraw()
        pont1.undraw()
        pont2.undraw()
        pont3.undraw()
        pont4.undraw()
        lin3.undraw()
        lin2.undraw()
        lin1.undraw()
        folha.undraw()
        borda.undraw()
        # ---------------------------------------------------------------

        t0 = Text(Point(400, 125), 'IMHOTEP')
        t0.setTextColor('orange red')
        t0.setStyle('bold')
        t0.setSize(30)
        t0.draw(win)

        l1 = Line(Point(0, 200), Point(800, 200))
        l1.setWidth(3)
        l1.draw(win)

        l2 = Line(Point(0, 400), Point(800, 400))
        l2.setWidth(3)
        l2.draw(win)

        t1 = Text(Point(150, 300), 'Digite seu nome :')
        t1.setStyle('bold')
        t1.setSize(18)
        t1.draw(win)

        nome = Entry(Point(400, 300), 30)
        nome.setFill('white')
        nome.setTextColor('black')
        nome.setStyle('bold italic')
        nome.draw(win)

        botao = Rectangle(Point(350, 325), Point(450, 375))
        botao.setFill('light gray')
        botao.draw(win)

        tex_botao = Text(Point(401, 352), 'PLAY !')
        tex_botao.setStyle('bold')
        tex_botao.draw(win)

        while True:
            ponto = win.getMouse()
            x = ponto.getX()
            y = ponto.getY()
            if x >= 350 and x <= 450 and y >= 325 and y <= 375:
                break

        print(t1)
        print(nome.getText())

        NAME = nome.getText()

        nome.undraw()
        tex_botao.undraw()
        botao.undraw()
        t1.undraw()
        l1.undraw()
        l2.undraw()
        t0.undraw()

        name = Text(Point(100, 575), "Nome: " + NAME)
        name.setStyle('bold italic')
        name.setSize(16)
        name.draw(win)

        # -----------------------------------------------------------------

        # Design
        linha_superior = Line(Point(0, 40), Point(800, 40))
        linha_superior.setWidth(10)
        linha_superior.setFill(color_rgb(0, 0, 0))
        linha_superior.draw(win)
        # Design
        linha_inferior = Line(Point(0, 550), Point(800, 550))
        linha_inferior.setWidth(3)
        linha_inferior.setFill(color_rgb(0, 0, 0))
        linha_inferior.draw(win)

        # Ball Design
        col = 390
        raio = 15
        circulo = Circle(Point(col, lin), raio)
        circulo.setFill(color_rgb(100, 100, 100))
        circulo.draw(win)

        # Gamescore UI
        pts = 0
        pontos = Text(Point(395, 575), "Pontos: " + str(pts))
        pontos.setStyle('bold')
        pontos.setSize(18)
        pontos.draw(win)

        # Design da barra (antes do primeiro input)
        col_ini = 340
        tamanho = 100
        barra = Line(Point(col_ini, 530), Point(col_ini + tamanho, 530))
        barra.setFill(color_rgb(50, 49, 45))
        barra.setWidth(10)
        barra.draw(win)

        # Variaveis no Startup
        comecar = False
        restart = False
        level = 1
        broken = 0
        difficulty = 8 - level
        barramento = 7.5
        xbrick = 5
        ybrick = 60
        bricks = {}
        scopex_top_left = []
        scopey_top_left = []
        scopex_bottom_right = []
        scopey_bottom_right = []
        clock = .035  # Tempo entre uma atualizacao e outra do jogo
        velocidade = 5  # velocidade da bola
        start = True
        continuar = True
        reseting = False

    # Nova posição do círculo
    if reseting == False:
        circulo.undraw()
        col += passada
        lin += velocidade
        circulo = Circle(Point(col, lin), 15)
        circulo.setFill(color_rgb(100, 100, 100))
        circulo.draw(win)

    # Checa a cada tick pelo input do teclado
    tecla = win.checkKey()

    # GameTestingCheats:
    if tecla == "1":
        broken += 1
    # Sair do joguinho
    if tecla == "Escape":
        continuar = False
        continue

    # Barra muda de direcao
    if tecla == "space":
        barramento = -barramento

    # Esse valor faz referência ao game-tick, ou seja, de quanto em quanto tempo o jogo atualiza
    time.sleep(clock)
