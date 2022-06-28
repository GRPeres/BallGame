from graphics import *
import pygame
import random

# Cria a janela
win = GraphWin("Bolinha ...", 800, 600)
# ---------------------- VINNY -------------------------------------------------
pygame.mixer.init()
pygame.init()

win.setBackground('orange')

t0 = Text(Point(400, 125), 'IMHOTEP')
t0.setTextColor('dark blue')
t0.setSize(25)
t0.draw(win)

l1 = Line(Point(0, 200), Point(800, 200))
l1.setWidth(3)
l1.draw(win)

l2 = Line(Point(0, 400), Point(800, 400))
l2.setWidth(3)
l2.draw(win)

t1 = Text(Point(100, 300), 'Digite seu nome :')
t1.setSize(15)
t1.draw(win)

nome = Entry(Point(400, 300), 30)
nome.setFill('white')
nome.setTextColor('blue')
nome.draw(win)

botao = Rectangle(Point(350, 325), Point(450, 375))
botao.setFill('light gray')
botao.draw(win)

textBotao = Text(Point(400, 350), 'PLAY !')
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
name.setSize(14)
name.draw(win)

# -------------------------------------------------------------------------
win.setBackground(color_rgb(174,164,124))

# Design
linhaSuperior = Line(Point(0, 40), Point(800, 40))
linhaSuperior.setWidth(10)
linhaSuperior.setFill(color_rgb(107,100,75))
linhaSuperior.draw(win)
# Design
linhaInferior = Line(Point(0, 550), Point(800, 550))
linhaInferior.setWidth(3)
linhaInferior.setFill(color_rgb(107,100,75))
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
pontos = Text(Point(400, 575), "Pontos: " + str(pts))
pontos.setSize(14)
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
scopexTop_Right = []
scopeyTop_Right = []
scopexBottom_Left = []
scopeyBottom_Left = []
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
                scopexTop_Right.clear()
                scopeyTop_Right.clear()
                scopexBottom_Left.clear()
                scopeyBottom_Left.clear()
        for o in range(0, 200, 30):
            NoBlock = random.randrange(difficulty - 3, difficulty)
            for i in range(0, 800, 50):
                if NoBlock >= (i / 50) or NoBlock >= 15 - (i / 50):
                    index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                    bricks[index] = Rectangle(Point(0, 0), Point(0, 0))
                    bricks[index].draw(win)
                    scopexTop_Right.append(0)
                    scopeyTop_Right.append(0)
                    scopexBottom_Left.append(0)
                    scopeyBottom_Left.append(0)
                    broken += 1
                else:
                    index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                    bricks[index] = Rectangle(Point(xbrick + i, ybrick + o), Point(xbrick + 45 + i, ybrick + 25 + o))
                    vermelho = random.randrange(112, 154)
                    verde = random.randrange(92, 123)
                    azul = random.randrange(3, 9)
                    bricks[index].setFill(color_rgb(vermelho, verde, azul))
                    bricks[index].draw(win)
                    scopexTop_Right.append(xbrick + i)
                    scopeyTop_Right.append(ybrick + o)
                    scopexBottom_Left.append(xbrick + 50 + i)
                    scopeyBottom_Left.append(ybrick + 30 + o)
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
        if col >= scopexTop_Right[q] - 5 and lin >= scopeyTop_Right[q] - 5 and col <= scopexBottom_Left[
            q] + 5 and lin <= \
                scopeyBottom_Left[q] + 5:
            bricks[q.__str__()].undraw()
            scopeyTop_Right[q] = 0
            scopexTop_Right[q] = 0
            scopeyBottom_Left[q] = 0
            scopexBottom_Left[q] = 0
            broken += 1
            # Atualiza os pontos a cada toque da bola na barra,
            pontos.undraw()
            pts += 1
            pontos = Text(Point(400, 575), "Pontos: " + str(pts))
            pontos.draw(win)

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

    # Criar tela de Game Over
    if lin > 550:
        reseting = True
        linhaSuperior.undraw()
        linhaInferior.undraw()
        circulo.undraw()
        pontos.undraw()
        barra.undraw()
        quadrado = Rectangle(Point(0, 0), Point(800, 600))
        quadrado.setFill("orange")
        quadrado.draw(win)
        t = Text(Point(400, 80), "GAME OVER")
        t.setSize(22)
        t.setFill(color_rgb(255, 0, 0))
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
        folha.setFill("black")
        folha.setOutline("yellow")
        folha.draw(win)

        lin1 = Rectangle(Point(210, 310), Point(590, 300))
        lin1.setFill("gray")
        lin1.setOutline("gray")
        lin1.draw(win)
        pont1 = Text(Point(400, 280), jog[0])
        pont1.setSize(22)
        pont1.setFill("yellow")
        pont1.draw(win)
        lin2 = Rectangle(Point(210, 400), Point(590, 410))
        lin2.setFill("gray")
        lin2.setOutline("gray")
        lin2.draw(win)
        pont2 = Text(Point(400, 380), jog[1])
        pont2.setSize(22)
        pont2.setFill("gold")
        pont2.draw(win)
        lin3 = Rectangle(Point(210, 500), Point(590, 510))
        lin3.setFill("gray")
        lin3.setOutline("gray")
        lin3.draw(win)
        pont3 = Text(Point(400, 480), jog[2])
        pont3.setSize(22)
        pont3.setFill("yellow")
        pont3.draw(win)
        pont4 = Text(Point(400, 550), jog[3])
        pont4.setSize(22)
        pont4.setFill("gold")
        pont4.draw(win)
        lin = 300

        linhaSuperior.undraw()
        linhaInferior.undraw()
        circulo.undraw()
        pontos.undraw()
        barra.undraw()

    if tecla == "space" and reseting:
        for o in range(0, 200, 30):
            for i in range(0, 800, 50):
                index = ((o / 30 * 16).__int__() + (i / 50).__int__()).__str__()
                bricks[index].undraw()
                scopexTop_Right.clear()
                scopeyTop_Right.clear()
                scopexBottom_Left.clear()
                scopeyBottom_Left.clear()
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
        # ---------------------- VINNY -------------------------------------------------
        pygame.mixer.init()
        pygame.init()

        win.setBackground('orange')

        t0 = Text(Point(400, 125), 'IMHOTEP')
        t0.setTextColor('dark blue')
        t0.setSize(25)
        t0.draw(win)

        l1 = Line(Point(0, 200), Point(800, 200))
        l1.setWidth(3)
        l1.draw(win)

        l2 = Line(Point(0, 400), Point(800, 400))
        l2.setWidth(3)
        l2.draw(win)

        t1 = Text(Point(100, 300), 'Digite seu nome :')
        t1.setSize(15)
        t1.draw(win)

        nome = Entry(Point(400, 300), 30)
        nome.setFill('white')
        nome.setTextColor('blue')
        nome.draw(win)

        botao = Rectangle(Point(350, 325), Point(450, 375))
        botao.setFill('light gray')
        botao.draw(win)

        textBotao = Text(Point(400, 350), 'PLAY !')
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
        name.setSize(14)
        name.draw(win)

        # -------------------------------------------------------------------------
        win.setBackground(color_rgb(174,164,124))

        # Design
        linhaSuperior = Line(Point(0, 40), Point(800, 40))
        linhaSuperior.setWidth(10)
        linhaSuperior.setFill(color_rgb(107,100,75))
        linhaSuperior.draw(win)
        # Design
        linhaInferior = Line(Point(0, 550), Point(800, 550))
        linhaInferior.setWidth(3)
        linhaInferior.setFill(color_rgb(107,100,75))
        linhaInferior.draw(win)

        # Ball Design
        col = 390
        raio = 15
        circulo = Circle(Point(col, lin), raio)
        circulo.setFill(color_rgb(100, 100, 100))
        circulo.draw(win)

        # Gamescore UI
        pts = 0
        pontos = Text(Point(400, 575), "Pontos: " + str(pts))
        pontos.setSize(14)
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
        scopexTop_Right = []
        scopeyTop_Right = []
        scopexBottom_Left = []
        scopeyBottom_Left = []
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
