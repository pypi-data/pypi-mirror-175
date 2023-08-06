from types import NoneType


class Node:
    def __init__(self, state_name, father, cost):
        self.state_name = state_name
        self.father = father
        self.cost = cost

    def __eq__(self, __obj: 'Node'):
        return self.state_name == __obj.state_name


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def path_print(path, total, search_method, print_path=False):

    print(f'{bcolors.WARNING + path[0] + bcolors.ENDC} to ' +
          f'{bcolors.OKGREEN + path[-1] + bcolors.ENDC}')
    print(f'Search method: {bcolors.BOLD + search_method + bcolors.ENDC}')
    if print_path:
        print()
        path_print_aux(path)
        print()
    print(f'Total distance: {bcolors.OKCYAN + str(total) + bcolors.ENDC}')


def path_print_aux(path):
    for ind, state in enumerate(path):
        if state == path[-2]:
            print(f'{state} --> ' + bcolors.OKGREEN +
                  f'{path[ind+1]}' + bcolors.ENDC)
            break
        elif state == path[0]:
            print(bcolors.WARNING + f'{state}' +
                  bcolors.ENDC + f' --> {path[1]}')
        else:
            print(f'{state} --> {path[ind+1]}')


def search(start, method, print_path=False):
    end = 'Bucharest'
    if method == 'bfs':
        method = 'Breadth-first search'
        resultado = length_search(map_dict, start, end)
    elif method == 'c_unif':
        method = 'Uniform-cost search'
        resultado = cost_search(map_dict, start, end)
    elif method == 'dfs':
        method = 'Depth-first search'
        resultado = deep_search(map_dict, start, end)
    elif method == 'greedy':
        method = 'Greedy search'
        resultado = greedy_search(map_dict, distance, start, end)
    elif method == 'star':
        method = 'A* search'
        resultado = star_search(map_dict, distance, start, end)
    return path_print(resultado[0], resultado[1], method, print_path)


def solution(node):
    path = []
    actual = node
    total = actual.cost
    while type(actual) is not NoneType:
        path.append(actual.state_name)
        actual = actual.father
    return path, total


