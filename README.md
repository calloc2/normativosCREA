# Normativos CREA-TO

Sistema de consulta e gerenciamento de ementas e atos normativos do CREA-TO.

## Estrutura do Projeto

```
normativosCREA/
├── core/                   # Configurações principais do Django
├── ementas/               # Aplicação principal
├── media/                 # Arquivos de upload (PDFs, anexos)
│   └── ementas/
│       └── pdf/           # PDFs das ementas
├── static/                # Arquivos estáticos (CSS, JS, imagens)
│   └── images/            # Imagens (logo CREA-TO)
├── templates/             # Templates HTML
└── manage.py              # Script de gerenciamento Django
```

## Configuração de Arquivos

### Arquivos Estáticos (`static/`)
- **Logo e imagens**: `static/images/`
- **CSS e JavaScript**: `static/`
- **Configuração**: `STATIC_URL = 'static/'` e `STATICFILES_DIRS`

### Arquivos de Mídia (`media/`)
- **PDFs das ementas**: `media/ementas/pdf/`
- **Configuração**: `MEDIA_URL = '/media/'` e `MEDIA_ROOT`
- **Gitignore**: A pasta `media/` está no `.gitignore` para não versionar arquivos de upload

### Filtros Implementados
- **Busca por texto**: título, número, resumo, ementa
- **Tipo de ato normativo**: Portaria, Decisão Plenária, Ato Administrativo
- **Situação**: Em Vigor, Revogada, Cancelada
- **Período de data**: Data de início e fim para publicação
- **Paginação**: 10, 50 ou 100 itens por página

## Desenvolvimento

### Instalação
1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate` (Windows)
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure as variáveis de ambiente no arquivo `.env`
6. Execute as migrações: `python manage.py migrate`
7. Inicie o servidor: `python manage.py runserver`

### Estrutura de Upload
- Os PDFs são salvos automaticamente em `media/ementas/pdf/`
- O campo `arquivo` no modelo `Ementa` usa `upload_to="ementas/pdf/"`
- Em desenvolvimento, os arquivos são servidos via `MEDIA_URL`

## Tecnologias
- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5.3
- **Banco de Dados**: PostgreSQL
