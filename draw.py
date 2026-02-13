from cmu_graphics import *
from cmu_graphics import app
import math
import time
app.performanceMode = True
app.gameOver = False
app.isGameOverTriggered = False

overlay = Rect(0,0,400,400, opacity = 0.5)
app.startY=200
app.shadowOffset = 10


### Time management
app.stepsPerSecond = 60
app.lastTime = time.time()
app.deltaTime = 1/app.stepsPerSecond
app.fps = app.stepsPerSecond

def deltaTime():
    currentTime = time.time()
    app.deltaTime = currentTime - app.lastTime
    app.lastTime = currentTime
    app.deltaTime = max(app.deltaTime, 1 / app.stepsPerSecond)
    return app.deltaTime

def updateFPS():
    if app.deltaTime > 0:
        app.fps = 1/app.deltaTime
    else:
        app.fps = app.stepsPerSecond # Safeguard just in case deltaTime is 0
    return app.fps

### Scene setup
app.gravity=400
app.friction=0 #lower number = lower friction
app.speed = 100

app.shift = app.speed*app.deltaTime

### Player setup
player = Group(
    Rect(0,app.startY,10,5, align = 'center', fill=None)
)

player.add(
    Rect(player.left, player.top, player.width, player.height),
    Circle(player.centerX, player.top, player.width/2),
    Circle(player.centerX, player.bottom, player.width/2)
)
player.centerX = 150
player.bottom = app.startY=200

player.vx = app.speed*.4
player.acceleration = 800
player.vy = 0
player.jumpHeight = 50
player.jumpAmount = 3
player.jumpCount = 0
player.jumpVelocity = math.sqrt(2*app.gravity*player.jumpHeight) * -1
player.currentSurface = None

### Scene setup
bg = Group(
    Rect(0,0,200,200),
    Rect(200,200,200,200),
    Rect(400,0,200,200),
    Rect(600,200,200,200)
)
bg.opacity = 10
shadows = Group()

###Obstacle Management
topPipe = 'top.png'
bottomPipe = 'bottom.png'

pipeSize = 30
def pipe(x,y,top):
    stretchFactor = 2 #how much to stretch the top or the bottom of the pipe
    pipe = Group()
    if top == True:
        pipe.add(Image(topPipe,0,0))
        extraPipe = Image(bottomPipe,pipe.left,pipe.top-pipe.height*stretchFactor)
        extraPipe.height*=stretchFactor
        pipe.add(extraPipe)
        pipe.width = pipeSize
        pipe.height = pipe.width * pipe.height/100
        pipe.left = x
        pipe.bottom = y
    else:
        pipe.add(Image(bottomPipe,0,0))
        extraPipe = Image(topPipe,pipe.left,pipe.top+pipe.height)
        extraPipe.height*=stretchFactor
        pipe.add(extraPipe)
        pipe.width = pipeSize
        pipe.height = pipe.width * pipe.height/100
        pipe.left = x
        pipe.top = y
    return pipe

def createObstacles():
    pair = Group()
    pair.gapX = 400
    pair.gapY = 100
    pair.center = randrange(100,300) #Initial centerY randomization
    pair.add(pipe(0,pair.center-pair.gapY/2,True))
    pair.add(pipe(0,pair.center+pair.gapY/2,False))
    pair.left = 400
    pair.scored = False
    return pair
 
app.obstaclePairs = [createObstacles()]

###app.scoreCounter
app.score= 0

scoreType = 'Score:'
scoreTypeLabel = Label(scoreType, 45, -20, size = 20, font = 'orbitron', bold = True, fill = 'darkslategrey', border = 'white', borderWidth = 0.5, opacity = 0)
scoreTypeLabelShadow = Label(scoreType, scoreTypeLabel.centerX + app.shadowOffset, scoreTypeLabel.centerY + app.shadowOffset, size = scoreTypeLabel.size, font = scoreTypeLabel.font, bold = scoreTypeLabel.bold, opacity = 10)

