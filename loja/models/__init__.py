from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#acima são bibliotecas padrões necessárias do Django, e abaixo nossos models


from .fabricante import Fabricante
from .categoria import Categoria
from .produto import Produto
from .usuario import Usuario
from .carrinho import Carrinho
from .carrinho import CarrinhoItem