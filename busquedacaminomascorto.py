#!/usr/bin/env python
#
#       iaImplementacion.py
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

import pdb
from math import sqrt

(ALGORITMO_A_ASTERISCO, ALGORITMO_PRIMERO_EL_MEJOR) = range(2)

class Arbol():
    """
        Una classe que imite el comportamiento de un arbol
    """
    def __init__(self, raiz, objetivo, obstaculos, tamano):
        self.raiz = raiz
        self.objetivo = objetivo
        self.obstaculos = obstaculos
        self.tamano = tamano
        self.nodos_padres = {raiz:[]}

    def getHijos(self, nodo):
        hijos = []
        listaTest = (-1, 0, 1)
        for x in listaTest:
            for y in listaTest:
                if y == 0 and x == 0:
                    continue
                nuevo_nodo_x = nodo[0] + x
                nuevo_nodo_y = nodo[1] + y
                nuevo_nodo = (nuevo_nodo_x, nuevo_nodo_y)
                if (0 <= nuevo_nodo_x <= self.tamano-1 and
                        0 <= nuevo_nodo_y <= self.tamano-1 and
                        nuevo_nodo not in self.obstaculos):


                    if self.addNodoPadres(nodo, nuevo_nodo):
                        hijos.append(nuevo_nodo)
        return hijos

    def addNodoPadres(self, padre, nodo):
        if nodo in self.nodos_padres:
            return False

        nodo_padres = []
        nodo_padres.extend(self.nodos_padres[padre])
        nodo_padres.append(padre)
        self.nodos_padres[nodo] = nodo_padres

        return True

    def getPadres(self, nodo):
        return self.nodos_padres[nodo]

class busqueda():
    def __init__(self, arbol):
        self.abierta = [arbol.raiz]
        self.cerrada = []
        self.arbol = arbol

    def hacer_busqueda(self, typo_busqueda):
        print "==============================\nSearching pass..."
        #pdb.set_trace()
        while len(self.abierta) > 0:
            nodo = self.abierta[0]
            self.cerrada.append(nodo)
            self.abierta.remove(nodo)

            if nodo == self.arbol.objetivo:
                print "Largo del camino: %s" %(len(self.arbol.getPadres(nodo)))
                print "Numero de nodos expendidos: %s" %(len(self.arbol.nodos_padres.items()))
                return self.arbol.getPadres(nodo)

            hijos =  self.arbol.getHijos(nodo)

            self.abierta.extend(hijos)
            self.heuristica(typo_busqueda)


        print "Ningun camino encontratdo\nNumero de nodos expendidos: %s" %(len(self.arbol.nodos_padres.items()))
        return []

    def heuristica(self, typo_busqueda):
        tmpList = []

        #La fonccion equivalente a la funccion G en el algoritmo A*
        def distancia_hasta_el_nodo(arbol, nodo):
             return len(arbol.getPadres(nodo))


        #La funccion equivalente a la funccion H en el algoritmo A*
        def distancia_directa(nodo, objetivo):
            #Gracias pitagoras
            return sqrt((nodo[0] - objetivo[0]) ** 2 + (nodo[1] - objetivo[1])\
                        ** 2)

        tmpList.extend(self.abierta)
        i = 0
        for nodo in tmpList:
            if typo_busqueda == ALGORITMO_A_ASTERISCO:
                #En A* f = h + g
                numero_heuristica = distancia_directa(nodo, self.arbol.objetivo)+\
                                   distancia_hasta_el_nodo(self.arbol, nodo)
                tmpList[i] = [numero_heuristica, nodo]
            elif typo_busqueda == ALGORITMO_PRIMERO_EL_MEJOR:
                #En primero el mejor f = h
                numero_heuristica = distancia_directa(nodo, self.arbol.objetivo)
                tmpList[i] = [numero_heuristica, nodo]
            i+=1
        tmpList.sort()
        i = 0
        for nodo in tmpList:
            self.abierta[i] = nodo[1]
            i+=1
