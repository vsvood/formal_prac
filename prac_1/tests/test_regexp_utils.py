import pytest

from automaton_lib.regexp_utils import regexp_to_rpn


def test_bad_degree():
    with pytest.raises(Exception, match=r"Bad degree at \d+"):
        regexp_to_rpn("^")


def test_bad_degree_value():
    with pytest.raises(Exception, match="Bad degree value at 2: a"):
        regexp_to_rpn("a^a")


def test_braces_mismatch():
    with pytest.raises(Exception, match=r"No '\(' for '\)' at 1"):
        regexp_to_rpn("a)")


def test_bad_symbol():
    with pytest.raises(Exception, match=r"Unknown symbol at 0: ' '"):
        regexp_to_rpn(" ")


def test_multy_char_token():
    assert regexp_to_rpn("aaa") == ['aaa']


def test_splitting_degree():
    assert regexp_to_rpn("aa^*") == ['a', 'a', '*', '&']


def test_non_splitting_degree():
    assert regexp_to_rpn("a^+") == ['a', '+']


def test_mul_flag():
    assert regexp_to_rpn("a^*b") == ['a', '*', 'b', '&']


def test_digit_degree():
    assert regexp_to_rpn("a^21") == ['a', '21']


def test_braces():
    assert regexp_to_rpn("a(b+c)d") == ['a', 'b', 'c', '|', 'd', '&', '&']


def test_mul():
    assert regexp_to_rpn("a*b*c") == ['a', 'b', 'c', '&', '&']


def test_priority():
    assert regexp_to_rpn("a*b+c") == ['a', 'b', '&', 'c', '|']


def test_eps():
    assert regexp_to_rpn("a1") == ['a', '', '&']
