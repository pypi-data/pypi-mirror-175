# Projeto: Pacote de Processamento de Imagens

<br />
<br />

Esse projeto é parte integrante de:
- **[Bootcamp Geração Tech Unimed-BH - Ciência de Dados]

<br />
<br />

## Instutor(a):

<br />
<br />

**Autor(a) do Projeto / Instrutor(a):** [Karina Kato](https://www.linkedin.com/in/karina-kato-4b2a56182/) - [Digital Innovation One](https://dio.me/sign-up?ref=M87RWQPGJO).

<br />

**Aula:** Descomplicando a criação de pacotes de processamento de imagens em Python

<br />

**Tecnologia(s):** Python

<br />

---

<br />

## Descrição:

<br />
<br />

O pacote "image_processing" é usado para:

- Módulo "processing":
  - Correspondência de histograma;
  - Redimensionar imagem;
  - Similaridade estrutural;

- Módulo "utils":
  - Ler imagem;
  - Plotar histograma;
  - Plotar imagem;
  - Resultado do gráfico;
  - Salvar imagem;

<br />

---

<br />

## Preparando o pacote para o deploy

<br />
<br />

- [x] Preparando o ambiente:

<br />

```
py -m pip install --upgrade pip
py -m pip install --user twine
py -m pip install --user setuptools
py -m pip install --user wheel
```

<br />

- [x] Certifique-se de estar no mesmo diretório do arquivo **"setup.py"** e então execute:

<br />

```
C:\Projetos\Python\Development\Packages\image-processing-package> py setup.py sdist bdist_wheel
```

<br />

- [x] Após executar o comando a priori, verifique se as pastas abaixo foram devidamente criadas:
  - [x] build;
  - [x] dist;
  - [x] image_processing.egg-info

<br />
<br />

## Passo a passo para hospedar um pacote em Python no ambiente Test Pypi

<br />
<br />

- [x] Suba os arquivos usando o Twine para o Test Pypi:

<br />

```
py -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

<br />

Informe seu usuário e senha. Feito isso, o projeto estará hospedado no Test Pypi.

<br />
<br />

## Passo a passo para hospedar um pacote em Python no ambiente Pypi

<br />
<br />

- [x] Suba os arquivos usando o Twine para o Pypi:

<br />

```
py -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

<br />

Informe seu usuário e senha. Feito isso, o projeto estará hospedado no Pypi.

<br />

---

<br />

## Instalação local utilizando o ambiente de teste do Pypi

<br />
<br />

- [x] Instalção das dependências:

<br />

```bash
pip install -r requeriments.txt
```

<br />

- [x] Instalação do pacote

```bash
pip install -i https://test.pypi.org/simple/ image-processing-bymacrosann
```

<br />
<br />

## Instalação local utilizando o ambiente de produção do Pypi

<br />
<br />

- [x] Instalação do pacote

```bash
pip install image-processing-bymacrosann
```

<br />

**Nota:** Não efetuei o deploy em produção para evitar repetição de n pacotes duplicados com mesma finalidade.

<br />

---

<br />

## Utilizando o pacote

<br />
<br />

- [x] Carregue os submódulos:


```python
from image-processing-bymacrosann.utils import io, plot
from image-processing-bymacrosann.processing import combination, tranformation
combination.find_difference(image1, image2)
```

<br />

---

<br />


Observação: leia as [notas](#notas) a seguir, no caso essa parte refere-se a quem realizou o deploy no [ambiente Test Pypi](#user-content-instalação-local-utilizando-o-ambiente-de-teste-do-pypi).

<br />
<br />

## Notas:

<br />
<br />

O pacote foi criado pela [Karina Kato](https://www.linkedin.com/in/karina-kato-4b2a56182/)

<br />
<br />

## License

<br />
<br />

[MIT](https://choosealicense.com/licenses/mit/)

<br />

---

<br />

## Links Úteis

<br />
<br />

[Inscreva-se na Dio](https://dio.me/sign-up?ref=M87RWQPGJO)
<br />
[Dealing with dependency conflicts](https://pip.pypa.io/en/latest/topics/dependency-resolution/#dealing-with-dependency-conflicts)
<br />
[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
<br />
[Why am I getting a "Invalid or non-existent authentication information." error when uploading files?](https://test.pypi.org/help/#file-name-reuse)
<br />
[Why isn't my desired project name available?](https://test.pypi.org/help/#project-name)
