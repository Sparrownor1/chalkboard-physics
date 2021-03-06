from math import sqrt

g = 9.8 #(meters per second) per second
accelFactor = 1 #adjust this via testing

class Ball:
    def __init__(self, x, y, r, vx, vy):
        self.position = (x, y)
        self.velocity = (vx, vy)
        self.radius = r


#return the m and b of a line that caused a collision or NONE if no collision took place
def isCollision(lines, ball):
    for line in lines:
        (startX, startY, endX, endY) = line
        m = (endY - startY)/(endX - startX)
        b = startY - m*startX
        (x0, y0) = ball.position
        xCoordOfMinDist = (x0 + m*(y0 - b))/(1 + m**2)
        yCoordOfMinDist = m*xCoordOfMinDist + b
        minDist = sqrt((x0 - xCoordOfMinDist)**2 + (y0 - yCoordOfMinDist)**2)
        if minDist <= ball.radius:
            return (m, b)
    return None

#return the x and y components of the vector which goes normal from the line y = mx + b 
#and goes to the point x0 y0
#the vector points in the direction STARTING from the line and pointing TO x0, y0
def getNormalVector(x0, y0, m, b):
    x = (x0 + m*(y0 - b))/(1 + m**2)
    y = m*x + b
    return (x0 - x, y0 - y)


#destructvie new ballPX, ballPY, ballVX, ballVY after delta T time has passed
def takeStep(ball, lines, deltaT):
    #calling isCollision method to check for intersection
    (px, py) = ball.position
    (vx, vy) = ball.velocity
    newPxTest = px + deltaT * vx
    newPyTest = py + deltaT * vy
    ball.position = (newPxTest, newPyTest)
    isCollisionResult = isCollision(lines, ball)
    if isCollisionResult != None:
        ball.position = (px, py) #revert to original posotion of normal updating caused a collision
        xVChange, yVChange = getNormalVector(px, py, isCollisionResult[0], isCollisionResult[1])
        ball.velocity[0] += xVChange*accelFactor
        ball.velocity[1] += yVChange*accelFactor
        ball.position[0] += deltaT*ball.velocity[0]
        ball.position[1] += deltaT*ball.velocity[1]
    else:
        #acceleration due to gravity
        ball.velocity[1] -= g*deltaT