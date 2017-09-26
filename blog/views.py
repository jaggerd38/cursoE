from django.shortcuts import render, render, get_object_or_404, redirect
from django.utils import timezone
from .models import Publicacion
from .forms import PostForm
# Create your views here.
def listar_pub(request):
    pub = Publicacion.objects.filter(fecha_publicacion__lte = timezone.now()).order_by('fecha_publicacion')

    return render(request, 'blog/listar_pub.html', {'pub':pub})

def detalle_pub(request, pk):
    #pub  Publicacion.objects.filter(pk = pk)
    pub = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'blog/detalle_pub.html', {'p': pub})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            #post.fecha_publicacion = timezone.now()
            post.save()
            return redirect('postear', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Publicacion, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('postear', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Publicacion.objects.filter(fecha_publicacion__isnull=True).order_by('fecha_creacion')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Publicacion, pk=pk)
    post.publicar()
    return redirect('postear', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Publicacion, pk=pk)
    post.delete()
    return redirect('post_list')
