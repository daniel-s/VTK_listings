#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

import vtk

points = vtk.vtkPoints()
elements = vtk.vtkCellArray()

#####################
# These can be set. #
#####################
x0 = -7
y0 = -7
x_max = 7
y_max = 7
stepx = 400
stepy = 400

def input_function(x, y):
    return math.sin(.2*(x**2+y**2))
    #return (x**2+y**2)

deltax = (x_max - x0) / float(stepx)
deltay = (y_max - y0) / float(stepy)

X = int(math.floor( (x_max - x0) / deltax))
Y = int(math.floor( (y_max - y0) / deltay))

# Update the new max figures
x_max = x0 + deltax*X
y_max = y0 + deltay*Y

#########################
# Creating the geometry #
#########################

def get_id(i, j, X):
    return i + (X+1)*j

zvals = []
for j in range(Y+1):
    for i in range(X+1):
        x = x0 + deltax*i
        y = y0 + deltay*j

        z_val = input_function(x, y)
        zvals.append(z_val)
        coord = x, y, z_val
        points.InsertNextPoint(coord)

for j in range(Y):
    for i in range(X):
        quad = vtk.vtkQuad()

        quad.GetPointIds().SetId(0, get_id(i, j, X))
        quad.GetPointIds().SetId(1, get_id(i, j, X)+1)
        quad.GetPointIds().SetId(2, get_id(i, j, X) + (Y+2))
        quad.GetPointIds().SetId(3, get_id(i, j, X) + (Y+1))
        elements.InsertNextCell(quad)

mesh = vtk.vtkPolyData()
mesh.SetPoints(points)
mesh.SetPolys(elements)

###################
# Rendering       #
###################

renderer = vtk.vtkRenderer()
window = vtk.vtkRenderWindow()
window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

window.SetSize(900, 900)

###################
# Mesh Actor      #
###################

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(mesh)
actor = vtk.vtkActor()
actor.SetMapper(mapper)
renderer.AddActor(actor)


###################
# Mesh lookup table
###################
lut = vtk.vtkLookupTable()
lut.SetTableRange(min(zvals), max(zvals))
lut.Build()
mapper.SetLookupTable(lut)
mapper.SetUseLookupTableScalarRange(True)


cell_data = vtk.vtkDoubleArray()
cell_data.SetNumberOfComponents(1)
cell_data.SetName("Height info")

for i in range(len(zvals)):
    cell_data.InsertNextTuple([zvals[i]])
mesh.GetPointData().SetScalars(cell_data)


###################
# Create Axes     #
###################
axes = vtk.vtkCubeAxesActor2D()
norms_generator = vtk.vtkPolyDataNormals()
norms_generator.SetInputData(mesh)
axes.SetInputConnection(norms_generator.GetOutputPort())
axes.SetCamera(renderer.GetActiveCamera())
# Prettify
axes.SetLabelFormat("%6.4g")
axes.GetAxisTitleTextProperty().SetFontSize(240)

# Adding the axes actor.
renderer.AddActor(axes)

####################
# Outline Filter   #
####################
outline_filter = vtk.vtkOutlineFilter()
outline_filter.SetInputConnection(norms_generator.GetOutputPort())
outline_mapper = vtk.vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())
outline_actor = vtk.vtkActor()
outline_actor.SetMapper(outline_mapper)

renderer.AddActor(outline_actor)


#############
# Picking ###
#############
text_container = []
def yolo(first, second):
    print("CellId:", first.GetCellId())
    print("zval:", zvals[first.GetCellId()], "coords:", first.GetPCoords())


    ################
    # Text actor   #
    ################
    text = vtk.vtkTextActor()
    text.SetInput("HI")
    text.SetPosition(0,0)

    global renderer
    global text_container
    # Free any existing text.
    for old_text in text_container:
        renderer.RemoveActor2D(old_text)
    text_container = []
    text_container.append(text)
    # Add new text
    renderer.AddActor2D(text)
    
    import pdb
    pdb.set_trace()
    
pick1 = vtk.vtkCellPicker()
pick1.AddObserver(vtk.vtkCommand.EndPickEvent, yolo)
interactor.SetPicker(pick1)


# Output to STL
def get_stl():
    stl = vtk.vtkSTLWriter()
    stl.SetFileName("stl_out.stl")
    tri_filter = vtk.vtkTriangleFilter()
    tri_filter.SetInputData(mesh)
    stl.SetInputConnection(tri.GetOutputPort())
    stl.Write()

def get_ply():
    ply = vtk.vtkPLYWriter()
    

# Finally engage the window and interactor.
window.Render()
interactor.Start()




