import csv
import io  # Asegúrate de importar la biblioteca io
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        cantidad = request.POST['cantidad']
        Producto.objects.create(nombre=nombre, precio=precio, cantidad=cantidad)
        return redirect('listar_productos')
    return render(request, 'crear.html')

def editar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.precio = request.POST['precio']
        producto.cantidad = request.POST['cantidad']
        producto.save()
        return redirect('listar_productos')
    return render(request, 'editar.html', {'producto': producto})

def eliminar_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'eliminar.html', {'producto': producto})

def exportar_productos(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Precio', 'Cantidad'])

    for producto in Producto.objects.all():
        writer.writerow([producto.nombre, producto.precio, producto.cantidad])

    return response

def importar_productos(request):
    if request.method == 'POST' and request.FILES['file']:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return HttpResponse('El archivo no es un CSV')
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)  # saltar la fila de encabezado
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = Producto.objects.update_or_create(
                nombre=column[0],
                precio=column[1],
                cantidad=column[2],
            )
        return redirect('listar_productos')
    return render(request, 'importar.html')
