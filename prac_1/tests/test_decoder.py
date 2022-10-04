"""Decoder tests"""
import pytest

from automaton_lib.comparator import check_equality
from automaton_lib.encoder import decode


def test_bad_format():
    with pytest.raises(Exception, match=r"Unknown format '.+'"):
        decode("", "abracadabra")


def test_broken_header():
    data = """XXX
Start: 0
Acceptance: 2
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: header\. Expected 'DOA: v1' line, '.+' found"):
        decode(data, "doa")


def test_no_start():
    data = """DOA: v1
Acceptance: 2
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: start\. Expected 'Start:' line, '.+' found"):
        decode(data, "doa")


def test_no_acceptance():
    data = """DOA: v1
Start: 0
--BEGIN--
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: acceptance\. Expected 'Acceptance:' line, '.+' found"):
        decode(data, "doa")


def test_no_begin():
    data = """DOA: v1
Start: 0
Acceptance: 2
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: begin\. Expected '--BEGIN--' line, '.+' found"):
        decode(data, "doa")


def test_broken_state_block():
    data = """DOA: v1
Start: 0
Acceptance: 2
--BEGIN--
    -> ab 1
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: '->' statement before State declaration"):
        decode(data, "doa")


def test_unknown_statement():
    data = """DOA: v1
Start: 0
Acceptance: 2
--BEGIN--
abobabass
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: '->' or 'State:' statement expected, '.+' found"):
        decode(data, "doa")


def test_unknown_statement_long():
    data = """DOA: v1
Start: 0
Acceptance: 2
--BEGIN--
a b c d e f g h i j k l m n o p
--END--
"""
    with pytest.raises(Exception,
                       match=r"Format error: '->' or 'State:' statement expected, '.+' found"):
        decode(data, "doa")


def test_simple_build():
    data = """DOA: v1
Start: 0
Acceptance: 1
--BEGIN--
State: 0
    -> a 1
--END--
"""
    machine = decode(data, "doa")

    assert machine.start_idx == {'0', }
    assert machine.end_idx == {'1', }
    assert len(machine.states) == 2
    assert len(machine.states['0'].links) == 1
    assert machine.states['0'].links['a'] == {'1', }
    assert len(machine.states['1'].links) == 0


def test_single_token():
    data = "DOA: v1\n" \
           "Start: 0\n" \
           "Acceptance: 1\n" \
           "--BEGIN--\n" \
           "State: 0\n" \
           "  -> aa 1\n" \
           "--END--\n"
    assert check_equality(decode("aa", "regexp"), decode(data, "doa"))


def test_plus():
    data = "DOA: v1\n" \
           "Start: 0\n" \
           "Acceptance: 1 & 2\n" \
           "--BEGIN--\n" \
           "State: 0\n" \
           "  -> a 1\n" \
           "  -> b 2\n" \
           "--END--\n"
    assert check_equality(decode("a+b", "regexp"), decode(data, "doa"))


def test_mul():
    data = "DOA: v1\n" \
           "Start: 0\n" \
           "Acceptance: 1\n" \
           "--BEGIN--\n" \
           "State: 0\n" \
           "  -> ab 1\n" \
           "--END--\n"
    assert check_equality(decode("a*b", "regexp"), decode(data, "doa"))


def test_kleene_plus():
    data = "DOA: v1\n" \
           "Start: 0\n" \
           "Acceptance: 1\n" \
           "--BEGIN--\n" \
           "State: 0\n" \
           "  -> a 1\n" \
           "State: 1\n" \
           "  -> a 1\n" \
           "--END--\n"
    assert check_equality(decode("a^+", "regexp"), decode(data, "doa"))


def test_kleene_star():
    data = "DOA: v1\n" \
           "Start: 0\n" \
           "Acceptance: 0\n" \
           "--BEGIN--\n" \
           "State: 0\n" \
           "  -> a 0\n" \
           "--END--\n"
    assert check_equality(decode("a^*", "regexp"), decode(data, "doa"))


def test_digit_degree():
    data = "DOA: v1\n" \
           "Start: 0\n" \
           "Acceptance: 1\n" \
           "--BEGIN--\n" \
           "State: 0\n" \
           "  -> aaaaa 1\n" \
           "--END--\n"
    assert check_equality(decode("a^5", "regexp"), decode(data, "doa"))
