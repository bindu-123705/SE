import pytest
from recycling_rewards import (
    reward_points,
    collection_accepted,
    slot_status,
)


# reward_points tests
def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0


def test_unknown_material():
    with pytest.raises(ValueError):
        reward_points("glass", 10, False)


def test_negative_weight():
    with pytest.raises(ValueError):
        reward_points("paper", -1, False)


def test_paper_bonus():
    assert reward_points("paper", 5, True) == 6


def test_plastic_reward():
    assert reward_points("plastic", 5, False) == 12


def test_metal_reward():
    assert reward_points("metal", 5, False) == 36


def test_metal_bonus_ignored():
    assert reward_points("metal", 3, True) == 12


def test_high_weight_nonmetal():
    assert reward_points("paper", 27, False) == 220


def test_high_weight_metal():
    assert reward_points("metal", 23, False) == 378


# collection_accepted tests
def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True


def test_hazardous_accepted():
    assert collection_accepted(5, 10, True) is True


def test_hazardous_rejected():
    assert collection_accepted(6, 1, True) is False


def test_weight_over_limit():
    assert collection_accepted(51, 1, False) is False


def test_too_many_bags():
    assert collection_accepted(20, 4, False) is False


# slot_status tests
def test_morning_open():
    assert slot_status(20, True, False) == "open"


def test_nonmorning_open():
    assert slot_status(10, False, False) == "open"


def test_holiday_open():
    assert slot_status(35, True, True) == "open"


def test_late_status():
    assert slot_status(10, True, False) == "late"


def test_missed_status():
    assert slot_status(4, True, False) == "missed"
