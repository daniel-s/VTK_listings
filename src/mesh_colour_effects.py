#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vtk

#####################
#  Create geometry  #
#####################

points = vtk.vtkPoints()
cells = vtk.vtkCellArray()
mesh = vtk.vtkPolyData()

# Create points.
points.InsertNextPoint( (0.0, 0.0, 0.0) )
points.InsertNextPoint( (1.0, 0.0, 0.0) )
points.InsertNextPoint( (1.0, 1.0, 0.0) )
points.InsertNextPoint( (0.0, 1.0, 0.0) )
points.InsertNextPoint( (0.5, 0.5, 0.0) )

# These node numbers will be used to define
# all the triangle cells in the mesh.
triangle_nodes = [
    [0, 1, 4],
    [1, 2, 4],
    [2, 3, 4],
    [3, 0, 4]
]

# Generate the cells from the above lists.
for node_list in triangle_nodes:
    tri = vtk.vtkTriangle()
    for i, node_id in enumerate(node_list):
        tri.GetPointIds().SetId(i, node_id)

    cells.InsertNextCell(tri)

# Set the geometry to the polygon object.
mesh.SetPoints(points)
mesh.SetPolys(cells)

# Generate the values for the nodes.
node_data = vtk.vtkDoubleArray()
node_data.SetNumberOfComponents(1)

node_data.InsertNextTuple([5.0])
node_data.InsertNextTuple([5.0])
node_data.InsertNextTuple([7.5])
node_data.InsertNextTuple([5.0])
node_data.InsertNextTuple([6.5])

mesh.GetPointData().SetScalars(node_data)

# Generate the values for the cells.
cell_data = vtk.vtkDoubleArray()
cell_data.SetNumberOfComponents(1)

cell_data.InsertNextTuple([0.0])
cell_data.InsertNextTuple([0.0])
cell_data.InsertNextTuple([0.5])
cell_data.InsertNextTuple([1.0])

mesh.GetCellData().SetScalars(cell_data)

# Note: The mesh is the same for each render, the
# differences are in the lookup tables used for
# each example.

################################
#  Setup the polydata mappers  #
################################

mesh_mapper_1 = vtk.vtkPolyDataMapper()
mesh_mapper_2 = vtk.vtkPolyDataMapper()
mesh_mapper_3 = vtk.vtkPolyDataMapper()
mesh_mapper_4 = vtk.vtkPolyDataMapper()

mesh_mapper_1.SetInputData(mesh)
mesh_mapper_2.SetInputData(mesh)
mesh_mapper_3.SetInputData(mesh)
mesh_mapper_4.SetInputData(mesh)

mesh_mapper_1.SetUseLookupTableScalarRange(True)
mesh_mapper_2.SetUseLookupTableScalarRange(True)
mesh_mapper_3.SetUseLookupTableScalarRange(True)
mesh_mapper_4.SetUseLookupTableScalarRange(True)

# This can also be used if you want to manually set
# the scalar range in the mapper, independently of
# the lookuptable.
# It is ignored if
# .SetUseLookupTableScalarRange(True) is used.
# mesh_mapper.SetScalarRange(5, 6.5)

##########################
#  Create lookup tables  #
##########################

"""
The first 3 lookup tables will have a table range set
to [5.0, 6.5]. The colours and how the table is
set will be different between the 4.
"""

lut_1 = vtk.vtkLookupTable()
lut_2 = vtk.vtkLookupTable()
lut_3 = vtk.vtkLookupTable()
lut_4 = vtk.vtkLookupTable()
lut_1.SetTableRange(5.0, 7.5)
lut_2.SetTableRange(5.0, 7.5)
lut_3.SetTableRange(5.0, 7.5)
lut_4.SetTableRange(0.0, 1.0)

## Creating lut_1
# lut_1 will just use the default settings.
lut_1.Build()
mesh_mapper_1.SetLookupTable(lut_1)

## Creating lut_2
# The default is a full RGB spectrum to create gradients.
# Fixing the hue and sat, varying the value, allows the
# use of darkness/brightness alone to show magnitude.
lut_2.SetHueRange(0.5, 0.5)
lut_2.SetSaturationRange(1.0, 1.0)
lut_2.SetValueRange(0.25, 1.0)
lut_2.Build()
mesh_mapper_2.SetLookupTable(lut_2)

