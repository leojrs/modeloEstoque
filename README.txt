Como inicializar
Instalando as tecnologias necessárias
Instale python 3.5.2 ou superior

É possível que a máquina já possua o virtualev, se não, execute o comando para instalá-lo:

$ sudo pip install virtualenv

Depois de instalar o virtualenv,  criar um novo ambiente de desenvolvimento isolado, tal como:

$ virtualenv flaskapp

Entrar no novo ambiente de desenvolvimento e ativá-lo, para que comece a trabalhar com ele.

$ cd flaskapp
$ . bin/activate

Agora, execute o comando para instalar o Flask de forma segura:

$ pip install Flask
$ pip install Flask-SQLAlchemy

python3 app.py runserver

Em seguida basta navegar para http://localhost:5000/index