scoreLabel = Label(app.score,45,45, size = 30, font = 'orbitron', bold = True, fill = 'darkslategrey', border='white', borderWidth = 1)
scoreShadow = Label(app.score, scoreLabel.centerX+app.shadowOffset, scoreLabel.centerY+app.shadowOffset, size = scoreLabel.size, font=scoreLabel.font, bold = scoreLabel.bold, opacity = 10)

scoreGroup=Group(scoreLabel)
scoreGroup.add(scoreTypeLabel)

###Game over screen setup
buttonWidth = 100
buttonHeight = 50
buttonRadius = 15
borderWidth = 1

gameOverText = Group(
Label("Game Over!", 200+app.shadowOffset,200+app.shadowOffset, size=50, font = 'montserrat', bold = True, opacity = 5),
Label("Game Over!", 200,200, size=50, font = 'montserrat', bold = True, fill='red', border = 'black', borderWidth = borderWidth),
)
gameOverText.bottom = 1
gameOverText.visible= False

def Circtangle(left, top, width, height, radius, fill, opacity):
    circtangle = Group(
    Rect(left,top+radius, radius, height-radius*2, fill = fill, opacity = opacity),
    Rect(left +width - radius,top+radius, radius, height-radius*2, fill = fill, opacity = opacity),
    Rect(left+radius, top, width-radius*2, height, fill = fill, opacity = opacity),
    Arc(left+radius,top+radius, radius*2, radius*2, 270, 90, fill = fill, opacity = opacity),
    Arc(left+width-radius,top+radius,radius*2,radius*2, 0, 90, fill = fill, opacity = opacity),
    Arc(left+radius,top+height-radius,radius*2,radius*2, 180, 90, fill = fill, opacity = opacity),
    Arc(left+width-radius,top+height-radius,radius*2,radius*2, 90, 90, fill = fill, opacity = opacity),
    )
    return circtangle

tryAgainButtonShadow=Group(
    Circtangle(0,0,buttonWidth,buttonHeight,buttonRadius, 'black', 1),
    Circtangle(0,0,buttonWidth,buttonHeight,buttonRadius, 'black', 1),
    Circtangle(0,0,buttonWidth,buttonHeight,buttonRadius, 'black', 1),
    Circtangle(0,0,buttonWidth,buttonHeight,buttonRadius, 'black', 1),
)

tryAgainButtonShadow.centerX = 200 + app.shadowOffset
tryAgainButtonShadow.top = 400

tryAgainButton=Group(
    Circtangle(0,0,buttonWidth,buttonHeight,buttonRadius, 'black', 100),
    Circtangle(0 + borderWidth, 0 + borderWidth, buttonWidth - borderWidth*2, buttonHeight-borderWidth*2, buttonRadius-borderWidth, 'white', 100),
    Circtangle(0 + borderWidth, 0 + borderWidth, buttonWidth - borderWidth*2, buttonHeight-borderWidth*2, buttonRadius-borderWidth, 'white', 100),
    Circtangle(0 + borderWidth, 0 + borderWidth, buttonWidth - borderWidth*2, buttonHeight-borderWidth*2, buttonRadius-borderWidth, 'white', 100),
    Label("Try Again?", buttonWidth/2 + app.shadowOffset/4, buttonHeight/2 + app.shadowOffset/4, size = 14, font = 'montserrat', bold = True, opacity = 10),
    Label("Try Again?", buttonWidth/2, buttonHeight/2, size = 14, font = 'montserrat', bold = True, border = 'White', borderWidth = 0.5, fill= 'darkslategrey'),
)

tryAgainButton.visible = False
tryAgainButton.centerX = 200
tryAgainButton.top = 400

tryAgainButtonOverlay=Circtangle(0,0,buttonWidth,buttonHeight,buttonRadius, 'black', 1)
tryAgainButtonOverlay.centerX=200
tryAgainButtonOverlay.top = 400

url = 'trophy.png'
icon = Image(url,0,0)
icon.width = 40
icon.height=40
icon.centerX = 340
icon.centerY = 45

