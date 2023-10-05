#Maths game
import pygame
import sys
import random
pygame.init()
DIMENSIONS = [800, 600]
REFRESH_SPEED = 50
screen = pygame.display.set_mode((DIMENSIONS[0], DIMENSIONS[1]))
pygame.display.set_caption("maths game")

clock = pygame.time.Clock()

#global variables
score = 0
lives = 5
AnswerCoord = dict()
SPEED = 2
status = str()
#loading images
bgSurface = pygame.image.load("bg.jpg").convert_alpha()
groundSurface = pygame.image.load("ground.png").convert_alpha()
groundRect = groundSurface.get_rect(topleft=(0, 500))

#question and answer generator function
def Generate_Questions():
    question = random.randint(0, 100)
    return question


def Generate_Correct_Answer(question):
    operation = random.choice(['add', 'minus', 'multiply', 'divide'])
    if operation == 'add':
        num1 = random.randint(0, question)
        num2 = question - num1
        answer = f"{num1}+{num2}"
        
    elif operation == 'minus':
        num1 = random.randint(question, 200)
        num2 = num1 - question
        answer = f"{num1}-{num2}"
        
    elif operation == 'multiply':
        factors = []
        for i in range(1, question + 1):
            if question % i == 0:
                factors.append(i)
        if len(factors) == 0:
            num1 = 1
            num2 = question
        elif len(factors) == 1:
            num1, num2 = factors[0], factors[0]
        else:
            num1 = int(random.choice(factors))
            num2 = int(question/num1)
        answer = f"{num1}x{num2}"
        
    elif operation == 'divide':
        multiplier = random.randint(1, 8)
        num1 = question * multiplier
        num2 = multiplier
        answer = f"{num1}/{num2}"
        
    return(f"!{answer}")



def Generate_Wrong_Answers():
    num1, num2 = random.randint(0, 200), random.randint(0, 200)
    operation = random.choice(['+', '-', 'x', '/'])
    return(f"{num1}{operation}{num2}")
    
        

#texts on top left (target Number) | top right (score and lives left)
def Blit_Text(number):
    textFont = pygame.font.Font(None, 100)
    questionSurface = textFont.render(str(number), True, 'Red')
    screen.blit(questionSurface, (10, 10))

    textFont = pygame.font.Font(None, 30)
    scoreSurface = textFont.render(f"Score:{str(score)}", True, (1, 50, 32))
    livesSurface = textFont.render(f"Lives:{str(lives)}", True, (1, 50, 32))
    statusSurface = textFont.render(f"Status:{status}", True, 'Black')
    screen.blit(scoreSurface, (700, 10))
    screen.blit(livesSurface, (700, 40))
    screen.blit(statusSurface, (10, 70))


#add answer and coord pairs to dict
def Add_AnswerCoord(loops, correctAnswer):
    timeElapse = loops/REFRESH_SPEED
    wrongBefore = int(random.randint(2, 5))
    if (timeElapse%1==0 and timeElapse == wrongBefore):
        AnswerCoord[correctAnswer] = [random.randint(50, 650), 0]
        
    elif (timeElapse%1==0 and timeElapse<wrongBefore):
        answer = Generate_Wrong_Answers()
        coord = [random.randint(100, 650), 0]
        AnswerCoord[answer] = coord
        
    elif (timeElapse%1==0 and timeElapse<20):
        answer = Generate_Wrong_Answers()
        coord = [random.randint(100, 650), 0]
        AnswerCoord[answer] = coord

    
#answer movement function (called after Add_AnswerCoord. It makes all the coordinates in AnswerCoord go down by SPEED)
answersFont = pygame.font.Font(None, 50)
def Answer_Movement(AnswerCoord):
    for answer, coord in AnswerCoord.items():
        answerSurface = answersFont.render(answer, True, 'Purple')
        coordTuple = (coord[0], coord[1])
        answerRect = answerSurface.get_rect(midbottom = coordTuple)
        screen.blit(answerSurface, answerRect)
        AnswerCoord[answer][1] += SPEED
    

