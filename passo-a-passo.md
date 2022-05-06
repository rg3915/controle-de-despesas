# Passo a passo

* Crie a virtualenv

```
python -m venv .venv
```


* Ative a virtualenv

```
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux
```

* Instale as bibliotecas

```
pip install django-ninja dr_scaffold djangorestframework django-extensions python-decouple
```

* Crie `requirements.txt`

```
Django==4.0.4
django-extensions==3.1.5
django-ninja==0.17.0
djangorestframework==3.13.1
dr-scaffold==2.1.2
python-decouple==3.6
```

* Gere o `.env`

```
python contrib/env_gen.py

cat .env
```

* Crie o projeto

```
django-admin startproject backend .
```

* Crie duas apps

```
cd backend
python ../manage.py startapp core
python ../manage.py startapp expense
```