app.highScore = 0
highScoreLabel = Label(app.highScore,370,45, size = 30, font = 'orbitron', bold = True, fill = 'darkslategrey', border='white', borderWidth = 1)

hs = Group(icon, highScoreLabel)

def gameOverScreen():
    gameOverText.visible=True
    tryAgainButton.visible=True

    player.vy += app.gravity * app.deltaTime # Apply gravity to player
    player.centerY += player.vy * app.deltaTime

    if overlay.opacity < 30:
        overlay.opacity *= 1.09
    if gameOverText.bottom < 180:
        if scoreTypeLabel.opacity <100:
            scoreTypeLabel.opacity += 4
        gameOverText.bottom *= 1.2
        scoreLabel.centerY = ogScoreCenterY + gameOverText.bottom + 10
        icon.centerY = ogScoreCenterY + gameOverText.bottom + 7
        highScoreLabel.centerY = ogScoreCenterY + gameOverText.bottom + 10
        scoreTypeLabel.centerY = gameOverText.bottom + 20
        scoreTypeLabelShadow.centerY = gameOverText.bottom + 20 + app.shadowOffset/3
        scoreShadow.centerY = ogScoreCenterY + gameOverText.bottom + app.shadowOffset + 10
        scoreLabel.centerX += 2
        icon.centerX -=1.7
        highScoreLabel.centerX-=1.3
        scoreTypeLabel.centerX +=2
        scoreTypeLabelShadow.centerX +=1.8
        scoreShadow.centerX += 2
    if tryAgainButton.top > 225:
        tryAgainButton.centerY *= 0.98
        tryAgainButtonOverlay.centerY *= 0.98
        tryAgainButtonShadow.centerY = tryAgainButton.centerY + app.shadowOffset
    if overlay.opacity > 30 and gameOverText.bottom >200 and tryAgainButton.top > 225:
        app.isGameOverTriggered = False

### Mouse input handling
app.mouseOnButton = False
app.mousePressed=False

def onMouseMove(x,y):
    if tryAgainButton.visible and tryAgainButton.hits(x,y):
        app.mouseOnButton=True
    else:
        app.mouseOnButton=False

def onMousePress(x,y):
    app.mousePressed=True

    if not app.gameOver:
        app.isDrawing = True
        app.points = []
        app.mouseX, app.mouseY = x,y

def onMouseDrag(x,y):
    app.mouseX, app.mouseY = x,y

def onMouseRelease(x, y):
    app.mousePressed=False
    if app.mouseOnButton and tryAgainButton.visible:
        restartGame()
    else:
        if not app.isGameOverTriggered:
            app.isDrawing = False
            app.mouseX, app.mouseY = None, None
            _addPoint((x,y))
            app.points = []

### Keyboard input handling
app.heldKeys= set()
def onKeyHold(keys):
    if not app.gameOver:
        if 'a' in keys or 'left' in keys:
            player.vx -= player.acceleration*app.deltaTime
        if 'd' in keys or 'right' in keys:
            player.vx +=player.acceleration*app.deltaTime
        app.heldKeys = set(keys)

def onKeyRelease(key):
    if not app.gameOver:
        app.heldKeys.remove(key)
        
def onKeyPress(key):
    if not app.gameOver:
        if (player.currentSurface is not None or player.jumpCount < player.jumpAmount) and key in ('w', 'up', 'space'):
            player.vy = player.jumpVelocity
            player.jumpCount+=1
            player.currentSurface = None

### Collision helpers
def point_line_distance(px,py,x1,y1,x2,y2):
    line_len = distance(x1,y1,x2,y2)
    if line_len == 0:
        return distance(px,py,x1,y1)
    
    t = ((px-x1) * (x2-x1) + (py - y1) * (y2 - y1)) / (line_len*line_len)
    t = max(0, min(1,t))
    proj_x = x1 + t*(x2-x1)
    proj_y = y1 + t*(y2-y1)
    
    return distance(px,py,proj_x,proj_y)

