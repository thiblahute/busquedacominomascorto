#!/usr/bin/env python
#
#       vistabusqueda.py
#
# Copyright (C) 2010 Thibault Saunier <tsaunier@gnome.org>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

import pygame
import os
import sys
from pygame.locals import *
import random
import time

from busquedacaminomascorto import Arbol, busqueda,\
     ALGORITMO_A_ASTERISCO, ALGORITMO_PRIMERO_EL_MEJOR
class Tablero(object):
    def __init__(self, tamano):
        """
            Crea el tablero
        """

        self.imagenes_tamano = 33
        self.tableroStart_x = 0
        self.tableroStart_y = 100
        self.tamano = tamano

        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.init()
        tamano_ventana = (tamano * self.imagenes_tamano, tamano * self.imagenes_tamano + 100)
        self.ventana = pygame.display.set_mode(tamano_ventana)
        pygame.display.set_caption('Inteligencia Artificial movimientos')

        self.inicio = ()
        self.objetivo = ()
        self.camino = []
        self.obstaculos = []

        self.CargarImagenes()

    def CargarImagenes(self):
        self.cudrado_blanco = pygame.image.load(os.path.join("images", "cudrado_blanco.png"))
        self.cudrado_violet = pygame.image.load(os.path.join("images", "cudrado_violet.png"))
        self.player = pygame.image.load(os.path.join("images", "player.png"))
        self.goal = pygame.image.load(os.path.join("images", "goal.png"))
        self.camino_im = pygame.image.load(os.path.join("images", "camino.png"))
        self.cuadrado_negro = pygame.image.load(os.path.join("images", "cuadrado_negro.png"))
        self.explicacion = pygame.image.load(os.path.join("images", "explicacion.png"))

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

    def _dibujar_explicacion(self):
        self.ventana.blit(self.explicacion, (0, 0))

    def dibujar(self):
        """
            Dibuja el tablero
        """
        self.ventana.fill((0, 0, 0))
        #TODO Permitir de agregar las explicaciones
        self._dibujar_explicacion()

        current_cuadrado = 0
        encontrado = False

        if not self.obstaculos:
            self.obstaculos = self.getObstaculos(self.tamano)

        for x in range(self.tamano):
            for y in range(self.tamano):
                (ventanaX, ventanaY) = self.ConvertVentanaCoord((x, y))
                encontrado = False

                for obs in self.obstaculos:
                    if (x, y) == obs:
                        self.ventana.blit(self.cuadrado_negro, (ventanaX, ventanaY))
                        current_cuadrado = (current_cuadrado+1)%2
                        encontrado = True
                        break

                for obs in self.camino:
                    if (x, y) == obs:
                        self.ventana.blit(self.camino_im, (ventanaX, ventanaY))
                        current_cuadrado = (current_cuadrado+1)%2
                        encontrado = True
                        break

                if (x, y) == self.inicio:
                    self.ventana.blit(self.player, (ventanaX, ventanaY))
                    if not self.camino:
                        current_cuadrado = (current_cuadrado+1)%2
                elif (x, y) == self.objetivo:
                    self.ventana.blit(self.goal, (ventanaX, ventanaY))
                    current_cuadrado = (current_cuadrado+1)%2
                elif current_cuadrado and not encontrado:
                    self.ventana.blit(self.cudrado_violet, (ventanaX, ventanaY))
                    current_cuadrado = (current_cuadrado+1)%2
                elif not encontrado:
                    self.ventana.blit(self.cudrado_blanco, (ventanaX, ventanaY))
                    current_cuadrado = (current_cuadrado+1)%2
            current_cuadrado = (current_cuadrado+1)%2

        pygame.display.flip()

    def hacerBusqueda(self, typo_busqueda):
        if not self.inicio or not self.objetivo:
            print "Tiene que seleccionar una departida y un objetivo"
            return
        arbol = Arbol(self.inicio, self.objetivo, self.obstaculos, self.tamano)
        busquador = busqueda(arbol)

        t = time.clock()
        self.camino = busquador.hacer_busqueda(typo_busqueda)
        print "Tiempo de ejecucion: %s\n\n" %(time.clock() -t)
        self.dibujar()

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
                if e.key is K_RETURN:
                    self.hacerBusqueda(ALGORITMO_A_ASTERISCO)
                if e.key in [K_RSHIFT, K_LSHIFT]:
                    self.hacerBusqueda(ALGORITMO_PRIMERO_EL_MEJOR)
            if e.type is MOUSEBUTTONDOWN:
                self._manejarMouseEvent(e)

    def _manejarMouseEvent(self, event):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        if event.button == 1:
            if not self.inicio:
                self.inicio = self.convertCoordTablero((mouseX, mouseY))
                for testNoObstaculo in self.obstaculos:
                    if self.inicio == testNoObstaculo:
                        self.inicio = []
                self.dibujar()
            elif not self.objetivo:
                self.objetivo = self.convertCoordTablero((mouseX, mouseY))
                if self.objetivo == self.inicio:
                    self.objetivo = ()
                for testNoObstaculo in self.obstaculos:
                    if self.objetivo == testNoObstaculo:
                        self.objetivo = []
                self.dibujar()

        if event.button == 3:
            obstaculo = self.convertCoordTablero((mouseX, mouseY))
            if self.camino:
                self.camino=[]
            if not obstaculo in self.obstaculos:
                if obstaculo == self.inicio:
                    self.inicio = ()
                    self.dibujar()
                elif obstaculo == self.objetivo:
                    self.objetivo = ()
                    self.dibujar()
                else:
                    self.obstaculos.append(obstaculo)
                    self.dibujar()

            else:
                self.obstaculos.remove(obstaculo)
                self.dibujar()

if __name__ == "__main__":
    tablero = Tablero(20)
    tablero.dibujar()
    tablero.CicloPrincipal()
