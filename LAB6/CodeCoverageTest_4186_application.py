import pytest

from car_insurance_premium import (
    annual_premium,
    no_claim_bonus,
    claim_payout
)


# ---------------- ANNUAL PREMIUM TESTS ----------------

def test_invalid_car_type():
    with pytest.raises(ValueError, match="unknown car type"):
        annual_premium("truck", 30, 0, False)


def test_driver_too_young():
    with pytest.raises(ValueError, match="driver too young"):
        annual_premium("sedan", 17, 0, False)


def test_driver_below_25():
    assert annual_premium("hatchback", 20, 1, False) == 12000


def test_driver_above_60_with_claims_and_anti_theft():
    assert annual_premium("suv", 60, 3, True) == 33500


def test_zero_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


# ---------------- NO CLAIM BONUS TESTS ----------------

def test_negative_claim_free_years():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)


def test_zero_claim_free_years():
    assert no_claim_bonus(0) == 0


def test_one_claim_free_year():
    assert no_claim_bonus(1) == 20


def test_three_claim_free_years():
    assert no_claim_bonus(3) == 35


def test_five_claim_free_years():
    assert no_claim_bonus(5) == 50


# ---------------- CLAIM PAYOUT TESTS ----------------

def test_negative_damage_cost():
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(-100, 10000, 500, False)


def test_total_loss():
    assert claim_payout(5000, 20000, 500, True) == 20000


def test_damage_below_deductible():
    assert claim_payout(100, 10000, 200, False) == 0


def test_normal_claim_payout():
    assert claim_payout(5000, 10000, 500, False) == 4500


def test_payout_exceeds_insured_value():
    assert claim_payout(15000, 10000, 500, False) == 10000
