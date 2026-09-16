from typing import TYPE_CHECKING, Callable, Mapping
import enum
from dataclasses import dataclass
from Options import OptionError

if TYPE_CHECKING:
    from .nodes import SC2MOGenLayout, SC2MOGenMission, MissionOrderNode


class TokenType(enum.Enum):
    NONE = enum.auto()
    OPEN_PAREN = enum.auto()
    CLOSE_PAREN = enum.auto()
    COMMA = enum.auto()
    NUMERIC = enum.auto()
    SYMBOL = enum.auto()
    OPERATOR = enum.auto()


@dataclass(slots=True)
class Token:
    offset: int
    content: str
    type: TokenType


def tokenize(term: str) -> list[Token]:
    if not term:
        return []
    result: list[Token] = []
    index = 0
    while index < len(term):
        char = term[index]
        if char == "(":
            result.append(Token(index, char, TokenType.OPEN_PAREN))
        elif char == ")":
            result.append(Token(index, char, TokenType.CLOSE_PAREN))
        elif char == ",":
            result.append(Token(index, char, TokenType.COMMA))
        elif char.isspace():
            pass
        elif char in "+-*/%":
            result.append(Token(index, char, TokenType.OPERATOR))
        elif char.isnumeric():
            start_index = index
            index += 1
            while index < len(term) and term[index].isnumeric():
                index += 1
            result.append(Token(start_index, term[start_index:index], TokenType.NUMERIC))
            continue
        elif char.isalpha() or char == "_":
            start_index = index
            index += 1
            while index < len(term) and (term[index].isalpha() or term[index] == "_"):
                index += 1
            result.append(Token(start_index, term[start_index:index], TokenType.SYMBOL))
            continue
        else:
            raise OptionError(f"Invalid character in layout search term \"{term}\" at offset {index}: {char}")
        index += 1
    return result


def resolve_operators(operands: list[int], operators: list[Token]) -> int:
    result = operands.pop(0)
    assert len(operands) == len(operators)
    for operand, operator in zip(operands, operators):
        if operator.content == "+":
            result = result + operand
        elif operator.content == "-":
            result = result - operand
        elif operator.content == "*":
            result = result * operand
        elif operator.content == "/":
            result = result // operand
        elif operator.content == "%":
            result = result % operand
        else:
            raise ValueError(f"Unknown operator '{operator.content}'")
    return result


def parse_index(
    term: str,
    index_functions: Mapping[str, tuple[Callable, int, bool]],
    search_info: tuple['SC2MOGenMission', 'SC2MOGenLayout'] | tuple[()],
    num_missions: int,
    context: str
) -> set[int]:
    tokens = tokenize(term)
    if not tokens:
        return set()
    if tokens[0].type == TokenType.SYMBOL and tokens[0].content.lower() in index_functions:
        func_info = index_functions[tokens[0].content.lower()]
        if func_info[1] == 0 and len(tokens) == 1:
            return func_info[0]()
        func, num_args, takes_strings = func_info
        if len(tokens) < 2 or tokens[1].type != TokenType.OPEN_PAREN:
            raise OptionError(f"Invalid layout search term \"{term}\": expected an opening parenthesis")
        if len(tokens) < 3 or tokens[-1].type != TokenType.CLOSE_PAREN:
            raise OptionError(f"Invalid layout search term \"{term}\": expected the expression to end with a closing parenthesis")
        content_tokens = tokens[2:-1]
        expression_scopes: list[list[Token]] = [[]]
        for token in content_tokens:
            if token.type == TokenType.COMMA:
                expression_scopes.append([])
            else:
                expression_scopes[-1].append(token)
        if not expression_scopes[-1]:
            expression_scopes.pop()
        if len(expression_scopes) != num_args:
            raise OptionError(
                f"Invalid layout search term \"{term}\": "
                f"function {tokens[0].content} takes {num_args} arguments, "
                f"but only {len(expression_scopes)} were provided"
            )
        arguments: list[str | int]
        if takes_strings:
            arguments = [''.join(element.content for element in scope) for scope in expression_scopes]
        else:
            arguments = [
                parse_int_expression(term, scope, index_functions, search_info, num_missions, context)
                for scope in expression_scopes
            ]
        return func(*arguments)
    return {parse_int_expression(term, tokens, index_functions, search_info, num_missions, context)}

