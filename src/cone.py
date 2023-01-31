#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# All use of the vtk library requires this import.
import vtk

#######################
#                     #
# Creating the actor. #
#                     #
#######################

# Here cone is the data source. If no values are specified
# default parameters will be assigned.
cone = vtk.vtkConeSource()

# To actually display the primitive shape requires the more
# abstract data source be mapped into a set of graphical primitives
# that can be displayed by the visualisation system of vtk.

# The process is to create a data mapper, then to connect that
# to the cone generator.
data_mapper = vtk.vtkPolyDataMapper()
data_mapper.SetInputConnection(cone.GetOutputPort())

# The output of the data mapper needs to be assigned to an actor
# before additing it to the scene.

actor = vtk.vtkActor()
actor.SetMapper(data_mapper)

#######################
#                     #
# Creating the scene. #
#                     #
#######################

# The window will be created by creating the simplest scene.

# A renderer is needed to take actors and draw them onto the
# window.
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
# The .SetBackground() method takes 3 RGB values 0.0 to 1.0.
renderer.SetBackground(0.0, 0.0, 0.0)

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(500, 500)

window_interactor = vtk.vtkRenderWindowInteractor()
window_interactor.SetRenderWindow(render_window)

window_interactor.Start()

