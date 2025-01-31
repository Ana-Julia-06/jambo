from django.shortcuts import render, get_object_or_404, redirect
from loja.models import Produto, Carrinho, CarrinhoItem, Usuario
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone

#função para add item ao carrinho

def create_carrinhoitem_view(request, produto_id=None):
    print ('create_carrinhoitem_view')
    produto = get_object_or_404(Produto, pk=produto_id)
    if produto:
        print('produto: ' + str(produto.id))

    #tenta pegar o carrinho da sessão ou cria um novo
    carrinho_id = request.session.get('carrinho_id')
    print('carrinho: ' + str(carrinho_id))
    carrinho = None
    if carrinho_id:
        #se o carinho já estiver na sessão, tentamos obter o carrinho
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        print(carrinho)
        print('carrinho1: ' + str(carrinho.id))
        hoje = datetime.today().date()
        #caso queira definir uma expiração do carrinho
        if carrinho.criado_em.date() != hoje:
            #se não for de hoje, cria um novo
            carrinho = Carrinho.objects.create()
            #armazena o id do carrinho na sessão
            request.session['carrinho_id'] = carrinho.id
            print ('novo carrinho: ' + str(carrinho.id))
    else:
        #se o carrinho não existir na sessão, cria um novo
        carrinho = Carrinho.objects.create()
        #armazena o id do carrinho na sessão
        request.session['carrinho_id'] = carrinho.id
        print('carrinho2: ' + str(carrinho.id))
    #verifica se o produto ja existe no carrinho do usuario
    carrinho_item = CarrinhoItem.objects.filter(carrinho=carrinho, produto=produto).first()
    if carrinho_item:
        #se o produto já estiver no carrinho, apenas aumenta a quantidade
        carrinho_item.quantidade += 1
        print('item de carrinho: Acrescentou 1 item do produto ' + str(carrinho_item.id))
    else:
        #se o produto não estiver no carrinho, cria um novo item dentro dele
        carrinho_item = CarrinhoItem.objects.create(
            carrinho=carrinho,
            produto=produto,
            quantidade=1,
            preco=produto.preco
        )
        print('item de carrinho: Acrescentou o produto ' + str(carrinho_item.id))
    carrinho_item.save()
    print('item de carrinho salvo: ' + str(carrinho_item.id))
    return redirect('/carrinho')

#função para exibir itens do carrinho

def list_carrinho_view(request):
    print('list_carrinho_view')
    carrinho = None
    carrinho_item = []
    #tenta pegar o carrinho da sessão ou cria um novo
    carrinho_id = request.session.get('carrinho_id')
    if carrinho_id:
        print('carrinho: ' + str(carrinho_id))
        #obtem o carrinho do usuario
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        print('Data do carrinho: ' + str(carrinho.criado_em))
        carrinho_item = None
        #verifica se o produto já existe no carrinho do usuário
        carrinho_item = CarrinhoItem.objects.filter(carrinho_id=carrinho_id)
        if carrinho_item:
            print('itens de carrinho encontrado ' + str(carrinho_item))
    context = {
        'carrinho': carrinho,
        'itens': carrinho_item
    }
    return render(request, 'carrinho/carrinho-listar.html', context=context)

#função para confirmar a compra, login obrigatorio

@login_required
def confirmar_carrinho_view(request):
    print('confirmar_carrinho_view')
    carrinho = None
    # Tenta pegar o carrinho da sessão ou cria um novo
    carrinho_id = request.session.get('carrinho_id')
    if carrinho_id:
        print('carrinho: ' + str(carrinho_id))
        # Obtem o carrinho do usuario
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        if carrinho:
            try:
                usuario = request.user 
                print('Usuario: ' + str(usuario))
                carrinho.user = usuario
                carrinho.situacao = 1
                carrinho.confirmado_em = timezone.make_aware(datetime.today())
                carrinho.save()
                print('Carrinho salvo')
            except Exception as e:
                print('Erro ao associar usuário ao carrinho: ', e)
        else:
            print("Carrinho não encontrado!")
    else:
        print("Carrinho não está na sessão.")

    context = {
        'carrinho': carrinho
    }
    return render(request, 'carrinho/carrinho-confirmado.html', context=context)

#função para excluir um item do carrinho

def remover_item_view(request, item_id):
    item = get_object_or_404(CarrinhoItem, id=item_id)
    #verifica se o item pertence ao carrinho do usuario
    carrinho_id = request.session.get('carrinho_id')
    if carrinho_id == item.carrinho.id:
        item.delete()
    return redirect('/carrinho')