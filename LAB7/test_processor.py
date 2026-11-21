
from hypothesis import given, strategies as st
import pytest

from processor import (
    decode_promo_voucher,
    calculate_seat_tier_price,
    parse_attendee_badge
)


# Test 1: Promo Voucher
@given(
    prefix=st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll")),
        min_size=1,
        max_size=10
    ),
    percentage=st.integers(min_value=0, max_value=100)
)
def test_decode_promo_voucher(prefix, percentage):
    voucher = f"{prefix}-{percentage}"
    result = decode_promo_voucher(voucher)

    assert result == f"Valid {prefix.upper()}: {percentage}% OFF"


# Test 2: Seat Tier Price
@given(
    tier=st.sampled_from(["VIP", "PREMIUM", "GENERAL"]),
    row=st.integers(min_value=0, max_value=100)
)
def test_calculate_seat_tier_price(tier, row):
    result = calculate_seat_tier_price(f"{tier}@{row}")

    rates = {"VIP": 150.0, "PREMIUM": 90.0, "GENERAL": 45.0}

    assert result == rates[tier] + (row * 2.0)


# Test 3: Attendee Badge
@given(
   name=st.text(
    alphabet=st.characters(blacklist_characters=","),
    min_size=1,
    max_size=20
).filter(lambda x: x.strip() != ""),
    age=st.integers(min_value=0, max_value=120),
    seat=st.text(
    alphabet=st.characters(blacklist_characters=","),
    min_size=1,
    max_size=10
).filter(lambda x: x.strip() != "")
)
def test_parse_attendee_badge(name, age, seat):
    result = parse_attendee_badge(f"{name},{age},{seat}")

    category = "Child" if age < 18 else "Adult"

    assert result == f"{name.strip()} [{category}] - Seat {seat.strip()}"


# Test 4: Invalid Inputs
@pytest.mark.parametrize("voucher", ["", "EARLY", "EARLY-ABC"])
def test_invalid_voucher(voucher):
    with pytest.raises((ValueError, TypeError)):
        decode_promo_voucher(voucher)


@pytest.mark.parametrize("tier", ["UNKNOWN@4", "VIP", "VIP@ABC"])
def test_invalid_tier(tier):
    with pytest.raises((ValueError, KeyError, IndexError)):
        calculate_seat_tier_price(tier)


@pytest.mark.parametrize("badge", ["", "John", "John,ABC,A1"])
def test_invalid_badge(badge):
    with pytest.raises((ValueError, IndexError)):
        parse_attendee_badge(badge)
        
def test_negative_row():
    with pytest.raises(ValueError):
        calculate_seat_tier_price("VIP@-2")
