import json

# Nome do arquivo onde os dados serão salvos
ARQUIVO_DADOS = "produtos.json"

class Produto:
    """Representa um produto com nome, preço e quantidade."""
    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def __str__(self):
        """Retorna uma representação em string do produto para exibição na Listbox."""
        return f"Nome: {self.nome} | Preço: R${self.preco:.2f} | Qtd: {self.quantidade}"

    def to_dict(self):
        """Converte o objeto Produto em um dicionário para serialização JSON."""
        return {
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade
        }

    @classmethod
    def from_dict(cls, data_dict):
        """Cria um objeto Produto a partir de um dicionário (ao carregar do JSON)."""
        return cls(data_dict["nome"], data_dict["preco"], data_dict["quantidade"])

def carregar_produtos():
    """Carrega a lista de produtos de um arquivo JSON.
    Retorna uma lista de objetos Produto.
    """
    produtos = []
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            for item in dados:
                produtos.append(Produto.from_dict(item))
    except FileNotFoundError:
        # Se o arquivo não existe, retorna uma lista vazia (primeira execução)
        pass
    except json.JSONDecodeError:
        # Lida com erros de decodificação JSON (arquivo corrompido)
        print(f"Aviso: Erro ao decodificar '{ARQUIVO_DADOS}'. Criando uma nova lista de produtos ou usando dados parciais.")
        # Você pode optar por retornar uma lista vazia ou os produtos lidos até o erro.
        # Por simplicidade, vamos retornar uma lista vazia aqui em caso de erro fatal.
        pass
    return produtos

def salvar_produtos(produtos):
    """Salva a lista de objetos Produto em um arquivo JSON."""
    # Converte a lista de objetos Produto em uma lista de dicionários
    dados_para_salvar = [p.to_dict() for p in produtos]
    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar dados no arquivo {ARQUIVO_DADOS}: {e}")

# --- NOVAS FUNÇÕES DE SERVIÇO PARA MANIPULAÇÃO DE DADOS ---

def adicionar_novo_produto(produtos_lista, nome, preco, quantidade):
    """Cria um novo produto e o adiciona à lista. Salva no arquivo."""
    novo_produto = Produto(nome, preco, quantidade)
    produtos_lista.append(novo_produto)
    salvar_produtos(produtos_lista)

def atualizar_produto_existente(produtos_lista, index, nome, preco, quantidade):
    """Atualiza um produto existente na lista pelo índice. Salva no arquivo."""
    if 0 <= index < len(produtos_lista):
        produtos_lista[index].nome = nome
        produtos_lista[index].preco = preco
        produtos_lista[index].quantidade = quantidade
        salvar_produtos(produtos_lista)
    else:
        print(f"Erro: Índice {index} fora dos limites para atualização.")

def excluir_produto_por_indice(produtos_lista, index):
    """Exclui um produto da lista pelo índice. Salva no arquivo."""
    if 0 <= index < len(produtos_lista):
        del produtos_lista[index]
        salvar_produtos(produtos_lista)
    else:
        print(f"Erro: Índice {index} fora dos limites para exclusão.")