# controle-de-despesas

Controle de Despesas feito com [Django Ninja](https://django-ninja.rest-framework.com/).

## Este projeto foi feito com:

* [Python 3.10.2](https://www.python.org/)
* [Django 4.0.4](https://www.djangoproject.com/)
* [Django Ninja 0.17.0](https://django-ninja.rest-framework.com/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/controle-de-despesas.git
cd controle-de-despesas
python -m venv .venv

.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux

pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
```

## Passo a passo

Leia o [passo-a-passo.md](passo-a-passo.md)

