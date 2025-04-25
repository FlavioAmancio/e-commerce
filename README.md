# Cadastro de Produtos com Streamlit, Azure Blob Storage e SQL Server

Este projeto utiliza **Streamlit**, **Azure Blob Storage** e **SQL Server** para permitir o cadastro e a exibição de produtos com nome, preço, descrição e imagem. A imagem dos produtos é armazenada no Azure Blob Storage, enquanto as informações do produto são salvas em um banco de dados SQL Server.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criação de interfaces web interativas.
- **Azure Storage Blob**: Serviço de armazenamento de arquivos na nuvem (Azure).
- **pymssql**: Conector Python para interagir com bancos de dados SQL Server.
- **dotenv**: Biblioteca para carregar variáveis de ambiente de um arquivo `.env`.

## Pré-requisitos

Antes de rodar o projeto, você precisa garantir que tenha as seguintes ferramentas instaladas:

- **Python 3.x** (recomendado: versão 3.7 ou superior)
- **Bibliotecas Python**: `streamlit`, `azure-storage-blob`, `pymssql`, `python-dotenv`

Você pode instalar as dependências utilizando o seguinte comando:

```bash
pip install streamlit azure-storage-blob pymssql python-dotenv

Além disso, você precisará de uma conta no Azure e um banco de dados SQL Server configurado. Crie um Container no Azure Blob Storage e configure as credenciais do banco de dados SQL Server.

Configuração
Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

BLOB_CONNECTION_STRING=your_blob_connection_string
BLOB_CONTAINER_NAME=your_blob_container_name
BLOB_ACCOUNT_NAME=your_blob_account_name

SQL_SERVER=your_sql_server_host
SQL_DATABASE=your_sql_database_name
SQL_USER=your_sql_user
SQL_PASSWORD=your_sql_password

Substitua os valores de acordo com as credenciais da sua conta do Azure e do SQL Server.

Como Usar
Inicie a aplicação Streamlit:

Execute o seguinte comando no terminal para rodar a aplicação:

bash
Copiar
Editar
streamlit run app.py

![image](https://github.com/user-attachments/assets/d070af1a-654d-4e80-842e-d51a8a0c225a)

Cadastro de Produto:

Na interface do Streamlit, você verá campos para preencher o nome, preço, descrição do produto e um botão para fazer o upload da imagem do produto.

![image](https://github.com/user-attachments/assets/61c0e756-0b83-4f28-86d4-a0945f566730)

Após preencher todos os campos, clique no botão "Salvar Produto" para cadastrar o produto. A imagem será carregada no Azure Blob Storage e os dados do produto serão salvos no banco de dados SQL Server.

![image](https://github.com/user-attachments/assets/8d31b807-624b-44a0-a9d3-24276cd3761e)

Exibição de Produtos Cadastrados:

![image](https://github.com/user-attachments/assets/d8446345-b630-401f-9a46-bbb09dd6079a)

Você também pode visualizar todos os produtos cadastrados clicando no botão "Listar Produtos". Os produtos serão exibidos com suas respectivas informações, incluindo a imagem armazenada no Azure Blob Storage.

Estrutura do Projeto
O projeto tem a seguinte estrutura de diretórios:

bash
Copiar
Editar
├── app.py            # Arquivo principal do Streamlit
├── .env              # Arquivo com variáveis de ambiente (não compartilhe este arquivo)
├── requirements.txt  # Lista de dependências Python
└── README.md         # Este arquivo
Como Funciona
Cadastro de Produtos:

Quando o usuário preenche o formulário e clica em "Salvar Produto", a imagem é enviada para o Azure Blob Storage utilizando o método upload_blob. A URL da imagem retornada é então inserida no banco de dados junto com o nome, preço e descrição do produto.

Exibição de Produtos:

Ao clicar em "Listar Produtos", a aplicação consulta o banco de dados SQL Server, recupera todos os produtos cadastrados e os exibe na tela, incluindo a imagem, preço e descrição.

Armazenamento de Dados:

As imagens dos produtos são armazenadas no Azure Blob Storage, e os dados do produto (nome, preço, descrição e URL da imagem) são persistidos em um banco de dados SQL Server.

Exemplo de Uso
Formulário de Cadastro de Produto
Ao abrir a aplicação, você verá um formulário com os seguintes campos:

Nome do Produto: Campo para digitar o nome do produto.

Preço do Produto: Campo para inserir o preço do produto.

Descrição do Produto: Campo para adicionar uma descrição do produto.

Imagem do Produto: Campo para enviar uma imagem do produto (somente arquivos .jpg, .png ou .jpeg).

Após preencher todos os campos, clique em "Salvar Produto" para cadastrar o produto. A imagem será carregada no Azure Blob Storage e a URL da imagem será armazenada junto com as outras informações no banco de dados.

Listagem de Produtos
Após cadastrar produtos, clique em "Listar Produtos" para ver os produtos que foram registrados. A aplicação exibirá uma lista de produtos com seu nome, preço, descrição e a imagem armazenada no Azure Blob Storage.

Considerações Finais
Este projeto demonstra como integrar uma aplicação web simples com o Azure Blob Storage para armazenamento de imagens e um banco de dados SQL Server para persistência de dados. O uso de Streamlit facilita a criação de interfaces web interativas, e a utilização de dotenv ajuda a manter as credenciais e configurações de forma segura.

Licença
Este projeto está licenciado sob a MIT License.

yaml
Copiar
Editar

---
