import comparator
import encoder


def test_isomorphism_used_mismatch():
    with open("test/comparator/used_mismatch_1.doa", 'r') as f:
        machine_1 = encoder.decode(f.read())
    with open("test/comparator/used_mismatch_2.doa", 'r') as f:
        machine_2 = encoder.decode(f.read())
    assert not comparator.check_isomorphism(machine_1, machine_2)


def test_isomorphism_trigger_mismatch():
    with open("test/comparator/trigger_mismatch_1.doa", 'r') as f:
        machine_1 = encoder.decode(f.read())
    with open("test/comparator/trigger_mismatch_2.doa", 'r') as f:
        machine_2 = encoder.decode(f.read())
    assert not comparator.check_isomorphism(machine_1, machine_2)


def test_isomorphism_trigger_number_mismatch():
    with open("test/comparator/trigger_number_mismatch_1.doa", 'r') as f:
        machine_1 = encoder.decode(f.read())
    with open("test/comparator/trigger_number_mismatch_2.doa", 'r') as f:
        machine_2 = encoder.decode(f.read())
    assert not comparator.check_isomorphism(machine_1, machine_2)


def test_end_mismatch_1():
    with open("test/comparator/end_mismatch_1_1.doa", 'r') as f:
        machine_1 = encoder.decode(f.read())
    with open("test/comparator/end_mismatch_1_2.doa", 'r') as f:
        machine_2 = encoder.decode(f.read())
    assert not comparator.check_isomorphism(machine_1, machine_2)


def test_end_mismatch_2():
    with open("test/comparator/end_mismatch_2_1.doa", 'r') as f:
        machine_1 = encoder.decode(f.read())
    with open("test/comparator/end_mismatch_2_2.doa", 'r') as f:
        machine_2 = encoder.decode(f.read())
    assert not comparator.check_isomorphism(machine_1, machine_2)


def test_isomorphism_success():
    with open("test/comparator/success_1.doa", 'r') as f:
        machine_1 = encoder.decode(f.read())
    with open("test/comparator/success_2.doa", 'r') as f:
        machine_2 = encoder.decode(f.read())
    assert comparator.check_isomorphism(machine_1, machine_2)


def test_equality_success():
    with open("test/comparator/equal_1.doa", 'r') as f:
        machine_1 = encoder.decode(f.read())
    with open("test/comparator/equal_2.doa", 'r') as f:
        machine_2 = encoder.decode(f.read())
    assert comparator.check_equality(machine_1, machine_2)


def test_equality_success_1():
    with open("test/comparator/input.doa", 'r') as f:
        machine_1 = encoder.decode(f.read())
    with open("test/comparator/output.doa", 'r') as f:
        machine_2 = encoder.decode(f.read())
    assert comparator.check_equality(machine_1, machine_2)

