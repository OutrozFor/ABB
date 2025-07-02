import pickle

class Registro:
    def __init__(self, cpf: str, nome: str, data_nascimento: str):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.deletado = False  # Flag para marcação de registro deletado
    
    def __lt__(self, outro) -> bool:
        # Define a comparação baseada no CPF (chave de ordenação padrão)
        return self.cpf < outro.cpf
    
    def __str__(self) -> str:
        return f"CPF: {self.cpf}, Nome: {self.nome}, Nascimento: {self.data_nascimento}"

class NoABB:
    def __init__(self, chave: str, indice: int):
        self.chave = chave      # CPF do registro
        self.indice = indice    # Índice na Estrutura de Dados Linear (EDL)
        self.esquerda = None    # Filho esquerdo
        self.direita = None     # Filho direito

class ABB:
    def __init__(self, registros: list = None):
        self.raiz = None
        if registros is not None:
            for idx, registro in enumerate(registros):
                self.inserir(registro.cpf, idx)
    
    def inserir(self, chave: str, indice: int):
        """Insere um novo nó na árvore usando chave e índice"""
        self.raiz = self._inserir(self.raiz, chave, indice)
    
    def _inserir(self, no: NoABB, chave: str, indice: int) -> NoABB:
        if no is None:
            return NoABB(chave, indice)
        if chave < no.chave:
            no.esquerda = self._inserir(no.esquerda, chave, indice)
        elif chave > no.chave:
            no.direita = self._inserir(no.direita, chave, indice)
        else:  # Chave duplicada (atualiza o índice)
            no.indice = indice
        return no
    
    def remover(self, chave: str):
        """Remove um nó da árvore pela chave"""
        self.raiz = self._remover(self.raiz, chave)
    
    def _remover(self, no: NoABB, chave: str) -> NoABB:
        if no is None:
            return None
        if chave < no.chave:
            no.esquerda = self._remover(no.esquerda, chave)
        elif chave > no.chave:
            no.direita = self._remover(no.direita, chave)
        else:
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            else:  # Nó com dois filhos
                temp = self._min_no(no.direita)
                no.chave, no.indice = temp.chave, temp.indice
                no.direita = self._remover(no.direita, temp.chave)
        return no
    
    def _min_no(self, no: NoABB) -> NoABB:
        """Retorna o nó com a menor chave da subárvore"""
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
    
    def buscar(self, chave: str) -> int:
        """Busca um nó na árvore e retorna o índice associado"""
        return self._buscar(self.raiz, chave)
    
    def _buscar(self, no: NoABB, chave: str) -> int:
        if no is None:
            return -1
        if chave == no.chave:
            return no.indice
        elif chave < no.chave:
            return self._buscar(no.esquerda, chave)
        else:
            return self._buscar(no.direita, chave)
    
    def em_ordem(self) -> list:
        """Retorna lista de índices em ordem crescente de chave"""
        return self._em_ordem(self.raiz, [])
    
    def _em_ordem(self, no: NoABB, lista: list) -> list:
        if no is not None:
            self._em_ordem(no.esquerda, lista)
            lista.append(no.indice)
            self._em_ordem(no.direita, lista)
        return lista
    
    def pre_ordem(self) -> list:
        """Retorna lista de índices em pré-ordem"""
        return self._pre_ordem(self.raiz, [])
    
    def _pre_ordem(self, no: NoABB, lista: list) -> list:
        if no is not None:
            lista.append(no.indice)
            self._pre_ordem(no.esquerda, lista)
            self._pre_ordem(no.direita, lista)
        return lista
    
    def pos_ordem(self) -> list:
        """Retorna lista de índices em pós-ordem"""
        return self._pos_ordem(self.raiz, [])
    
    def _pos_ordem(self, no: NoABB, lista: list) -> list:
        if no is not None:
            self._pos_ordem(no.esquerda, lista)
            self._pos_ordem(no.direita, lista)
            lista.append(no.indice)
        return lista
    
    def em_largura(self) -> list:
        """Retorna lista de índices em nível (largura)"""
        if self.raiz is None:
            return []
        fila = [self.raiz]
        resultado = []
        while fila:
            no = fila.pop(0)
            resultado.append(no.indice)
            if no.esquerda:
                fila.append(no.esquerda)
            if no.direita:
                fila.append(no.direita)
        return resultado

