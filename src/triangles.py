#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import vtk

points = vtk.vtkPoints()
elements_1 = vtk.vtkCellArray()
elements_2 = vtk.vtkCellArray()
mesh_1 = vtk.vtkPolyData()
mesh_2 = vtk.vtkPolyData()

#########################
# Creating the geometry #
#########################

tri = vtk.vtkTriangle()

# Create the same triangle
# First creating the points.
points_a = []
points_a.append( (0.0, 0.0, 0.0) )
points_a.append( (0.0, 1.0, 0.0) )
points_a.append( (1.0, 0.0, 0.0) )

# Assign these points.
[points.InsertNextPoint(point) for point in points_a]

# Then create the tri elements from those points.
for i in range(3):
    tri.GetPointIds().SetId(i, i)

elements_1.InsertNextCell(tri)

mesh_1.SetPoints(points)
mesh_1.SetPolys(elements_1)

mesh_2.SetPoints(points)
mesh_2.SetPolys(elements_1)

cell_data_1 = vtk.vtkDoubleArray()
cell_data_2 = vtk.vtkDoubleArray()
cell_data_1.SetNumberOfComponents(1)
cell_data_2.SetNumberOfComponents(1)

cell_data_1.InsertNextTuple([0.5])
mesh_1.GetCellData().SetScalars(cell_data_1)

cell_data_2.InsertNextTuple([0.0])
cell_data_2.InsertNextTuple([1.0])
cell_data_2.InsertNextTuple([0.5])
mesh_2.GetPointData().SetScalars(cell_data_2)

###################
# Rendering       #
###################

# Create the window.
window = vtk.vtkRenderWindow()
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

# Add the renderers.
render_1 = vtk.vtkRenderer()
render_2 = vtk.vtkRenderer()
# The the renderers as left/right here.
render_1.SetViewport( (0.0, 0.0, 0.5, 1.0) )
render_2.SetViewport( (0.5, 0.0, 1.0, 1.0) )
window.AddRenderer(render_1)
window.AddRenderer(render_2)

window.SetSize(800, 400)

###################
# Mesh Actors     #
###################

map_1 = vtk.vtkPolyDataMapper()
map_2 = vtk.vtkPolyDataMapper()

map_1.SetInputData(mesh_1)
map_2.SetInputData(mesh_2)

act_1 = vtk.vtkActor()
act_2 = vtk.vtkActor()
act_1.SetMapper(map_1)
act_2.SetMapper(map_2)

render_1.AddActor(act_1)
render_2.AddActor(act_2)

render_1.ResetCamera()
render_2.ResetCamera()


###################
# Mesh lookup table
###################
lut = vtk.vtkLookupTable()
lut.SetValueRange(0.0, 1.0)
lut.Build()
map_1.SetLookupTable(lut)
map_2.SetLookupTable(lut)

# Finally engage the window and interactor.
window.Render()
interactor.Start()
