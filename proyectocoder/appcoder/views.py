from django.http import HttpResponse
from appcoder.models import Curso, Profesor, Estudiante
from appcoder.forms import ProfesorFormulario, EstudianteFormulario, CursoFormulario
from django.shortcuts import render, redirect

# Dependencias para resolver apertura de archivos usando rutas relativas
from proyectocoder.settings import BASE_DIR
import os

def inicio(request):
    return render(request, "appcoder/index.html")

def cursos(request):

    errores = ""

    # Validamos tipo de peticion
    if request.method == "POST":
        # Cargamos los datos en el formulario
        formulario = CursoFormulario(request.POST)

        # Validamos los datos
        if formulario.is_valid():
            # Recuperamos los datos sanitizados
            data = formulario.cleaned_data
            # Creamos el curso
            curso = Curso(nombre=data["nombre"], camada=data["camada"])
            # Guardamos el curso
            curso.save()
        else:
            # Si el formulario no es valido, guardamos los errores para mostrarlos
            errores = formulario.errors

    # Recuperar todos los cursos de la BD
    cursos = Curso.objects.all() # Obtener TODOS los registros de ese modelo
    
    # Creamos el formulario vacio
    formulario = CursoFormulario()
    
    # Creamos el contexto
    contexto = {"listado_cursos": cursos, "formulario": formulario, "errores": errores}
    
    # Retornamos la respuesta
    return render(request, "appcoder/cursos.html", contexto)



def editar_curso(request, id):
    curso = Curso.objects.get(id=id)

    if request.method == "POST":
        formulario = CursoFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data

            curso.nombre = data["nombre"]
            curso.camada = data["camada"]
            curso.save()
            return redirect("coder-cursos")
        else:
            return render(request, "appcoder/editar_curso.html", {"formulario": formulario, "errores": formulario.errors})    

    else:
        formulario = CursoFormulario(initial={"nombre": curso.nombre, "camada": curso.camada})
        return render(request, "appcoder/editar_curso.html", {"formulario": formulario, "errores": ""})


def eliminar_curso(request, id):
    curso = Curso.objects.get(id=id)
    curso.delete()

    return redirect("coder-cursos")


def estudiantes(request):
    errores = ""

    # Validamos tipo de peticion
    if request.method == "POST":
        # Cargamos los datos en el formulario
        formulario = EstudianteFormulario(request.POST)

        # Validamos los datos
        if formulario.is_valid():
            # Recuperamos los datos sanitizados
            data = formulario.cleaned_data
            # Creamos el curso
            estudiante = Estudiante(nombre=data["nombre"], apellido=data["apellido"], email=data["email"])
            # Guardamos el curso
            estudiante.save()
        else:
            # Si el formulario no es valido, guardamos los errores para mostrarlos
            errores = formulario.errors

    # Recuperar todos los cursos de la BD
    estudiantes = Estudiante.objects.all() # Obtener TODOS los registros de ese modelo
    
    # Creamos el formulario vacio
    formulario = EstudianteFormulario()
    
    # Creamos el contexto
    contexto = {"listado_estudiantes": estudiantes, "formulario": formulario, "errores": errores}
    
    # Retornamos la respuesta
    return render(request, "appcoder/estudiantes.html", contexto)



def profesores(request):
    errores = ""

    # Validamos tipo de peticion
    if request.method == "POST":
        # Cargamos los datos en el formulario
        formulario = ProfesorFormulario(request.POST)

        # Validamos los datos
        if formulario.is_valid():
            # Recuperamos los datos sanitizados
            data = formulario.cleaned_data
            # Creamos el curso
            profesor = Profesor(nombre=data["nombre"], apellido=data["apellido"], email=data["email"], profesion=data["profesion"])
            # Guardamos el curso
            profesor.save()
        else:
            # Si el formulario no es valido, guardamos los errores para mostrarlos
            errores = formulario.errors

    # Recuperar todos los cursos de la BD
    profesores = Profesor.objects.all() # Obtener TODOS los registros de ese modelo
    
    # Creamos el formulario vacio
    formulario = ProfesorFormulario()
    
    # Creamos el contexto
    contexto = {"listado_profesores": profesores, "formulario": formulario, "errores": errores}
    
    # Retornamos la respuesta
    return render(request, "appcoder/profesores.html", contexto)

def buscar_curso(request):

    return render(request, "appcoder/busqueda_cursos.html")

def resultados_busqueda_cursos(request):
    nombre_curso = request.GET["nombre_curso"]

    cursos = Curso.objects.filter(nombre__icontains=nombre_curso)
    return render(request, "appcoder/resultados_busquedas_cursos.html", {"cursos": cursos})

def buscar_alumnos(request):

    if request.GET:
        nombre_alumno = request.GET.get("nombre_alumno", "")
        if nombre_alumno == "":
            estudiantes = []
        else:
            estudiantes = Estudiante.objects.filter(nombre__icontains=nombre_alumno)
        return render(request, "appcoder/busqueda_estudiantes.html", {"listado_alumnos": estudiantes})

    return render(request, "appcoder/busqueda_estudiantes.html", {"listado_alumnos": []})


def entregables(request):
    return render(request, "appcoder/entregables.html")


def test(request):
    ruta = os.path.join(BASE_DIR, "appcoder/templates/appcoder/base.html")
    print(BASE_DIR, __file__)
    file = open(ruta)

    return HttpResponse(file.read())