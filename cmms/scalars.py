from graphene.types import Scalar
from graphql.language import ast


class BigInt(Scalar):
    """
    We convert BigInt to String, cause Int or Float always caused rounding error.
    No thanks to JS/JSON.
    """

    @staticmethod
    def big_to_str(value):
        return str(value)
        """
        num = int(value)
        if num > MAX_INT or num < MIN_INT:
            return float(int(num))
        return num
        """

    serialize = big_to_str
    parse_value = big_to_str

    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.IntValueNode):
            return node.value
            """
            if num > MAX_INT or num < MIN_INT:
                return float(int(num))
            return num
            """
