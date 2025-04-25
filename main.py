# Importa a biblioteca Streamlit para a criação da interface web.
import streamlit as st  
# Importa o cliente para interagir com o Azure Blob Storage.
from azure.storage.blob import BlobServiceClient  
# Importa a biblioteca para manipulação de arquivos e variáveis de ambiente.
import os  
# Importa a biblioteca para interagir com o SQL Server.
import pymssql  
# Importa a biblioteca para gerar identificadores únicos.
import uuid 
# Importa a biblioteca para manipulação de JSON. 
import json  
# Importa a função para carregar variáveis de ambiente de um arquivo .env.
from dotenv import load_dotenv

# ...............................................................................................................................................
# ...............................................................................................................................................

# Carrega as variáveis de ambiente do arquivo .env.
load_dotenv()

# ...............................................................................................................................................
# ...............................................................................................................................................

# Carrega as variáveis de configuração do Azure e SQL Server a partir do arquivo .env.
blobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName    = os.getenv('BLOB_CONTAINER_NAME')
blobaccountName      = os.getenv('BLOB_ACCOUNT_NAME')

SQL_SERVER           = os.getenv('SQL_SERVER')
SQL_DATABASE         = os.getenv('SQL_DATABASE')
SQL_USER             = os.getenv('SQL_USER')
SQL_PASSWORD         = os.getenv('SQL_PASSWORD')

# ...............................................................................................................................................
# ...............................................................................................................................................

# Exibe o título da página no Streamlit.
st.title('Cadastro de Produtos') 
# Formulário de cadastro de produtos.
# Campo de entrada de texto para o nome do produto.
product_name         = st.text_input('Nome do Produto') 
# Campo de entrada para o preço do produto com formato de número.
product_price        = st.number_input('Preço do Produto', min_value=0.0, format='%.2f')  
# Campo de entrada de área de texto para a descrição do produto.
product_description  = st.text_area('Descrição do Produto')  
# Campo para upload de imagem do produto.
product_image        = st.file_uploader('Imagem do Produto', type=['jpg', 'png', 'jpeg'])  

# ...............................................................................................................................................
# ...............................................................................................................................................

# Função para fazer o upload de um arquivo para o Azure Blob Storage.
def upload_blob(file):
    # Cria um cliente para o Azure Blob Storage utilizando a string de conexão.
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    # Obtém o cliente do container onde os arquivos serão armazenados.
    container_client    = blob_service_client.get_container_client(blobContainerName)
    # Gera um nome único para o arquivo usando o uuid.
    blob_name           = str(uuid.uuid4()) + file.name
    # Cria o cliente do blob para o arquivo específico.
    blob_client         = container_client.get_blob_client(blob_name)
    # Realiza o upload do arquivo para o Azure Blob Storage, sobrescrevendo se já existir.
    blob_client.upload_blob(file.read(), overwrite=True)
    # Cria a URL de acesso ao blob armazenado no Azure.
    image_url           = f"https://{blobaccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    # Retorna a URL do arquivo armazenado no Blob Storage.
    return image_url

# ...............................................................................................................................................
# ...............................................................................................................................................

# Função para inserir as informações do produto no banco de dados SQL Server.
def insert_product(product_name, product_price, product_description, product_image):
  try:
    image_url = upload_blob(product_image)
    # Estabelece a conexão com o banco de dados SQL Server.
    conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
    # Cria um cursor para executar comandos SQL no banco de dados.
    cursor = conn.cursor()
    # Comando SQL para inserir um novo produto na tabela "Products".
    query = """
    INSERT INTO Produtos (nome, preco, descricao, imagem_url) 
    VALUES (%s, %s, %s, %s)
    """
    # Executa o comando SQL, passando os dados do produto como parâmetros para evitar SQL injection.
    cursor.execute(query, (product_name, product_price, product_description, image_url))
    # Confirma a transação no banco de dados.
    conn.commit()
    # Fecha a conexão com o banco de dados.
    conn.close()
    return True
  except Exception as e:
     st.error(f"Erro ao inserir produto: {e}")
     return False
  
# ...............................................................................................................................................
# ...............................................................................................................................................

def list_products():
  try:
    # Estabelece a conexão com o banco de dados SQL Server.
    conn = pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)
    # Cria um cursor para executar comandos SQL no banco de dados.
    cursor = conn.cursor()
    # Comando SQL para selecionar todos os produtos da tabela "Products".
    query = "SELECT * FROM Produtos"
    # Executa o comando SQL.
    cursor.execute(query)
    # Recupera todos os resultados da consulta.
    products = cursor.fetchall()
    # Fecha a conexão com o banco de dados.
    conn.close()
    return products
  except Exception as e:
    st.error(f"Erro ao listar produtos: {e}")
    return []

# ...............................................................................................................................................
# ...............................................................................................................................................

def list_products_screen():
   products = list_products()
   # Verifica se há produtos cadastrados.
   if products:
      # Define o número de cards por linha.
      cards_por_linha = 3
      # Cria colunas para os cards dos produtos.
      cols = st.columns(cards_por_linha)
      for i, product in enumerate(products):
          col = cols[i % cards_por_linha]
          # Exibe o nome do produto.
          with col:
             st.markdown(f"**Nome:** {product[1]}")
             # Exibe o preço do produto formatado como moeda.
             st.write(f"**Preço:** R$ {product[2]:.2f}")
             # Exibe a descrição do produto.    
             st.write(f"**Descrição:** {product[3]}")
             # Exibe a imagem do produto.
             if product[4]:
                html_img = f'<img src="{product[4]}" alt="Imagem do Produto" width="200" height="200">'
                st.markdown(html_img, unsafe_allow_html=True)
             st.markdown('---')
          # A cada linha cards_por_linha, cria uma nova coluna de cards.
          if (i + 1) % cards_por_linha == 0:
              cols = st.columns(cards_por_linha)
   else:
      # Se não houver produtos cadastrados, exibe uma mensagem informando.
      st.write("Nenhum produto cadastrado.")      

# ...............................................................................................................................................
# ...............................................................................................................................................

# Quando o botão "Salvar Produto" é pressionado, executa a lógica para salvar o produto no banco de dados.
if st.button('Salvar Produto'):
    # Verifica se todos os campos do formulário foram preenchidos.
    if product_name and product_price and product_description and product_image:
        # Realiza o upload da imagem para o Azure Blob Storage e obtém a URL da imagem.
        image_url = upload_blob(product_image)
        # Chama a função para inserir as informações do produto no banco de dados.
        insert_product(product_name, product_price, product_description, image_url)
        # Exibe uma mensagem de sucesso quando o produto for salvo corretamente.
        st.success('Produto salvo com sucesso!')
        list_products_screen()
    else:
        # Se algum campo não foi preenchido, exibe uma mensagem de erro.
        st.error('Preencha todos os campos para salvar o produto.')

# ...............................................................................................................................................
# ...............................................................................................................................................

# Exibe o título "Produtos Cadastrados".
st.header('Produtos Cadastrados')

# Quando o botão "Listar Produtos" é pressionado, exibe os produtos cadastrados (lógica de listagem pode ser implementada aqui).
if st.button('Listar Produtos'):
    # Chama a função para listar os produtos cadastrados.
    list_products_screen()
    # Aqui você pode implementar a lógica para listar os produtos do banco de dados.
    st.write('Produtos listados com sucesso.')