def surface_properties(line):
    dx = line.x2 - line.x1
    dy = line.y2 - line.y1
    line.length = distance(line.x1, line.y1, line.x2, line.y2)
    line.angle = math.atan2(dy, dx)
    line.normal = (dy/line.length, -dx/line.length)
    line.tangent = (dx/line.length, dy/line.length)
    line.left = min(line.x1, line.x2)
    line.right = max(line.x1, line.x2)
    line.top = min(line.y1, line.y2)
    line.bottom = max(line.y1, line.y2)
    return line

### Drawing constants
app.line_resolution = max(1, int(400/app.speed))
   
app.isDrawing = False
app.mouseX = None
app.mouseY = None
app.points = []
app.lineWidth = 2
surfaces = Group(*[surface_properties(line) for line in [
Line(0,app.startY,250,app.startY, lineWidth = app.lineWidth)    
]])

### Drawing helpers
def catmull_point(p0,p1,p2,p3, t): # Catmulll-Rom smoothing
    t2, t3 = t*t, t*t*t
    x0,y0 = p0
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    f1 = -0.5*t3 + t2 - 0.5*t
    f2 = 1.5*t3 - 2.5*t2 + 1
    f3 = -1.5*t3 + 2.0*t2 + 0.5*t
    f4 = 0.5*t3 - 0.5*t2
    x = x0*f1 + x1*f2 + x2*f3 + x3*f4
    y = y0*f1 + y1*f2 + y2*f3 + y3*f4
    return x,y

def _addPoint(point):
    if not app.gameOver:
        app.points.append(point)
        if len(app.points) == 1: # Very first point (just a circle)
            if not app.performanceMode:
                surfaces.add(Circle(point[0], point[1], app.lineWidth / 2))
                shadows.add(Circle(point[0] + app.shadowOffset, 
                point[1] + app.shadowOffset, app.lineWidth/2, 
                opacity = 5))
        elif len(app.points) < 4: # Points 2 & 3
            x1, y1 = app.points[1]
            x2, y2 = app.points[-2]
            if distance(x1,y1,x2,y2) > 0:
                surfaces.add(surface_properties(Line(x1, y1, x2, y2, lineWidth=app.lineWidth)))
                
                if not app.performanceMode:
                    shadows.add(Line(x1 + app.shadowOffset, y1 + app.shadowOffset, 
                    x2 + app.shadowOffset, y2 + app.shadowOffset, 
                    lineWidth = app.lineWidth, opacity=10))
                if app.lineWidth > 5 and not app.performanceMode:
                    surfaces.add(Circle(x1,y1, app.lineWidth/2))
                    shadows.add(Circle(x1 + app.shadowOffset, y1 + app.shadowOffset, 
                    app.lineWidth/2, opacity = 10))
        else: # Once enough points have been stored, interpolate between points
            p0,p1,p2,p3 = app.points[-4:]
            prev = None
            for i in range(app.line_resolution + 1):
                t = i/app.line_resolution
                xi,yi = catmull_point(p0,p1,p2,p3, t)
                if prev and distance(prev[0], prev[1], xi, yi) > 0:
                    surfaces.add(surface_properties(Line(prev[0], prev[1], xi, yi, lineWidth=app.lineWidth)))
                    if not app.performanceMode:
                        shadows.add(Line(prev[0] + app.shadowOffset, prev[1] + app.shadowOffset, 
                        xi + app.shadowOffset, yi + app.shadowOffset, lineWidth = app.lineWidth, 
                        opacity=10))
                        if app.lineWidth > 5:
                            surfaces.add(Circle(prev[0], prev[1], app.lineWidth/2))
                prev = (xi,yi)
            app.points = app.points[-3:]

createObstacles()

###Game States
def gameOver():
    if not app.isGameOverTriggered:
        app.isGameOverTriggered = True
        app.gameOver = True
        app.isDrawing = False

