"""
Author: James Bell
Intro to OOP
Last Edited: 4/29/2019

This program is designed to create p particles and make them move randomly throughout the canvas, changing their colors when they collide.
"""

from cs1graphics import *
from random import choice


class Particle:
    """ Class to describe the particle"""

    def __init__(self, x, y, radius=5, color='red', velocity=0):
        """ initialize values for new particle """

        if x >= 0 and y >= 0 and radius > 0:
            self.x = x
            self.y = y
            self.radius = radius
            self.velocity = velocity

            self.point = None
            self.prevX = None
            self.prevY = None
        else:
            raise ValueError('Invalid value')

        if type(color) == str:
            self.color = color
        else:
            raise TypeError('Invalid type')

    def draw(self, canvas):  # canvas parameter
        """ Method to draw particle on canvas"""
        self.point = Circle(self.radius, Point(self.x, self.y))
        self.point.setFillColor(self.color)
        canvas.add(self.point)

    def move(self, c, d):  # use canvas as parameter
        """ Method to move from old position to new"""
        """ c,d are the new points for x,y """
        point = self.point.getReferencePoint()  # saves previous position
        self.prevX = point.getX()
        self.prevY = point.getY()

        self.x = c
        self.y = d
        self.point.move(c, d)

    def getPosition(self):
        """ Method to retrieve particle's current position"""
        point = self.point.getReferencePoint()
        self.x = point.getX()
        self.y = point.getY()

        position = Point(self.x, self.y)

        return position

    def getPrevious(self):
        """ Method to retrieve particle's previous position"""
        return Point(self.prevX, self.prevY)

    def setVelocity(self, velocity):
        """ set new value to velocity """

        if velocity > 0:
            self.velocity = velocity
        else:
            raise ValueError('Invalid value')

    def getVelocity(self):
        """ Method to retrieve velocity"""
        return self.velocity

    def setPosition(self, x, y):
        """ Method to set initial position"""
        if x > 0 and y > 0:
            self.x = x
            self.y = y
        else:
            raise ValueError('Invalid value')

    def setColor(self, color):
        """ Method to set particle to new color"""
        self.color = color
        self.point.setFillColor(self.color)

    def setRadius(self, radius):
        """ Method to set radius of particle"""

        if radius > 0:
            self.radius = radius
        else:
            raise ValueError('Invalid value')

    def getColor(self):
        return self.color


class WorkSpace:
    """ Class Workspace to initialize canvas, and to move particles along canvas"""

    def __init__(self, p=2, radius=5, color='red', velocity=5):
        """ method to initialize canvas, particles, velocity, and draws particles on canvas """

        if p < 10 or p > 50:
            raise ValueError('Invalid number of particles')

        n = (p * 30 + 60) / 2

        self.paper = Canvas(n, n, 'white', 'Final Project')
        self.velocity = velocity

        """ list of particles creates instance p times given by user """
        self.particles = []

        for x in range(p):  # creates list of particles with ambiguous name
            self.particles.append('p')

        i = 0
        d = 30
        x = 30
        while i < p:
            """ initializes list of particles as instances of Particles and draws them on canvas """
            if i == p - 1:  # i is last element of list
                self.particles[i] = Particle(n - x, d, radius, color, velocity)
                self.particles[i].draw(self.paper)
                break
            else:
                self.particles[i] = Particle(n - x, d, radius, color, velocity)
                self.particles[i + 1] = Particle(x, d, radius, color, velocity)

                self.particles[i].draw(self.paper)
                self.particles[i + 1].draw(self.paper)
                i += 2
                d += 30
                x += 30

    def change_color(self, x):
        """ method to change particle of given index color to blue """
        self.particles[x].setColor('blue')

    def check_collision(self, i, step):
        """ method to check position of index 'i' with the rest of the list """

        if isinstance(self.particles[i], Particle):
            point1 = self.particles[i].getPosition()
            # x = point1.getX()
            # y = point1.getY()

            for q in range(len(self.particles)):
                """ point2 takes value of every Particle in the list """
                point2 = self.particles[q].getPosition()

                if point1.getX() == point2.getX() and point1.getY() == point2.getY() and i != q and step != 0:  # makes sure it's not comparing with itself
                    self.change_color(i)
                    self.change_color(q)  # changes colors of both particles

    def check_edges(self, i, circle):
        """ method to determine particle's position related to edge and move it away if it reaches """
        """ first checks if particle is within bounds, if not it automatically moves it in the opposite direction """
        # BR = bottom right, TL = top left, etc

        BRedge = self.paper.getWidth() - self.velocity - self.particles[i].radius
        TLedge = self.velocity + self.particles[i].radius

        move = 0

        point1 = self.particles[i].getPosition()
        x = point1.getX()
        y = point1.getY()

        if x >= BRedge:
            while move < 10:
                circle.move(((-1) * self.velocity), 0)
                move += self.velocity

        if y >= BRedge:
            while move < 10:
                circle.move(0, ((-1) * self.velocity))
                move += self.velocity

        if x <= TLedge:
            while move < 10:
                circle.move(self.velocity, 0)
                move += self.velocity

        if y <= TLedge:
            while move < 10:
                circle.move(0, self.velocity)
                move += self.velocity

    def displace(self, circle, direction):
        """ Method to displace particle in a given direction for given velocity """
        move = 0

        if direction == 'North':
            while move < 10:  # while statement to move smoothly
                circle.move(0, ((-1) * self.velocity))
                move += self.velocity

        elif direction == 'South':
            while move < 10:
                circle.move(0, self.velocity)
                move += self.velocity

        elif direction == 'East':
            while move < 10:
                circle.move(self.velocity, 0)
                move += self.velocity

        elif direction == 'West':
            while move < 10:
                circle.move(((-1) * self.velocity), 0)
                move += self.velocity

    def move_all(self, steps):
        """ method to move both particles simultaneously 'n' steps """
        possibleDirection = ['North', 'South', 'East', 'West']

        for r in range(steps):
            for i in range(len(self.particles)):
                circle = self.particles[i]  # assign variable to particle to simplify code

                self.check_collision(i, r)
                direction = choice(possibleDirection)  # randomizes direction
                self.check_edges(i, circle)
                self.displace(circle, direction)


def main():
    """ MAIN DRIVER: creates workspace instance and moves particles """

    # num particles; radius = 5; color = red, velocity = 5
    space = WorkSpace(20, 5, 'red', 5)

    space.move_all(50)  # steps = 200

    space.paper.wait()
    space.paper.close()


main()