# Dicionário contendo uma lista de tuplas de cada transição para cada cidade
#(destino, distância)
map_dict = {
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Zerind': [('Oradea', 71), ('Arad', 75)],
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Bucharest': [('Pitesti', 101), ('Fagaras', 211), ('Giurgiu', 90)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]}

# Distância em linha reta de cada cidade para Bucharest
distance = {'Arad': 366, 'Craiova': 160, 'Bucharest': 0, 'Drobeta': 242, 'Eforie': 161, 'Fagaras': 176,
            'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234, 'Oradea': 380,
            'Pitesti': 100, 'Rimnicu Vilcea': 193, 'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199,
            'Zerind': 374}

# Função do algoritmo de busca em largura


def length_search(map_dict, start, end):
    border = []
    used = []
    start_node = Node(start, None, 0)
    border.append(start_node)
    while True:
        # Caso de erro
        if len(border) == 0:
            print('error')
            return None
        # Verificando o primeiro elemento da borda, removendo da borda e inserindo em usados
        actual = border[0]
        border.pop(0)
        used.append(actual)
        # Verificando as transições do nó atual
        actual_transitions = map_dict.get(actual.state_name)
        for transition in actual_transitions:
            # Criando nó filho para cada transição
            child = Node(transition[0], actual, actual.cost + transition[1])
            if child not in used + border:
                # Se nó filho é destino final, retornar solução
                if child.state_name == end:
                    path_distance = solution(child)
                    path = list(reversed(path_distance[0]))
                    total = path_distance[1]
                    return path, total
                # Se nó filho não é destino final, inserir na borda
                border.append(child)

# Função do algoritmo de busca em profundidade


def deep_search(map_dict, start, end):
    used = []
    start_node = Node(start, None, 0)
    border = [start_node]
    while True:
        # Caso de erro
        if len(border) == 0:
            print('error')
            return 0
        # Verificando o último elemento da borda, removendo da borda e inserindo em usados
        actual = border[-1]
        border.pop()
        used.append(actual)
        # Verificando as transições do nó atual
        actual_transitions = map_dict.get(actual.state_name)
        for transition in actual_transitions:
            # Criando nó filho para cada transição
            child = Node(transition[0], actual, actual.cost + transition[1])
            if child not in used + border:
                # Se nó filho é destino final, retornar solução
                if child.state_name == end:
                    path_distance = solution(child)
                    path = list(reversed(path_distance[0]))
                    total = path_distance[1]
                    return path, total
                # Se nó filho não é destino final, inserir na borda
                border.append(child)


# Função do algoritmo de busca em custo uniforme
def cost_search(map_dict, start, end):
    border = []
    used = []
    start_node = Node(start, None, 0)
    border.append(start_node)
    while True:
        # Caso de erro
        if len(border) == 0:
            return 'error'
        # Verificando o primeiro elemento da borda, removendo da borda e inserindo em usados
        actual = border[0]
        border.pop(0)
        # Se nó atual é destino final, retornar solução
        if actual.state_name == end:
            solution_path = solution(actual)
            path = list(reversed(solution_path[0]))
            cost = solution_path[1]
            return path, cost
        # Se nó atual não é destino final, inserir em usados
        used.append(actual)
        # Verificando as transições do nó atual
        actual_transitions = map_dict.get(actual.state_name)
        for transition in actual_transitions:
            # Criando nó filho para cada transição
            child = Node(transition[0], actual, actual.cost + transition[1])
            if child not in used and child not in border:
                border.append(child)
            # Se filho está na borda
            elif child in border:
                for x in border:
                    # Se filho tem custo menor que o que está na borda, trocar pelo menor
                    if child.state_name == x.state_name:
                        if x.cost > child.cost:
                            x.cost = child.cost
                            x.father = child.father

# Função do algoritmo de busca gulosa


def greedy_search(map_dict, hv, start, end):
    start_node = Node(start, None, 0)
    border, used = [start_node], []
    while True:
        # Caso de erro
        if len(border) == 0:
            return 'error'
        # Ordenar borda pela função de ordenação gulosa
        border = greedy_order(border, hv)
        # Verificar primeiro elemento da borda, e remover
        actual = border[0]
        border.pop(0)
        # Se nó atual é destino final, retornar solução
        if actual.state_name == end:
            path_total = solution(actual)
            path = list(reversed(path_total[0]))
            total = path_total[1]
            return path, total
        # Se nó atual não é destino final, inserir em usados
        used.append(actual)
        # Verificar transições do nó atual
        actual_transitions = map_dict.get(actual.state_name)
        for transition in actual_transitions:
            # Criando nó filho para cada transição
            child = Node(transition[0], actual,
                         actual.cost + transition[1])
            # Se filho não está em borda nem usados, adicionar na borda
            if child not in border + used:
                border.append(child)
            # Se filho tem custo menor que o que está na borda, trocar pelo menor
            elif child in border:
                for x in border:
                    if x == child and x.cost > child.cost:
                        x.cost == child.cost
                        x.father == child.father

# Função de ordenção heurística gulosa para ordenar a borda
# baseado na menor distância em linha reta


def greedy_order(border, hv):
    # Transformando cada elemento da borda em uma tupla (cidade, distancia em linba reta)
    border = [(x, hv.get(x.state_name)) for x in border]
    # Ordenação em distância de menor para maior
    border.sort(key=lambda tup: tup[1])
    # Transformando itens da borda em apenas cidade
    border = [x[0] for x in border]
    return border

# ---- // BUSCA ESTRELA // ----

# Função do algoritmo de busca estrela


def star_search(map_dict, hv, start, end):
    start_node = Node(start, None, 0)
    border, used = [start_node], []
    while True:
        # Caso de erro
        if len(border) == 0:
            return 'error'
        # Ordenar borda pela função de ordenação estrela
        border = star_order(border, hv)
        # Verificar primeiro elemento da borda, e remover
        actual = border[0]
        border.pop(0)
        # Se nó atual é destino final, retornar solução
        if actual.state_name == end:
            path_total = solution(actual)
            path = list(reversed(path_total[0]))
            total = path_total[1]
            return path, total
        # Se nó atual não é destino final, inserir em usados
        used.append(actual)
        # Verificar transições do nó atual
        actual_transitions = map_dict.get(actual.state_name)
        for transition in actual_transitions:
            # Criando nó filho para cada transição
            child = Node(transition[0], actual,
                         actual.cost + transition[1])
            # Se filho não está em borda nem usados, adicionar na borda
            if child not in border + used:
                border.append(child)
            # Se filho tem custo menor que o que está na borda, trocar pelo menor
            elif child in border:
                for x in border:
                    if x == child and x.cost > child.cost:
                        x.cost = child.cost
                        x.father = child.father

# Função de ordenção heurística estrela para ordenar a borda
# baseado na menor distância em linha reta adicionado com a distância.


def star_order(border, hv):
    # Transformando cada elemento da borda em uma tupla (cidade, distancia em linba reta)
    border = [(x, hv.get(x.state_name) + x.cost) for x in border]
    # Ordenação em menor para maior
    border.sort(key=lambda tup: tup[1])
    # Transformando itens da borda em apenas cidade
    border = [x[0] for x in border]
    return border
