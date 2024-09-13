from django.contrib import admin

# Register your models here.
from .models import * #importa nossos models

class FabricanteAdmin(admin.ModelAdmin):
    # Cria um filtro de hierarquia com datas
    date_hierarchy = 'criado_em'
    search_fields = ('fabricante',)

class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('categoria',)

class ProdutoAdmin(admin.ModelAdmin):
    date_hierarchy = 'criado_em'
    list_display = ('produto', 'destaque', 'promocao', 'msgPromocao', 'preco', 'categoria',)
    empty_value_display = 'Sem promoção'
    search_fields = ('produto',)
    fields = ('produto', 'destaque', 'promocao', 'msgPromocao', 'preco', 'categoria', 'fabricante', 'image')

admin.site.register(Fabricante, FabricanteAdmin) #adiciona a interface do adm
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Usuario)