#clicked on answer function (correct + incorrect)
def Mouse_Click(mouse_pos, correctAnswer):
    global lives
    x, y = mouse_pos[0], mouse_pos[1]
    
    #checks it equals correct answer coord
    try:
        correctAnsX, correctAnsY = AnswerCoord[correctAnswer][0], AnswerCoord[correctAnswer][1]
        if (correctAnsX-50 <= x <= correctAnsX+50) and (correctAnsY-40 <= y <= correctAnsY+20):
            status = "correct"
            Change_Color(correctAnswer)
            return status
    except Exception:
        pass
    #checks if it equals any other incorrect answers
    else:
        for Coord in AnswerCoord.values():
            if (Coord[0]-50 <= x <= Coord[0]+50) and (Coord[1]-40 <= y <= Coord[1]+20):
                status = "incorrect"
                lives -= 1
                return status
    
#correct answer changes color
def Change_Color(correctAnswer):
    correctAnswerSurface = answersFont.render(correctAnswer, True, 'Green')
    x, y = AnswerCoord[correctAnswer][0],AnswerCoord[correctAnswer][1]
    correctAnswerRect = correctAnswerSurface.get_rect(midbottom = (x, y))
    screen.blit(correctAnswerSurface, correctAnswerRect)
    
#answer reaches floor function (correct + incorrect)
def Check_Floor(correctAnswer):
    try:
        CorrectAnsY = AnswerCoord[correctAnswer][1]
        if CorrectAnsY > 500:
            return True
    except KeyError:
        pass
    return False

#score <=0 function
def Check_Lives0(lives):
    if lives == 0:
        return True
    return False
        
        

#Display game over function
def Game_Over():
    AnswerCoord.clear()
    text = "Its fuckin game over"
    message = "Press Return to play again"
    textFont = pygame.font.Font(None, 100)
    messageFont = pygame.font.Font(None, 30)
    textSurface = textFont.render(text, True, 'Red')
    messageSurface = messageFont.render(message, True, 'Red')
    textRect = textSurface.get_rect(center=(400, 300))
    messageRect = messageSurface.get_rect(center=(400, 400))
    screen.blit(textSurface, textRect)
    screen.blit(messageSurface, messageRect)
    
#Restart game function
    '''
def Play_Again():
    global lives, status, roundOver
    lives = 5
    status = str()
    roundOver = False
    bgSurface = pygame.image.load("bg.jpg").convert_alpha()
    groundSurface = pygame.image.load("ground.png").convert_alpha()
    groundRect = groundSurface.get_rect(topleft=(0, 500))
    '''
    
    
roundOver = False
subtractingFloorLife = False
answeredCorrectly = False
loops = 0
question = Generate_Questions()
correctAnswer = Generate_Correct_Answer(question)

while True:
    #blitting images
    screen.blit(bgSurface, (0,0))
    screen.blit(groundSurface, groundRect)
    Blit_Text(question)
    
    #if round over: new question, update score, clear dictionary, new correct answer, subtractingFloorLife
    if roundOver == True:
        question = Generate_Questions()
        correctAnswer = Generate_Correct_Answer(question)
        AnswerCoord.clear()
        loops = 0
        subtractingFloorLife = False
        roundOver = False
    

    if roundOver == False:
        #displaying all the possible answers
        Add_AnswerCoord(loops, correctAnswer)
        Answer_Movement(AnswerCoord)
        
        if subtractingFloorLife == False:
            if Check_Floor(correctAnswer) == True:
                status = "floor"
                lives -= 1
                subtractingFloorLife = True
                roundOver = True

    #checks if lives = 0
    if Check_Lives0(lives) == True:
        pygame.time.delay(500)
        Game_Over()
        
        
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                status = Mouse_Click(mouse_pos, correctAnswer)
                if status == "correct" or status == "floor":
                    if status == "correct":
                        score += 1
                    roundOver = True
            '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if Check_Lives0(lives) == True:
                        print('yes')
                        Play_Again()
                        '''
                    
    pygame.display.flip()
    loops += 1
    clock.tick(50)
