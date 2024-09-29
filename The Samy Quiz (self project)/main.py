
import pgzrun

HEIGHT = 650
WIDTH = 870

marqueeBox = Rect(0,0,880,80)
questionBox = Rect(0,0,650,150)
timerBox = Rect(0,0,150,150)
answerBox1 = Rect(0,0,300,150)
answerBox2 = Rect(0,0,300,150)
answerBox3 = Rect(0,0,300,150)
answerBox4 = Rect(0,0,300,150)
skipBox = Rect(0,0,150,330)

score = 0
marqueeMessage = ""
timeLeft = 10
fileName = "questions.txt"
isGameover = False
question = []
questions = []
answerBoxes = [answerBox1,answerBox2,answerBox3,answerBox4]
questionIndex = 0
questionCount = 0

marqueeBox.move_ip(0,0)
questionBox.move_ip(20,100)
timerBox.move_ip(700,100)
answerBox1.move_ip(20,270)
answerBox2.move_ip(370,270)
answerBox3.move_ip(20,450)
answerBox4.move_ip(370,450)
skipBox.move_ip(700,270)

def draw():
    global marqueeMessage
    screen.clear()
    screen.fill("black")
    screen.draw.rect(marqueeBox,"black")
    screen.draw.rect(questionBox,"green")
    screen.draw.rect(skipBox,"red")
    screen.draw.rect(timerBox,"blue")
    for answerBox in answerBoxes:
        screen.draw.rect(answerBox,"purple")
    marqueeMessage = f"Welcome to the Samy Quiz! Question {questionIndex}/{questionCount}."
    screen.draw.textbox(marqueeMessage, marqueeBox, color = "white")
    screen.draw.textbox(str(timeLeft), timerBox, color = "white", shadow = (0.5,0.5), scolor = "grey")
    screen.draw.textbox(question[0].strip(), questionBox, color = "white", shadow = (0.5,0.5), scolor = "grey")
    screen.draw.textbox("Skip", skipBox, color = "white", shadow = (0.5,0.5), scolor = "grey", angle = -90)
    index = 1
    for answerBox in answerBoxes:
        screen.draw.textbox(question[index].strip(), answerBox, color = "white", shadow = (0.5,0.5), scolor = "grey")
        index += 1

def Marquee():
    marqueeBox.x = marqueeBox.x - 2
    if marqueeBox.right < 0:
        marqueeBox.left = WIDTH

def readQFile():
    global questionCount, questions
    Qfile = open(fileName, "r")
    for row in Qfile:
        questions.append(row)
        questionCount += 1
    Qfile.close()

def readNextQ():
    global questionIndex
    questionIndex += 1

    return questions.pop(0).split(",")


def gameOver():
    global question, timeLeft, isGameover
    message = f"Gameover! You got {score}/{questionCount}!"
    question = [message,"_","_","_","_",5]
    timeLeft = 0
    isGameover = True

def correctAnswer():
    global score, question, timeLeft, questions
    score += 1
    if questions:
        question = readNextQ()
        timeLeft = 10
    else:
        gameOver()

def updTimeLeft():
    global timeLeft
    if timeLeft:
        timeLeft -= 1
    else:
        gameOver()

def skipQ():
    global question, timeLeft
    if questions and not isGameover:
        question = readNextQ()
        timeLeft = 10
    else:
        gameOver()

def on_mouse_down(pos):
    index = 1
    for answerBox in answerBoxes:
        if answerBox.collidepoint(pos):
            if index is int(question[5]):
                correctAnswer()
            else:
                gameOver()
        index += 1
    if skipBox.collidepoint(pos):
        skipQ()

def update():
    Marquee()

readQFile()
question = readNextQ()
clock.schedule_interval(updTimeLeft,1)
pgzrun.go()