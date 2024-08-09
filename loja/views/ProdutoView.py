from django.shortcuts import render
from loja.models import Produto
from datetime import timedelta, datetime
from django.utils import timezone
def edit_produto_view(request, id=None):
    produtos = Produto.objects.all()
    if id is not None:
        produtos = produtos.filter(id=id)
    produto = produtos.first()
    print(produto)
    context = { 'produto': produto }
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
    