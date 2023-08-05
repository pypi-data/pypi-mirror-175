from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing-ghf-package",
    version="0.0.1",
    author="Geraldo Henrique Fonseca",
    author_email="ghenfon@gmail.com",
    description="Test version - Image processing. Projeto criado pela Karina Kato para o bootcamp de ciência de dados da Unimed-BH.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GeraldoHenriqueFonseca/Processador_de_imagens_Dio_Unimed_BH",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)