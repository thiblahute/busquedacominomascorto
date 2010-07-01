#! /usr/bin/env python
import pygame
import os
import sys
from pygame.locals import *
import random

class Tablero(object):
    def __init__(self, tamano):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.init()
        self.imagenes_tamano = 33
        tamano_ventana = (tamano * self.imagenes_tamano, tamano * self.imagenes_tamano + 100)
        self.ventana = pygame.display.set_mode(tamano_ventana)
        self.tableroStart_x = 0
        self.tableroStart_y = 100
        pygame.display.set_caption('Inteligencia Artificial movimientos')
        self.actual = ()
        self.fin = ()
        self.obstaculos = []
        self.tamano = tamano

        self.CargarImagenes()

    def CargarImagenes(self):
        self.cudrado_blanco = pygame.image.load(os.path.join("images", "cudrado_blanco.png"))
        self.cudrado_violet = pygame.image.load(os.path.join("images", "cudrado_violet.png"))
        self.player = pygame.image.load(os.path.join("images", "player.png"))
        self.goal = pygame.image.load(os.path.join("images", "goal.png"))
        self.cudrado_negro = pygame.image.load(os.path.join("images", "cudrado_negro.png"))

    def ConvertVentanaCoord(self, chessSquareTuple):
        (row, col) = chessSquareTuple
        ventanaX = self.tableroStart_x + col*self.imagenes_tamano
        ventanaY = self.tableroStart_y + row*self.imagenes_tamano
        return (ventanaX, ventanaY)

    def convertCoordTablero(self, ventanaPositionTuple):
        (X, Y) = ventanaPositionTuple
        row = (Y-self.tableroStart_y) / self.imagenes_tamano
        col = (X-self.tableroStart_x) / self.imagenes_tamano
        return (row, col)

    def getObstaculos(self, numero_obstaculos):
        obstaculos = []
        verifList = []

        def testVerifList(listToTest):
            for i in verifList:
                if listToTest[0] in [i[0], i[0]+1, i[0]-1]\
                    and listToTest[1] in [i[1], i[1]+1, i[1]-1]:
                    return False
            return True

        random0 = 1
        random1 = 2
        safe = 0
        for i in range(numero_obstaculos):
            while not testVerifList([random0, random1]) and safe != 15:
                random0 = random.randrange(1, numero_obstaculos)
                random1 = random.randrange(1, numero_obstaculos)
                safe+=1
            if safe != 15:
                verifList.append([random0, random1])
                obstaculos.append((random0, random1))
            safe = 0

        return obstaculos

    def _dibujar_explicaciones(self):
        rectangulo = pygame.Rect(25, 10, 300, 90)
        pygame.draw.rect(self.ventana, pygame.Color('gray'), rectangulo)

        msgs = [
            'Clickear isquierda una vez para poner el player y una seconda vez para poner el objetivo',
            'Click isquirda para poner nuevos ostaculos'
        ]

        font = pygame.font.SysFont('arial', 16)

        for i, msg in enumerate(msgs):
            rendered = font.render(msg, True, Color('white'))
            self.ventana.blit(rendered, rectangulo.move(10, i * rendered.get_height()))

    def dibujar(self):
        self.ventana.fill((0, 0, 0))
        #TODO Permitir de agregar las explicaciones
        #self._dibujar_explicaciones()

        current_cuadrado = 0
        obstacBool = False

        if not self.obstaculos:
            self.obstaculos = self.getObstaculos(self.tamano)

        for r in range(self.tamano):
            for c in range(self.tamano):
                (ventanaX, ventanaY) = self.ConvertVentanaCoord((r, c))
                for obs in self.obstaculos:
                    if (r, c) == obs:
                        self.ventana.blit(self.cudrado_negro, (ventanaX, ventanaY))
                        current_cuadrado = (current_cuadrado+1)%2
                        obstacBool = True
                if (r, c) == self.actual:
                    self.ventana.blit(self.player, (ventanaX, ventanaY))
                    current_cuadrado = (current_cuadrado+1)%2
                elif (r, c) == self.fin:
                    self.ventana.blit(self.goal, (ventanaX, ventanaY))
                    current_cuadrado = (current_cuadrado+1)%2
                elif current_cuadrado and not obstacBool:
                    self.ventana.blit(self.cudrado_violet, (ventanaX, ventanaY))
                    current_cuadrado = (current_cuadrado+1)%2
                elif not obstacBool:
                    self.ventana.blit(self.cudrado_blanco, (ventanaX, ventanaY))
                    current_cuadrado = (current_cuadrado+1)%2
                obstacBool = False

            current_cuadrado = (current_cuadrado+1)%2
        pygame.display.flip()

    def CicloPrincipal(self):
        #test function
        pygame.event.set_blocked(MOUSEMOTION)
        while True:
            e = pygame.event.wait()
            if e.type is QUIT:
                return
            if e.type is KEYDOWN:
                if e.key is K_ESCAPE:
                    pygame.quit()
                    return
            if e.type is MOUSEBUTTONDOWN:
                self._manejarMouseEvent(e)

    def _manejarMouseEvent(self, event):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        if event.button == 1:
            if not self.actual:
                self.actual = self.convertCoordTablero((mouseX, mouseY))
                for testNoObstaculo in self.obstaculos:
                    if self.actual == testNoObstaculo:
                        self.actual = []
                self.dibujar()

            elif not self.fin:
                self.fin = self.convertCoordTablero((mouseX, mouseY))
                for testNoObstaculo in self.obstaculos:
                    if self.fin == testNoObstaculo:
                        self.fin = []
                self.dibujar()
        if event.button == 3:
            obstaculo = self.convertCoordTablero((mouseX, mouseY))
            if not obstaculo in self.obstaculos:
                self.obstaculos.append(obstaculo)
                self.dibujar()
            else:
                self.obstaculos.remove(obstaculo)
                self.dibujar()

if __name__ == "__main__":
    tablero = Tablero(20)
    tablero.dibujar()
    tablero.CicloPrincipal()

