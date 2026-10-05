from lark import Tree


# ============================================================
# HABILIDADES DOS AGENTES
# ============================================================

AGENT_ABILITIES = {
    "Jett": {"Dash", "Updraft"},
    "Sova": {"Reveal"},
    "Killjoy": {"Turret"},
    "Omen": {"Smoke", "Ultimate"},
    "Raze": {"Satchel"},
    "Brimstone": {"Smoke"},
    "Sage": {"Wall"},
    "Phoenix": {"Flash"},
    "Breach": {"Flash"},
    "Cypher": {"Trap"},
}


# ============================================================
# LOCALIZAÇÕES VÁLIDAS
# ============================================================

LOCATIONS = {
    "A",
    "B",
    "C",
    "A_Main",
    "B_Main",
    "BSite",
    "A_Site",
    "C_Site",
    "Mid",
    "BoxMid"
}


# ============================================================
# FUNÇÃO AUXILIAR
# ============================================================

def obter_valor(no):
    """
    Extrai o valor real de um nó da árvore sintática.

    Exemplo:

    Tree(
        Token('RULE', 'agente'),
        [Token('ID', 'Jett')]
    )

    retorna:

    Jett
    """

    if isinstance(no, Tree):

        if no.children:

            return obter_valor(
                no.children[0]
            )

    return str(no)


# ============================================================
# VERIFICAÇÃO SEMÂNTICA
# ============================================================

def verificar_semantica(arvore):
    """
    Verifica algumas regras semânticas da ValorScript.

    Retorna uma lista contendo os erros encontrados.
    """

    erros = []

    # --------------------------------------------------------
    # ESTRUTURA PRINCIPAL
    # --------------------------------------------------------

    strategy = arvore.children[0]

    team_node = strategy.children[4]

    actions_node = team_node.children[2]

    # --------------------------------------------------------
    # VERIFICA AS AÇÕES
    # --------------------------------------------------------

    for action_wrapper in actions_node.children:

        action = action_wrapper.children[0]

        # ====================================================
        # USE
        # ====================================================

        if action.data == "ability":

            agente = obter_valor(
                action.children[0]
            )

            habilidade = obter_valor(
                action.children[1]
            )

            local = obter_valor(
                action.children[2]
            )

            # ------------------------------------------------
            # Verifica se o agente existe
            # ------------------------------------------------

            if agente not in AGENT_ABILITIES:

                erros.append(
                    f"'{agente}' não é um agente válido."
                )

                continue

            # ------------------------------------------------
            # Verifica se o agente possui a habilidade
            # ------------------------------------------------

            if habilidade not in AGENT_ABILITIES[agente]:

                erros.append(
                    f"O agente '{agente}' não possui "
                    f"a habilidade '{habilidade}'."
                )

            # ------------------------------------------------
            # Verifica se a localização existe
            # ------------------------------------------------

            if local not in LOCATIONS:

                erros.append(
                    f"'{local}' não é uma localização válida."
                )

        # ====================================================
        # POSITION
        # ====================================================

        elif action.data == "position":

            local = obter_valor(
                action.children[0]
            )

            if local not in LOCATIONS:

                erros.append(
                    f"POSITION espera uma localização, "
                    f"mas recebeu '{local}'."
                )

        # ====================================================
        # PLANT
        # ====================================================

        elif action.data == "plant":

            local = obter_valor(
                action.children[0]
            )

            if local not in LOCATIONS:

                erros.append(
                    f"PLANT espera uma localização, "
                    f"mas recebeu '{local}'."
                )

    return erros