class SGBD:
    def __init__(self):
        self.edl = []           # Estrutura de Dados Linear para registros
        self.indice_cpf = ABB() # Árvore de índice para CPF
    
    def inserir_registro(self, registro: Registro) -> int:
        """Insere registro na EDL e atualiza índice"""
        indice = len(self.edl)
        self.edl.append(registro)
        self.indice_cpf.inserir(registro.cpf, indice)
        return indice
    
    def remover_registro(self, cpf: str):
        """Marca registro como deletado e remove do índice"""
        indice = self.indice_cpf.buscar(cpf)
        if indice != -1:
            self.edl[indice].deletado = True
            self.indice_cpf.remover(cpf)
    
    def buscar_por_cpf(self, cpf: str) -> Registro:
        """Busca registro usando índice de CPF"""
        indice = self.indice_cpf.buscar(cpf)
        if indice == -1 or self.edl[indice].deletado:
            return None
        return self.edl[indice]
    
    def gerar_edl_ordenada(self) -> list:
        """Gera nova EDL ordenada usando percurso em ordem"""
        indices_ordenados = self.indice_cpf.em_ordem()
        return [self.edl[i] for i in indices_ordenados if not self.edl[i].deletado]

    def salvar (self, arquivo="dados_abb.pkl"):
        with open(arquivo, "wb") as f
            pickle.dump(self.edl, f)

    def carregar(self, arquivo="dados_abb.pkl"):
        try:
            with open(arquivo, "rb") as f:
                self.edl = pickle.load(f)
            # Reconstrói o índice a partir da EDL carregada
            self.indice_cpf = ABB(self.edl)
        except FileNotFoundError:
            self.edl = []
            self.indice_cpf = ABB()

# Exemplo de uso
if __name__ == "__main__":
    # Criar instância do SGBD
    sgbd = SGBD()
    
    # Inserir registros
    sgbd.inserir_registro(Registro("11111111111", "João Silva", "1990-01-01"))
    sgbd.inserir_registro(Registro("33333333333", "Maria Souza", "1985-05-15"))
    sgbd.inserir_registro(Registro("22222222222", "Carlos Oliveira", "2000-11-30"))
    sgbd.inserir_registro(Registro("88888888888", "Ana Terra", "1999-04-03"))
    sgbd.inserir_registro(Registro("55555555555", "Vitoria Araujo", "2005-08-12"))
    sgbd.inserir_registro(Registro("7777777777", "Julia Castelo" , "2008-05-25"))

    # Buscar registro
    print("\nBusca por CPF:")
    print(sgbd.buscar_por_cpf("22222222222") or "Registro não encontrado")
    print(sgbd.buscar_por_cpf("44444444444") or "Registro não encontrado")
    print(sgbd.buscar_por_cpf("88888888888") or "Registro não encontrado")
    print(sgbd.buscar_por_cpf("55555555555") or "Registro não encontrado")
    print(sgbd.buscar_por_cpf("77777777777") or "Registro não encontrado")   
    
    # Remover registro
    sgbd.remover_registro("33333333333")
    sgbd.remover_registro("11111111111")
    
    # Gerar EDL ordenada por CPF
    print("\nEDL Ordenada por CPF:")
    for registro in sgbd.gerar_edl_ordenada():
        print(registro)
    
    # Percursos na árvore de índice
    print("\nPercursos na árvore de índice:")
    print("Em Ordem:", sgbd.indice_cpf.em_ordem())
    print("Pré-Ordem:", sgbd.indice_cpf.pre_ordem())
    print("Pós-Ordem:", sgbd.indice_cpf.pos_ordem())
    print("Em Largura:", sgbd.indice_cpf.em_largura()) 
