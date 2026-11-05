import pytest

from car_insurance_premium import (
    annual_premium,
    no_claim_bonus,
    claim_payout
)


# ---------------- ANNUAL PREMIUM ----------------

def test_unknown_car_type():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 1, False)


def test_driver_under_18():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 1, False)


def test_driver_under_25():
    assert annual_premium("hatchback", 20, 1, False) == 12000


def test_driver_age_25():
    assert annual_premium("sedan", 25, 1, False) == 12000


def test_driver_age_60():
    assert annual_premium("suv", 60, 1, False) == 17000


def test_zero_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_one_claim():
    assert annual_premium("sedan", 30, 1, False) == 12000


def test_more_than_two_claims():
    assert annual_premium("hatchback", 30, 3, False) == 16000


def test_anti_theft_discount():
    assert annual_premium("sedan", 30, 1, True) == 11500


# ---------------- NO CLAIM BONUS ----------------

def test_negative_years():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


def test_zero_years():
    assert no_claim_bonus(0) == 0


def test_one_year():
    assert no_claim_bonus(1) == 20


def test_three_years():
    assert no_claim_bonus(3) == 35


def test_five_years():
    assert no_claim_bonus(5) == 50


# ---------------- CLAIM PAYOUT ----------------

def test_negative_damage():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-100, 10000, 500, False)


def test_negative_deductible():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(100, 10000, -500, False)


def test_total_loss():
    assert claim_payout(5000, 20000, 500, True) == 20000


def test_not_total_loss():
    assert claim_payout(5000, 10000, 500, False) == 4500


def test_damage_equal_to_deductible():
    assert claim_payout(500, 10000, 500, False) == 0


def test_damage_below_deductible():
    assert claim_payout(100, 10000, 500, False) == 0


def test_payout_exceeds_insured_value():
    assert claim_payout(15000, 10000, 500, False) == 10000


def test_payout_within_insured_value():
    assert claim_payout(5000, 10000, 500, False) == 4500
