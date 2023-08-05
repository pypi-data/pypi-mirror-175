# Desafio Unimed BH: Pacote de Processamento de Imagens

## Descrição
- Esse projeto consiste na criação de um pacote para python, com base no curso ministrado por Karina Kato no bootcamp de ciência de dados da Unimed-BH.
- Pacote de exemplo, baseado no [scikit-image](https://scikit-image.org)
---

## Passos para a hospedagem no Pypi
- Primeiro se realiza uma instalação ou upgrade do `pip`, `twine`, `setuptools` e `wheel`

python -m pip install --upgrade pip
python -m pip install --user twine
python -m pip install --user setuptools
python -m pip install --user wheel

- Cria-se as distribuições

python setup.py sdist bdist_wheel

- Serão criadas 3 pastas no projeto: 
  - build
  - dist
  - image_processing_package.egg-info

- O próximo passo é o upload no Test Pypi.

python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

- O comando para upload no Pypi é:

python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

## Instalação
- Para a instalação local, é necessário instalar os requerimentos primeiro.

pip install -r requirements.txt


Para a instalação do pacote, basta usar o [pip](https://pip.pypa.io/en/stable/) direcionando para o image-processing-ghf-package

```bash
pip install image-processing-ghf-package==0.0.1
```
---
## Uso
- Basta importar os módulos de acordo com o que deseja

```python
from image-processing-ghf-package.processing import transformation
transformation.resize_image(image_test, 0.5)
```
---
## Autor
Geraldo Henrique Fonseca

## Licença
[MIT](https://choosealicense.com/licenses/mit/)