## Creating lut_3
# Creating gradients from developer provided colours
# via a vtkColorTransferFunction.
no_of_colours = 256
lut_3.SetNumberOfColors(no_of_colours)

ctransfer = vtk.vtkColorTransferFunction()
ctransfer.AddRGBPoint(0.0, 1.0, 0.25, 0.0) # Orange
ctransfer.AddRGBPoint(0.5, 1.0, 0.00, 0.0) # Red
ctransfer.AddRGBPoint(1.0, 1.0, 0.95, 0.95) # White

for i in range(no_of_colours):
    new_colour = ctransfer.GetColor(i / float(no_of_colours))
    lut_3.SetTableValue(i, *new_colour)

lut_3.Build()
mesh_mapper_3.SetLookupTable(lut_3)

## Create lut_4
# lut_4 is different, it will also use the .SetTableValue() method
# as above, but will display categorial data. Cell
# values of 0.0, 0.5, and 1.0 will be used to display
# red, amber (yellow), green. This shows the use of a custom
# lookup table to display categorical data.

# N is the number of categories.
lut_4.SetNumberOfColors(3)

lut_4.SetTableValue(0, 1.0, 0.0, 0.0) # Red
lut_4.SetTableValue(1, 1.0, 0.75, 0.0) # Amber
lut_4.SetTableValue(2, 0.0, 1.0, 0.0) # Green

lut_4.SetAnnotation(0.0, "Red")
lut_4.SetAnnotation(0.5, "Amber")
lut_4.SetAnnotation(1.0, "Green")

lut_4.Build()
mesh_mapper_4.SetLookupTable(lut_4)
# NOTE: The mesh features both cell and node data.
# The default is to visualise the float data. In this
# case it is therefore necessary to tell the mapper to
# use the cell data associated with the mesh.
mesh_mapper_4.SetScalarModeToUseCellData()


##########################################
#  Creating the vtkActors and rendering  #
##########################################

mesh_actor_1 = vtk.vtkActor()
mesh_actor_2 = vtk.vtkActor()
mesh_actor_3 = vtk.vtkActor()
mesh_actor_4 = vtk.vtkActor()
mesh_actor_1.SetMapper(mesh_mapper_1)
mesh_actor_2.SetMapper(mesh_mapper_2)
mesh_actor_3.SetMapper(mesh_mapper_3)
mesh_actor_4.SetMapper(mesh_mapper_4)

bar_1 = vtk.vtkScalarBarActor()
bar_2 = vtk.vtkScalarBarActor()
bar_3 = vtk.vtkScalarBarActor()
bar_4 = vtk.vtkScalarBarActor()
# bar_4 is categorical, so should not have
# labels. Instead using annotations from lut_4.
bar_4.SetNumberOfLabels(0)
# The default fonts for annotations are not the same as
# for the default labels. Need adjusting.
bar_4.GetAnnotationTextProperty().SetFontSize(24)

bar_1.SetLookupTable(lut_1)
bar_2.SetLookupTable(lut_2)
bar_3.SetLookupTable(lut_3)
bar_4.SetLookupTable(lut_4)

renderer_1 = vtk.vtkRenderer()
renderer_2 = vtk.vtkRenderer()
renderer_3 = vtk.vtkRenderer()
renderer_4 = vtk.vtkRenderer()

renderer_1.SetViewport( (0.0, 0.5, 0.5, 1.0) )
renderer_2.SetViewport( (0.5, 0.5, 1.0, 1.0) )
renderer_3.SetViewport( (0.5, 0.0, 1.0, 0.5) )
renderer_4.SetViewport( (0.0, 0.0, 0.5, 0.5) )

renderer_1.AddActor(bar_1)
renderer_2.AddActor(bar_2)
renderer_3.AddActor(bar_3)
renderer_4.AddActor(bar_4)

renderer_1.AddActor(mesh_actor_1)
renderer_2.AddActor(mesh_actor_2)
renderer_3.AddActor(mesh_actor_3)
renderer_4.AddActor(mesh_actor_4)

window = vtk.vtkRenderWindow()
window.AddRenderer(renderer_1)
window.AddRenderer(renderer_2)
window.AddRenderer(renderer_3)
window.AddRenderer(renderer_4)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

window.SetSize(1000, 1000)
window.Render()
interactor.Start()
