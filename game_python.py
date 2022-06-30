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
win.setBackground(color_rgb(255, 178, 102))

yell = True
for incLin in range(0, 250, 25):
    for inc in range(0, 800, 40):
        ret = Rectangle(Point(0 + inc, 0 + incLin), Point(39 + inc, 24 + incLin))
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

text_Botao = Text(Point(400, 532), 'START !')
text_Botao.setTextColor("red")
text_Botao.setStyle("bold")
text_Botao.setSize(16)
text_Botao.draw(win)

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
text_Botao.undraw()

# ---------------tela_nome---------------------------------

quadrad = Rectangle(Point(0, 0), Point(800, 600))
quadrad.setFill(color_rgb(255, 178, 102))
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

textBotao = Text(Point(401, 352), 'PLAY !')
textBotao.setStyle('bold')
textBotao.draw(win)

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
textBotao.undraw()
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
linhaSuperior = Line(Point(0, 40), Point(800, 40))
linhaSuperior.setWidth(10)
linhaSuperior.setFill(color_rgb(0, 0, 0))
linhaSuperior.draw(win)
# Design
linhaInferior = Line(Point(0, 550), Point(800, 550))
linhaInferior.setWidth(3)
linhaInferior.setFill(color_rgb(0, 0, 0))
linhaInferior.draw(win)

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
colIni = 340
tamanho = 100
barra = Line(Point(colIni, 530), Point(colIni + tamanho, 530))
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
scopexTop_Left = []
scopeyTop_Left = []
scopexBottom_Right = []
scopeyBottom_Right = []
Clock = .035  # Tempo entre uma atualizacao e outra do jogo
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
                scopexTop_Left.clear()
                scopeyTop_Left.clear()
                scopexBottom_Right.clear()
                scopeyBottom_Right.clear()
        for o in range(0, 200, 30):
            NoBlock = random.randrange(difficulty - 3, difficulty)
            for i in range(0, 800, 50):
                if NoBlock >= (i / 50) or NoBlock >= 15 - (i / 50):
                    index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                    bricks[index] = Rectangle(Point(0, 0), Point(0, 0))
                    bricks[index].draw(win)
                    scopexTop_Left.append(0)
                    scopeyTop_Left.append(0)
                    scopexBottom_Right.append(0)
                    scopeyBottom_Right.append(0)
                    broken += 1
                else:
                    index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                    bricks[index] = Rectangle(Point(xbrick + i, ybrick + o), Point(xbrick + 45 + i, ybrick + 25 + o))
                    vermelho = random.randrange(245, 255)
                    verde = random.randrange(120, 155)
                    azul = random.randrange(0, 75)
                    bricks[index].setFill(color_rgb(vermelho, verde, azul))
                    bricks[index].draw(win)
                    scopexTop_Left.append(xbrick + i)
                    scopeyTop_Left.append(ybrick + o)
                    scopexBottom_Right.append(xbrick + 50 + i)
                    scopeyBottom_Right.append(ybrick + 30 + o)
        passada = random.randrange(1, 10)

        circulo.undraw()
        col = 390
        lin = 300
        raio = 15
        circulo = Circle(Point(col, lin), raio)
        circulo.setFill(color_rgb(100, 100, 100))
        circulo.draw(win)

        barra.undraw()
        colIni = 340
        tamanho = 100
        barra = Line(Point(colIni, 530), Point(colIni + tamanho, 530))
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
    if (colIni + 5) <= 701 and (colIni - 5) >= -1 and reseting == False:
        colIni = colIni + barramento
        barra.undraw()
        barra = Line(Point(colIni, 530), Point(colIni + 100, 530))
        barra.setFill(color_rgb(50, 49, 45))
        barra.setWidth(10)
        barra.draw(win)
    elif (colIni + 5) >= 701 and reseting == False:
        barramento = -barramento
        while (colIni + 5) >= 701:
            colIni = colIni - 1
    elif (colIni - 5) <= -1 and reseting == False:
        barramento = -barramento
        while (colIni - 5) <= -1:
            colIni = colIni + 1

    # Reconhece quando a Bola bate nos tijolinhos da pagina
    for q in range(1, 112):
        if col >= scopexTop_Left[q] - 5 and col <= scopexBottom_Right[q] + 5 and lin == scopeyBottom_Right[q] + 5:
            bricks[q.__str__()].undraw()
            pygame.mixer.Sound.play(blockbreak)
            scopeyTop_Left[q] = 0
            scopexTop_Left[q] = 0
            scopeyBottom_Right[q] = 0
            scopexBottom_Right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            velocidade = -velocidade

        if col >= scopexTop_Left[q] - 5 and col <= scopexBottom_Right[q] + 5 and lin == scopeyTop_Left[q] - 5:
            bricks[q.__str__()].undraw()
            pygame.mixer.Sound.play(blockbreak)
            scopeyTop_Left[q] = 0
            scopexTop_Left[q] = 0
            scopeyBottom_Right[q] = 0
            scopexBottom_Right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            velocidade = -velocidade

        if lin >= scopeyTop_Left[q] - 5 and lin <= scopeyBottom_Right[q] + 5 and col == scopexBottom_Right[q] + 5:
            bricks[q.__str__()].undraw()
            pygame.mixer.Sound.play(blockbreak)
            scopeyTop_Left[q] = 0
            scopexTop_Left[q] = 0
            scopeyBottom_Right[q] = 0
            scopexBottom_Right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            passada = -passada

        if lin >= scopeyTop_Left[q] - 5 and lin <= scopeyBottom_Right[q] + 5 and col == scopexTop_Left[q] - 5:
            bricks[q.__str__()].undraw()
            pygame.mixer.Sound.play(blockbreak)
            scopeyTop_Left[q] = 0
            scopexTop_Left[q] = 0
            scopeyBottom_Right[q] = 0
            scopexBottom_Right[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.setStyle('bold')
            pontos.setSize(18)
            pontos.draw(win)
            passada = -passada
            
            if lin == scopeyTop_Left[q] and col == scopexTop_Left[q] - 5:
             bricks[q.__str__()].undraw()
            scopeyTop_Left[q] = 0
            scopexTop_Left[q] = 0
            scopeyBottom_Right[q] = 0
            scopexBottom_Right[q] = 0
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

        if lin == scopeyBottom_Right[q] + 5 and col == scopexBottom_Right[q] + 5:
            bricks[q.__str__()].undraw()
            scopeyTop_Left[q] = 0
            scopexTop_Left[q] = 0
            scopeyBottom_Right[q] = 0
            scopexBottom_Right[q] = 0
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
    if lin >= 515 and col > colIni and col < (colIni + tamanho) and lin <= 519:
        velocidade = -velocidade
        pygame.mixer.Sound.play(hit)

    # Criar tela de Game Over
    if lin > 550:
        pygame.mixer.Sound.play(go)
        reseting = True
        linhaSuperior.undraw()
        linhaInferior.undraw()
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

        linhaSuperior.undraw()
        linhaInferior.undraw()
        circulo.undraw()
        pontos.undraw()
        barra.undraw()

    if tecla == "space" and reseting:
        pygame.mixer.Sound.play(hit)
        for o in range(0, 200, 30):
            for i in range(0, 800, 50):
                index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                bricks[index].undraw()
                scopexTop_Left.clear()
                scopeyTop_Left.clear()
                scopexBottom_Right.clear()
                scopeyBottom_Right.clear()
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

        win.setBackground(color_rgb(51, 153, 255))

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

        textBotao = Text(Point(401, 352), 'PLAY !')
        textBotao.setStyle('bold')
        textBotao.draw(win)

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
        textBotao.undraw()
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
        win.setBackground(color_rgb(101, 178, 255))

        # Design
        linhaSuperior = Line(Point(0, 40), Point(800, 40))
        linhaSuperior.setWidth(10)
        linhaSuperior.setFill(color_rgb(0, 0, 0))
        linhaSuperior.draw(win)
        # Design
        linhaInferior = Line(Point(0, 550), Point(800, 550))
        linhaInferior.setWidth(3)
        linhaInferior.setFill(color_rgb(0, 0, 0))
        linhaInferior.draw(win)

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
        colIni = 340
        tamanho = 100
        barra = Line(Point(colIni, 530), Point(colIni + tamanho, 530))
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
        scopexTop_Left = []
        scopeyTop_Left = []
        scopexBottom_Right = []
        scopeyBottom_Right = []
        Clock = .035  # Tempo entre uma atualizacao e outra do jogo
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
    time.sleep(Clock)
