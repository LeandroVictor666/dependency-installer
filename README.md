# Depedency Installer
This tool was developed for the Ubuntu operating system, I will soon be adding other distributions.
I haven't done any testing so far, if you get any errors with the tool, please share them with me!

#### [PT-BR]
Essa ferramenta foi desenvolvida no sistema operacional Ubuntu, em breve irei adicionar outras dist.
Eu não realizei nenhum tipo de teste, se você obter qualquer erro, por favor, sinta-se a vontade para compartilhar comigo!

---

#### Description
This tool was created for both up-and-coming beginner developers and even for the most experienced developer.
If you're a beginner, you won't need to break your head trying to install any technology, just have a brief knowledge of the Linux operating system to call upon such technologies.
If you're an experienced developer, you know that one of our greatest resources is our time, this py script will save you time
#### [PT-BR]
Essa ferramenta foi desenvolvida tanto para desenvolvedores iniciantes em ascenção, quanto para desenvolvedores mais experientes, se você é um iniciante, você não precisara quebrar sua cabeça tentando instalar nenhuma tecnologia, você só precisa ter um breve conhecimento no sistema operacional linux para chamar tais tecnologias.
Se você é um desenvolvedor experiente, sabe que um dos nossos maiores recursos é o nosso tempo, esse script py fara com que você economize seu tempo

---

#### Usage
- In the terminal, run the command: 'git clone https://github.com/LeandroVictor666/dependency-installer.git'
- Open the project folder, run the comand 'pip install -r requirements.txt', then, run the 'python3 dependency_installer.py' command, choose the technologies you want to install, and press 'Enter' to install them.
- Wait for the installation to finish
- [OPTIONAL] install nodejs via nvm, open a new terminal and run 'nvm install node' | It might seem a little pointless, to be honest, I was considering removing the automatic installation of nodejs and npm, and guiding the user to install nodejs via NVM, but perhaps some beginner developers will use this script, so I decided to leave it. More advanced developers will certainly know what to do.
- If you have installed rbenv, open terminal and run 'rbenv install -l' or 'rbenv install 3.1.2' to install ruby in your system.
- START CODDING

Note: The reason for these two final steps is that I WAS UNABLE to execute either the NVM command or the RBENV command via Python due to the terminal context, even after using the subprocess to execute in a new context, I continued to have errors.

### [PT-BR]
#### Como usar
- No terminal, execute o comando 'git clone https://github.com/LeandroVictor666/dependency-installer.git'.
- Abra a pasta do projeto e execute o comando 'pip install -r requirements.txt'. Em seguida, execute o comando 'python3 dependency_installer.py'. Escolha quais tecnologias você deseja instalar e aperte 'Enter' para instalar.
- Aguarde a instalação finalizar.
- [OPCIONAL] Instale o Node.js através do NVM. Abra um novo terminal e rode o comando 'nvm install node'. Isso pode parecer um pouco sem sentido; para ser honesto, eu estava considerando remover a instalação automática do Node.js e do npm e guiar o usuário a instalar o Node.js via NVM. Mas talvez alguns desenvolvedores iniciantes utilizem esse script, então decidi deixar como está. Desenvolvedores mais avançados certamente saberão o que fazer.]
- Se você instalou o Rbenv, abra um novo terminal e execute o comando 'rbenv install -l' ou 'rbenv install 3.1.2' para instalar o Ruby no seu sistema.
- COMEÇE A CODAR

Nota: A razão para essas duas etapas finais é que eu NÃO consegui executar nem o comando do NVM nem do RBENV através do Python, por conta do contexto do terminal (creio eu). Mesmo após utilizar o subprocess para executar os comandos em um novo contexto, continuei a ter erros.

#### Informations
##### Technologies included in the script: 
- NodeJs
- NPM
- NVM
- PHP
- PHP Extensions
- Composer
- Rbenv
- Docker
- Docker-Compose 
-> (I will soon include more, leave a suggestion!)

#### [PT-BR]
##### Tecnologias Incluidas No Script:
- Node.Js
- NPM
- NVM
- PHP
- PHP Extensions
- Composer
- RBenv
- Docker
- Docker-Compose
-> (Em breve adicionarei mais, deixe sugestões!)