from lark import Tree

AGENT_ABILITIES = {
    "Jett": {"Dash"},
    "Sova": {"Reveal"},
    "Killjoy": {"Turret"},
    "Omen": {"Smoke"},
    "Raze": {"Satchel"},
    "Brimstone": {"Smoke"},
    "Sage": {"Wall"},
    "Phoenix": {"Flash"},
    "Breach": {"Flash"},
    "Cypher": {"Trap"},
    "Omen": {"Ultimate"},
}

LOCATIONS = {
    "A",
    "B",
    "A_Main",
    "B_Main",
    "BSite",
    "Mid",
}


def verificar_semantica(arvore):
    """
    Verifica algumas regras semânticas da ValorScript.

    Retorna uma lista contendo os erros encontrados.
    """

    erros = []

    strategy = arvore.children[0]

    team_node = strategy.children[4]

    actions_node = team_node.children[2]

    for action_wrapper in actions_node.children:

        action = action_wrapper.children[0]

        if action.data == "ability":

            agente = str(action.children[0])
            habilidade = str(action.children[1])
            local = str(action.children[2])

            if agente not in AGENT_ABILITIES:

                erros.append(
                    f"'{agente}' não é um agente válido."
                )

                continue

            if habilidade not in AGENT_ABILITIES[agente]:

                erros.append(
                    f"O agente '{agente}' não possui "
                    f"a habilidade '{habilidade}'."
                )

            if local not in LOCATIONS:

                erros.append(
                    f"'{local}' não é uma localização válida."
                )

        elif action.data == "position":

            local = str(action.children[0])

            if local not in LOCATIONS:

                erros.append(
                    f"POSITION espera uma localização, "
                    f"mas recebeu '{local}'."
                )

        elif action.data == "plant":

            local = str(action.children[0])

            if local not in LOCATIONS:

                erros.append(
                    f"PLANT espera uma localização, "
                    f"mas recebeu '{local}'."
                )

    return erros