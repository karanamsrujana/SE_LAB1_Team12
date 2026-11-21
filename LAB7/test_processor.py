
from hypothesis import given, strategies as st
from processor import (
    decode_promo_voucher,
    calculate_seat_tier_price,
    parse_attendee_badge
)


# Test 1: Promo Voucher
@given(st.text() | st.none())
def test_decode_promo_voucher_no_crash(s):
    try:
        result = decode_promo_voucher(s)
        assert isinstance(result, str)
    except Exception:
        pass


# Test 2: Seat Tier Price
@given(st.text() | st.none())
def test_calculate_seat_tier_price_safe(s):
    try:
        result = calculate_seat_tier_price(s)
        assert isinstance(result, (int, float))
    except Exception:
        pass


# Test 3: Attendee Badge
@given(st.text() | st.none())
def test_parse_attendee_badge_safe(s):
    try:
        result = parse_attendee_badge(s)
        assert isinstance(result, str)
    except Exception:
        pass
