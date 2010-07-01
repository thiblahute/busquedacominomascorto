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

class nodo():
    def __init__(self, datos, seguientesi=None):
        self.datos = datos
        self.seguientes = []

class arboleDeBusquedaA():
    def __init__(self, raiz, objetivo):
        self.abierta = [raiz]
        self.cerrada = []
        self.objetivo = objetivo

    def hacer_busqueda(self):
        while self.abierta:
            nodo = self.abierta[0]
            self.cerrada.append(nodo)

            if nodo == objetivo:
                self.getResultList()
            



    def heuristica(self):
        pass

