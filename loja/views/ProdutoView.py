from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from loja.models import Produto, Fabricante, Categoria
from datetime import timedelta, datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

@login_required

def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    Fabricantes = Fabricante.objects.all()
    Categorias = Categoria.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    produto.preco = "{:.2f}".format(produto.preco).replace(',', '.')
    print(produto)
    context = { 'produto': produto, 'fabricantes': Fabricantes, 'categorias': Categorias}
    return render(request, template_name='produto/produto-edit.html', context=context, status=200)
    
def list_produto_view(request, id=None):
    produto = request.GET.get("produto")
    destaque = request.GET.get("destaque")
    promocao = request.GET.get("promocao")
    categoria = request.GET.get("categoria")
    fabricante = request.GET.get("fabricante")
    dias = request.GET.get("dias")
    produtos = Produto.objects.all()
    if dias is not None:
        now = timezone.now()
        now = now - timedelta(days = int(dias))
        produtos = produtos.filter(criado_em__gte=now)
    if produto is not None:
        produtos = produtos.filter(produto__contains=produto)
    if destaque is not None:
        produtos = produtos.filter(destaque=destaque)
    if promocao is not None:
        produtos = produtos.filter(promocao=promocao)
    if categoria is not None:
        produtos = produtos.filter(categoria__categoria=categoria)
    if fabricante is not None:
        produtos = produtos.filter(fabricante__fabricante=fabricante)
    context = { 'produtos': produtos }
    return render(request, template_name='produto/produto.html', context=context, status=200)

def edit_produto_postback(request, id=None):
    if request.method == 'POST':
        id = request.POST.get("id")
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        preco = request.POST.get("preco")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")
        print("postback")
        print(id)
        print(produto)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        print(preco)
        try:
            obj_produto = Produto.objects.filter(id=id).first()
            obj_produto.produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
            if (preco is not None) and (preco != ""):
                obj_produto.preco = preco
            obj_produto.save()
            print("Produto %s salvo com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto %s" % e)
    return redirect("/produto")

def details_produto_view(request, id=None):
    produtos = Produto.objects.all()
    Categorias = Categoria.objects.all()
    Fabricantes = Fabricante.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    produto.preco = "{:.2f}".format(produto.preco).replace(',', '.')
    print(produto)
    context = {'produto': produto, 'categorias': Categorias, 'fabricantes': Fabricantes}
    return render(request, template_name='produto/produto-details.html', context=context, status=200)

def delete_produto_view(request, id=None):
    produtos = Produto.objects.all()
    Categorias = Categoria.objects.all()
    Fabricantes = Fabricante.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    produto.preco = "{:.2f}".format(produto.preco).replace(',', '.')
    print(produto)
    context = {'produto': produto, 'fabricantes': Fabricantes, 'categorias': Categorias}
    return render(request, template_name='produto/produto-delete.html', context=context, status=200)

def delete_produto_postback(request, id=None):
    if request.method == 'POST':
        id = request.POST.get("id")
        produto = request.POST.get("produto")
        print("postback-delete")
        print(id)
        try:
            Produto.objects.filter(id=id).delete()
            print("Produto %s excluído com sucesso" % produto)
        except Exception as e:
            print("Erro salvando edição de produto: %s" % e)
    return redirect("/produto")

def create_produto_view(request, id=None):
    if request.method == 'POST':
        produto = request.POST.get("Produto")
        destaque = request.POST.get("destaque")
        promocao = request.POST.get("promocao")
        msgPromocao = request.POST.get("msgPromocao")
        categoria = request.POST.get("CategoriaFk")
        fabricante = request.POST.get("FabricanteFk")
        preco = request.POST.get("preco")
        image = request.POST.get("image")
        print("postback-create")
        print(produto)
        print(destaque)
        print(promocao)
        print(msgPromocao)
        print(preco)
        print(image)
        try:
            obj_produto = Produto()
            obj_produto.produto = produto
            obj_produto.destaque = (destaque is not None)
            obj_produto.promocao = (promocao is not None)
            if msgPromocao is not None:
                obj_produto.msgPromocao = msgPromocao
            obj_produto.preco = 0
            if (preco is not None) and (preco != ""):
                obj_produto.preco = preco
            obj_produto.categoria = Categoria.objects.filter(id=categoria).first()
            obj_produto.fabricante = Fabricante.objects.filter(id=fabricante).first()
            obj_produto.criado_em = timezone.now()
            obj_produto.alterado_em = obj_produto.criado_em
            if request.FILES is not None:
                num_files = len(request.FILES.getlist('image'))
                if num_files > 0:
                    imagefile = request.FILES['image']
                    print(imagefile)
                    fs = FileSystemStorage()
                    filename = fs.save(imagefile.name, imagefile)
                    if (filename is not None) and (filename != ""):
                        obj_produto.image = filename
            obj_produto.save()
            print("Produto %s salvo com sucesso" % produto)
        except Exception as e:
            print("Erro inserindo produto: %s" % e)
        return redirect("/produto")
    else:
        Categorias = Categoria.objects.all()
        Fabricantes = Fabricante.objects.all()
        context = {'categorias': Categorias, 'fabricantes': Fabricantes}
        return render(request, template_name='produto/produto-create.html', context=context, status=200)