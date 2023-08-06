

## GITHUB ACTIONS
https://github.com/cds-astro/mocpy/blob/master/.github/workflows/deploy.yml


## GITHUB TAGGING - RELEASE
```
git tag -a v0.0.1 -m "Releasing v0.0.1"
```


# CREATING A RUST PYTHON PACKAGE 

Create & Activate Virtual Environment
```
python3 -m venv .venv 
source .env/bin/activate
```

Install & Init Maturin (Py03)
```
pip install maturin
maturin init
```

Build Development Package
```
maturin develop
```

Test Package
```
$ python
>>> import oxidizer
>>> oxidizer.sum_as_string(5, 20)
```



