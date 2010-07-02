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
                if (0 <= nuevo_nodo_x <= self.tamano and
                        0 <= nuevo_nodo_y <= self.tamano and
                        nuevo_nodo not in self.obstaculos):


                    if self.addNodoPadres(nodo, nuevo_nodo):
                        hijos.append(nuevo_nodo)
        return hijos

    def addNodoPadres(self, padre, nodo):
        #pdb.set_trace()
        if nodo in self.nodos_padres:
            return False
        nodo_padres = []
        nodo_padres.extend(self.nodos_padres[padre])
        nodo_padres.append(padre)
        self.nodos_padres[nodo] = nodo_padres
        #print "%s, %s" %(nodo, nodo_padres)

        return True

    def getPadres(self, nodo):
        return self.nodos_padres[nodo]

class busquedaA():
    def __init__(self, arbol):
        self.abierta = [arbol.raiz]
        self.cerrada = []
        self.arbol = arbol

    def hacer_busqueda(self):
        print "Searching pass..."
        #pdb.set_trace()
        i = 0
        while len(self.abierta) > 0:
            nodo = self.abierta[0]
            self.cerrada.append(nodo)
            self.abierta.remove(nodo)

            if nodo == self.arbol.objetivo:
                return self.arbol.getPadres(nodo)

            hijos =  self.arbol.getHijos(nodo)

            self.abierta.extend(hijos)

            #tmp = nodo
            #while self.arbol.raiz != tmp:
            #    tmp = self.arbol.getPadre(nodo)
            i+=1

        print "Ningun camino encontratdo %s" %i
        return []

    def heuristica(self, desde, hasta):
        pass