ogScoreCenterY = scoreLabel.centerY
ogScoreCenterX = scoreLabel.centerX
app.ogSpeed = app.speed

def restartGame():
    app.gameOver = False
    app.isGameOverTriggered = False
    overlay.opacity = 0.5
    gameOverText.visible = False
    gameOverText.bottom = 1
    tryAgainButton.visible = False
    tryAgainButtonShadow.top = 400
    tryAgainButton.top=400
    tryAgainButtonOverlay.top=400
    player.centerX = 150
    player.centerY = app.startY
    player.vx = app.speed * 0.3
    player.vy = 0
    player.jumpCount = 0
    player.currentSurface = None
    app.speed = app.ogSpeed
    app.line_resolution = int(400/app.speed)
    for pair in app.obstaclePairs:
        pair.visible = False
        pair.clear()
    app.obstaclePairs.clear()
    app.obstaclePairs.append(createObstacles())
    surfaces.clear()
    shadows.clear()
    surfaces.add(surface_properties(Line(0, app.startY, 250, app.startY, lineWidth=app.lineWidth)))
    app.points = []
    bg.centerX = 200
    app.score= 0
    scoreLabel.centerY = ogScoreCenterY
    scoreShadow.centerY = ogScoreCenterY + app.shadowOffset
    scoreLabel.centerX = ogScoreCenterX
    scoreShadow.centerX = ogScoreCenterX + app.shadowOffset
    scoreGroup.fill = 'darkslategrey'
    scoreLabel.border = 'white'
    scoreLabel.value = app.score
    scoreShadow.value = app.score
    scoreTypeLabel.centerX = 45
    scoreTypeLabel.centerY = -20
    scoreTypeLabelShadow.centerX = 45 + app.shadowOffset/3
    scoreTypeLabelShadow.centerY = -20 + app.shadowOffset/3
    app.heldkeys = set()
    scoreTypeLabel.value = 'Score:'
    scoreTypeLabelShadow.value = 'Score:'
    scoreTypeLabel.opacity = 0
    highScoreLabel.centerX = 370
    icon.centerX = 340
    highScoreLabel.centerY = 45
    icon.centerY = 45
endScreen=Group(overlay,gameOverText,tryAgainButton)
#res = Label(app.line_resolution,200,200)
#speed = Label(rounded(app.speed),300,200)