def parse_int_expression(
    term: str,
    tokens: list[Token],
    index_functions: Mapping[str, tuple[Callable, int, bool]],
    search_info: tuple['SC2MOGenMission', 'SC2MOGenLayout'] | tuple[()],
    num_missions: int,
    context: str,
) -> int:
    stack: list[int] = []
    operator_stack: list[list[Token]] = []
    operator_precedence = {
        "+": 2,
        "-": 2,
        "*": 3,
        "/": 3,
        "%": 3,
        ",": 1,
        "(": 0,
        ")": 0,
    }
    index = 0
    previous_type = TokenType.NONE
    unary_multiplier = 1
    while index < len(tokens):
        token = tokens[index]
        if token.type == TokenType.NUMERIC:
            if previous_type in (TokenType.NUMERIC, TokenType.SYMBOL):
                raise OptionError(
                    f"Unknown formatting in layout search term \"{term}\": "
                    f"a number directly follows a number/symbol at offset {token.offset}"
                )
            stack.append(unary_multiplier * int(token.content))
        elif token.type == TokenType.SYMBOL:
            if token.content.lower() in index_functions:
                raise OptionError(
                    f"Invalid symbol in layout search term \"{term}\": "
                    f"index function {token.content.lower()} cannot be used within the scope of a larger expression"
                )
            if previous_type in (TokenType.NUMERIC, TokenType.SYMBOL):
                raise OptionError(
                    f"Unknown formatting in layout search term \"{term}\": "
                    f"a symbol directly follows a number/symbol at {token.offset}"
                )
            if not search_info:
                raise OptionError(
                    f"Invalid symbol in layout search term \"{term}\": "
                    f"cannot use variables while {context}"
                )
            start_mission, start_layout = search_info
            if token.content.lower() not in start_layout.layout_type.variables:
                raise OptionError(
                    f"Invalid symbol in layout search term \"{term}\": "
                    f"unknown symbol {token.content} "
                    f"for layout type '{start_layout.layout_type.NAME_IN_OPTIONS}'"
                )
            variable_func = start_layout.layout_type.variables[token.content.lower()]
            stack.append(unary_multiplier * variable_func(start_mission, start_layout))
        elif token.type == TokenType.OPERATOR:
            if previous_type in (TokenType.OPERATOR, TokenType.COMMA, TokenType.OPEN_PAREN, TokenType.NONE):
                if token.content in "-+":
                    index += 1
                    if index >= len(tokens):
                        raise OptionError(
                            f"Unknown formatting in layout search term \"{term}\": "
                            f"ending on a unary operator {token.content}"
                        )
                    if tokens[index].type not in (TokenType.SYMBOL, TokenType.NUMERIC):
                        raise OptionError(
                            f"Unknown formatting in layout search term \"{term}\": "
                            f"unary operator {token.content} does not precede a variable or number "
                            f"at offset {token.offset}"
                        )
                    if token.content == "-":
                        unary_multiplier = -1
                    continue
                else:
                    raise OptionError(
                        f"Unknown formatting in layout search term \"{term}\": "
                        f"two operators appear in a row at offset {token.offset}"
                    )
            precedence = operator_precedence[token.content]
            if not operator_stack or operator_precedence[operator_stack[-1][0].content] < precedence:
                operator_stack.append([])
            elif operator_precedence[operator_stack[-1][0].content] > precedence:
                while operator_stack and operator_precedence[operator_stack[-1][0].content] > precedence:
                    operators = operator_stack.pop()
                    num_operands = len(operators) + 1
                    associative_result = resolve_operators(stack[-num_operands:], operators)
                    stack[-num_operands:] = [associative_result]
                if not operator_stack or operator_precedence[operator_stack[-1][0].content] != precedence:
                    operator_stack.append([])
            operator_stack[-1].append(token)
        elif token.type == TokenType.COMMA:
            raise OptionError(
                f"Unknown formatting in layout search term \"{term}\": "
                f"unexpected comma at offset {token.offset}"
            )
        elif token.type == TokenType.OPEN_PAREN:
            operator_stack.append([token])
        elif token.type == TokenType.CLOSE_PAREN:
            while operator_stack and operator_stack[-1][0].content != '(':
                operators = operator_stack.pop()
                num_operands = len(operators) + 1
                associative_result = resolve_operators(stack[-num_operands:], operators)
                stack[-num_operands:] = [associative_result]
            if not operator_stack:
                raise OptionError(
                    f"Unknown formatting in layout search term \"{term}\": "
                    f"encountered closing ')' at offset {token.offset} when there are no opening parentheses to close"
                )
            operator_stack.pop()
        previous_type = token.type
        unary_multiplier = 1
        index += 1
    while operator_stack and operator_stack[-1][0].content != '(':
        operators = operator_stack.pop()
        num_operands = len(operators) + 1
        associative_result = resolve_operators(stack[-num_operands:], operators)
        stack[-num_operands:] = [associative_result]
    if operator_stack:
        raise OptionError(
            f"Unknown formatting in layout search term \"{term}\": "
            f"unclosed '(' at offset {operator_stack[-1][0].offset}"
        )
    assert len(stack) == 1
    result = stack[0]
    if result < 0:
        result = result + num_missions
    return result