#! python3


def choice(*bitsin, choicebit: str="1"):
    """
    Inputs e, f, g should be entered as g, f, e so that 'e'
    is the choice bit, e=1 chooses f and e=0 chooses g
    :param bitsin:
    :param choicebit:
    :return:
    """

    return bitsin[int(choicebit)]