##### Main
def onStep():
    app.highScore = max(app.score, app.highScore)
    highScoreLabel.value = app.highScore
    app.line_resolution = int(400/app.speed)
    #res.value = app.line_resolution
    #speed.value = rounded(app.speed)
    app.deltaTime = deltaTime()
    
    if player.currentSurface is None:
            player.vy += app.gravity * app.deltaTime # Apply gravity to player
    
    player.centerX += player.vx * app.deltaTime # Update playerposition
    player.centerX = max(player.width/2, min(400-player.width/7, player.centerX))
    
    if app.mouseOnButton:
        if tryAgainButtonOverlay.opacity<8:
            tryAgainButtonOverlay.opacity*=1.2
        if app.mousePressed:
            if tryAgainButtonOverlay.opacity<15:
                tryAgainButtonOverlay.opacity*=1.2
    else:
        if tryAgainButtonOverlay.opacity>1:
            tryAgainButtonOverlay.opacity*=0.9
    
    if 5 <= app.highScore < 10:
        highScoreLabel.fill = gradient('sienna','saddlebrown','rosybrown','burlywood','sienna', start = 'right-bottom')
        highScoreLabel.border = gradient('sienna','saddlebrown','rosybrown','burlywood','sienna', start = 'left-top')
    elif 10 <= app.highScore < 25:
        highScoreLabel.fill = gradient('grey','lightgrey','white','lightgrey','darkgrey','white','darkgrey', start = 'left-top')
        highScoreLabel.border = gradient('grey','lightgrey','white','lightgrey','darkgrey','white','darkgrey', start = 'right-bottom')
    elif 25 <= app.highScore < 50:
        highScoreLabel.fill = gradient('khaki','darkgoldenrod','gold','moccasin','goldenrod', start = 'right-bottom')
        highScoreLabel.border = gradient('khaki','darkgoldenrod','gold','moccasin','goldenrod', start = 'left-top')
    elif app.highScore > 50:
        highScoreLabel.fill = gradient('lightsteelblue','lightcyan','azure','lightsteelblue','steelblue', start = 'right-bottom')
        highScoreLabel.border = gradient('lightsteelblue','lightcyan','azure','lightsteelblue','steelblue', start = 'left-top')

    if 5 <= app.score < 10:
        scoreGroup.fill = gradient('sienna','saddlebrown','rosybrown','burlywood','sienna', start = 'right-bottom')
        scoreLabel.border = gradient('sienna','saddlebrown','rosybrown','burlywood','sienna', start = 'left-top')
        scoreTypeLabel.value = 'Bronze'
        scoreTypeLabelShadow.value = 'Bronze'
    elif 10 <= app.score < 25:
        scoreGroup.fill = gradient('grey','lightgrey','white','lightgrey','darkgrey','white','darkgrey', start = 'left-top')
        scoreLabel.border = gradient('grey','lightgrey','white','lightgrey','darkgrey','white','darkgrey', start = 'right-bottom')
        scoreTypeLabel.value = 'Silver'
        scoreTypeLabelShadow.value = 'Silver'
    elif 25 <= app.score < 50:
        scoreGroup.fill = gradient('khaki','darkgoldenrod','gold','moccasin','goldenrod', start = 'right-bottom')
        scoreLabel.border = gradient('khaki','darkgoldenrod','gold','moccasin','goldenrod', start = 'left-top')
        scoreTypeLabel.value = 'Gold'
        scoreTypeLabelShadow.value = 'Gold'
    elif app.score > 50:
        scoreGroup.fill = gradient('lightsteelblue','azure','lightcyan','lightsteelblue','steelblue', start = 'right-bottom')
        scoreLabel.border = gradient('lightsteelblue','lightcyan','azure','lightsteelblue','steelblue', start = 'left-top')
        scoreTypeLabel.value = 'DIAMOND'
        scoreTypeLabelShadow.value = 'DIAMOND'

    ### Scene Movement
    app.shift = app.speed*app.deltaTime
    surfaces.centerX -= app.shift
    shadows.centerX -= app.shift
    player.centerX -= app.shift
    bg.centerX -= app.shift/1.5 # parralax effect
    
    for pair in app.obstaclePairs:
        if pair.visible:
            pair.centerX -= app.shift
    
    if len(app.obstaclePairs) == 0 or app.obstaclePairs[-1].right <=400 - pair.gapX:
        newObstaclePair = createObstacles()
        app.obstaclePairs.append(newObstaclePair)
    app.obstaclePairs = [pair for pair in app.obstaclePairs if pair.right >0]
    
    for pair in app.obstaclePairs:
        if not app.gameOver and not pair.scored and player.centerX > pair.centerX:
            app.score += 1
            scoreLabel.value = app.score
            scoreShadow.value = app.score
            pair.scored = True
    
    if app.points:
        app.points = [(px-app.shift,py) for px,py in app.points]
    for surface in list(surfaces):
        if surface.right <0:
            surface.visible = False
            #surfaces.remove(surface)
    for shadow in list(shadows):
        if shadow.right <0:
            shadow.visible = False
            #shadows.remove(shadow)
    for pair in app.obstaclePairs:
        if pair.right <0:
            pair.visible = False
            #app.obstaclePairs.remove(pair)
    if bg.centerX <= 0:
        bg.left = 0    
        
    if app.gameOver:
        gameOverScreen()
        if app.speed >0.1:
            app.speed *=0.95
    else:
        app.speed *= 1.0005
        player.centerY += player.vy * app.deltaTime
    
        ### Player physics
        if player.left <0 or player.right > 400 or player.top < 0 or player.bottom > 400:
            gameOver()
        
        for pair in app.obstaclePairs:
            for obstacle in pair:
                if obstacle.hits(player.centerX, player.centerY):
                    player.vx = 0
                    gameOver()
                    
        ### Collision detection
        px, py = player.centerX, player.bottom
        if player.currentSurface is not None:
            surface = player.currentSurface
            line_thickness = getattr(surface, 'lineWidth', 1)
            dist = point_line_distance(px, py, surface.x1, surface.y1, surface.x2, surface.y2)
            if player.hitsShape(surface):
                dx = surface.x2 - surface.x1
                dy = surface.y2 - surface.y1
                length = distance(surface.x1, surface.y1, surface.x2, surface.y2)
                
                if length != 0:
                    normal = surface.normal
                    tangent = surface.tangent
                    t = ((px - surface.x1) * dx + (py - surface.y1) * dy) / (length * length)
                    t = max(0, min(1,t))
                else:
                    normal = (0,-1)
                    tangent = (1,0)
                    t = 0
                vel_along_tangent = player.vx * tangent[0] + player.vy * tangent[1]
                if not app.heldKeys:
                    vel_along_tangent *= (1 - app.friction * app.deltaTime)
                     
                player.vx = vel_along_tangent * tangent[0]
                player.vy = vel_along_tangent * tangent[1]
                nearest_x = surface.x1 + t * dx
                nearest_y = surface.y1 + t * dy
                surface_edge_y = nearest_y + normal[1] * line_thickness / 2
                player.bottom = surface_edge_y
                player.jumpCount = 0
            else:
                player.currentSurface = None

        if player.currentSurface is None:
            for surface in surfaces:
                if isinstance(surface, Line):
                    line_thickness = getattr(surface, 'lineWidth', 1)
                    dist = point_line_distance(px, py, surface.x1, surface.y1, surface.x2, surface.y2)
                    if dist < line_thickness / 2 + 1 or player.hitsShape(surface):
                        dx = surface.x2 - surface.x1
                        dy = surface.y2 - surface.y1
                        length = distance(surface.x1, surface.y1, surface.x2, surface.y2)
                        if length !=0:
                            normal = surface.normal
                            tangent = surface.tangent
                            t = ((px - surface.x1) * dx + (py - surface.y1) * dy) / (length*length)
                            t = max(0, min(1, t))
                        else:
                            normal = (0, -1)
                            tangent = (1, 0)
                            t = 0
                        nearest_x = surface.x1 + t * dx
                        nearest_y = surface.y1 + t * dy
                        
                        vx = px - nearest_x
                        vy = py - nearest_y
                        dot = vx*normal[0] + vy*normal[1]
                        if dot > 0:
                            surface_edge_y = nearest_y + normal[1] * line_thickness / 2
                            player.centerY = surface_edge_y - (player.bottom - player.centerY)
                            player.jumpCount = 0
                            
                        vel_along_tangent = player.vx * tangent[0] + player.vy * tangent[1]
                        if not app.heldKeys:
                            vel_along_tangent *= (1 - app.friction * app.deltaTime)
                        player.vx = vel_along_tangent * tangent[0]
                        player.vy = vel_along_tangent * tangent[1]
                        player.currentSurface = surface
                        break
        
        ### Drawing
        if app.isDrawing and app.mouseX is not None and not app.gameOver:
            x, y = app.mouseX, app.mouseY
            if not app.points:
                _addPoint((x,y))
            else:
                x0, y0 = app.points[-1]
                if math.hypot(x - x0, y - y0) >= max(20/app.line_resolution, 2):
                    _addPoint((x,y))
    
    bg.toBack()
    for pair in app.obstaclePairs:
        pair.toFront()
    shadows.toFront()
    surfaces.toFront()
    endScreen.toFront()
    tryAgainButtonOverlay.toFront()
    scoreLabel.toFront()
    scoreGroup.toFront()
    hs.toFront()
    player.toFront()


cmu_graphics.run()