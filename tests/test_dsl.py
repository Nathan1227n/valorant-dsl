import unittest

from parser import carregar_parser, analisar_codigo


class TestValorScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parser = carregar_parser()

    def test_estrategia_valida(self):
        codigo = """
        STRATEGY teste {
            ROUND 5
            MAP Ascent
            OBJECTIVE A

            TEAM ATTACK {
                PLAYERS {
                    PLAYER Nathan Jett
                }

                ACTIONS {
                    USE Jett Dash AT A_Main
                    POSITION A_Main
                    WAIT 5
                    PLANT A
                }
            }
        }
        """

        arvore = analisar_codigo(
            self.parser,
            codigo
        )

        self.assertIsNotNone(arvore)

    def test_wait_invalido(self):
        codigo = """
        STRATEGY teste {
            ROUND 5
            MAP Ascent
            OBJECTIVE A

            TEAM ATTACK {
                PLAYERS {
                    PLAYER Nathan Jett
                }

                ACTIONS {
                    WAIT cinco
                }
            }
        }
        """

        with self.assertRaises(Exception):
            analisar_codigo(
                self.parser,
                codigo
            )

    def test_team_obrigatorio(self):
        codigo = """
        STRATEGY teste {
            ROUND 5
            MAP Ascent
            OBJECTIVE A
        }
        """

        with self.assertRaises(Exception):
            analisar_codigo(
                self.parser,
                codigo
            )


if __name__ == "__main__":
    unittest.main()