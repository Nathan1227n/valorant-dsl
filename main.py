from pathlib import Path

from rich.console import Console
from rich.tree import Tree as RichTree

from parser import (
    carregar_parser,
    analisar_codigo,
    obter_tokens
)

from checker import verificar_semantica


console = Console()


# ============================================================
# FUNÇÃO AUXILIAR
# ============================================================

def obter_valor(no):
    """
    Extrai o valor real de um nó da árvore sintática.

    Exemplo:

    Tree('agente', [Token('ID', 'Jett')])

    retorna:

    Jett
    """

    if hasattr(no, "children") and no.children:
        return str(no.children[0])

    return str(no)


# ============================================================
# ÁRVORE VISUAL
# ============================================================

def criar_arvore_visual(arvore):
    """
    Cria uma representação visual da árvore sintática.
    """

    raiz = RichTree("[bold cyan]VALORSCRIPT[/bold cyan]")

    # --------------------------------------------------------
    # STRATEGY
    # --------------------------------------------------------

    strategy = arvore.children[0]

    nome_strategy = str(strategy.children[0])

    no_strategy = raiz.add(
        f"[bold magenta]STRATEGY:[/bold magenta] {nome_strategy}"
    )

    # --------------------------------------------------------
    # ROUND
    # --------------------------------------------------------

    round_node = strategy.children[1]
    numero_round = obter_valor(round_node.children[0])

    no_strategy.add(
        f"[bold yellow]ROUND:[/bold yellow] {numero_round}"
    )

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    map_node = strategy.children[2]
    nome_map = obter_valor(map_node.children[0])

    no_strategy.add(
        f"[bold yellow]MAP:[/bold yellow] {nome_map}"
    )

    # --------------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------------

    objective_node = strategy.children[3]
    objetivo = obter_valor(objective_node.children[0])

    no_strategy.add(
        f"[bold yellow]OBJECTIVE:[/bold yellow] {objetivo}"
    )

    # --------------------------------------------------------
    # TEAM
    # --------------------------------------------------------

    team_node = strategy.children[4]

    team_type_node = team_node.children[0]
    tipo_team = str(team_type_node.data).upper()

    no_team = no_strategy.add(
        f"[bold green]TEAM:[/bold green] {tipo_team}"
    )

    # --------------------------------------------------------
    # PLAYERS
    # --------------------------------------------------------

    players_node = team_node.children[1]

    no_players = no_team.add(
        "[bold cyan]PLAYERS[/bold cyan]"
    )

    for player_node in players_node.children:

        jogador = obter_valor(player_node.children[0])
        agente = obter_valor(player_node.children[1])

        no_players.add(
            f"[blue]PLAYER:[/blue] {jogador} → {agente}"
        )

    # --------------------------------------------------------
    # ACTIONS
    # --------------------------------------------------------

    actions_node = team_node.children[2]

    no_actions = no_team.add(
        "[bold cyan]ACTIONS[/bold cyan]"
    )

    for action_wrapper in actions_node.children:

        action = action_wrapper.children[0]
        tipo_acao = action.data

        # ----------------------------------------------------
        # USE
        # ----------------------------------------------------

        if tipo_acao == "ability":

            agente = obter_valor(action.children[0])
            habilidade = obter_valor(action.children[1])
            local = obter_valor(action.children[2])

            no_actions.add(
                f"[blue]USE:[/blue] "
                f"{agente} → {habilidade} @ {local}"
            )

        # ----------------------------------------------------
        # POSITION
        # ----------------------------------------------------

        elif tipo_acao == "position":

            posicao = obter_valor(action.children[0])

            no_actions.add(
                f"[blue]POSITION:[/blue] {posicao}"
            )

        # ----------------------------------------------------
        # WAIT
        # ----------------------------------------------------

        elif tipo_acao == "wait":

            tempo = obter_valor(action.children[0])

            no_actions.add(
                f"[blue]WAIT:[/blue] {tempo}"
            )

        # ----------------------------------------------------
        # PLANT
        # ----------------------------------------------------

        elif tipo_acao == "plant":

            local = obter_valor(action.children[0])

            no_actions.add(
                f"[blue]PLANT:[/blue] {local}"
            )

    return raiz


# ============================================================
# TESTE DE UM ARQUIVO
# ============================================================

def testar_arquivo(parser, caminho):

    print("=" * 60)
    print(f"Arquivo: {caminho}")
    print("=" * 60)

    with open(caminho, "r", encoding="utf-8") as arquivo:
        codigo = arquivo.read()

    # --------------------------------------------------------
    # ANÁLISE SINTÁTICA
    # --------------------------------------------------------

    try:

        arvore = analisar_codigo(parser, codigo)

    except Exception as erro:

        print("Sintaxe: INVÁLIDA")
        print()
        print("Erro de sintaxe:")
        print(erro)
        print()

        return

    print("Sintaxe: VÁLIDA")
    print()

    # --------------------------------------------------------
    # TOKENS
    # --------------------------------------------------------

    print("Tokens reconhecidos:")

    for token in obter_tokens(parser, codigo):

        tipo = token.type.lstrip("_")

        print(
            f"{tipo:<12} -> {token.value}"
        )

    # --------------------------------------------------------
    # PRETTY()
    # --------------------------------------------------------

    print()
    print("Árvore sintática - pretty():")

    print(arvore.pretty())

    # --------------------------------------------------------
    # ÁRVORE VISUAL
    # --------------------------------------------------------

    print()
    print("Árvore visual:")

    arvore_visual = criar_arvore_visual(arvore)

    console.print(arvore_visual)

    # --------------------------------------------------------
    # ANÁLISE SEMÂNTICA
    # --------------------------------------------------------

    erros = verificar_semantica(arvore)

    print()

    if erros:

        print("Semântica: INVÁLIDA")
        print()
        print("Erros encontrados:")

        for erro in erros:
            print(f"  - {erro}")

    else:

        print("Semântica: VÁLIDA")
        print()
        print("Programa válido!")

    print()


# ============================================================
# MAIN
# ============================================================

def main():

    parser = carregar_parser()

    pasta = Path("examples")

    arquivos = sorted(
        pasta.glob("*.vsl")
    )

    if not arquivos:

        print(
            "Nenhum arquivo .vsl encontrado "
            "em examples/"
        )

        return

    for arquivo in arquivos:

        testar_arquivo(
            parser,
            arquivo
        )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()