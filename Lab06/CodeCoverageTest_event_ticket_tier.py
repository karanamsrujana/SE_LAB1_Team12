
import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


def test_invalid_manifests():
    with pytest.raises(ValueError):
        process_ticket_manifest({}, 0.1)


def test_negative_tax():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


def test_unconfirmed_manifest():
    result = process_ticket_manifest(
        [{"is_confirmed": False, "tier": "vip"}], 0.1
    )
    assert result["status"] == "ZERO_SALES"


def test_vip_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 1}]}], 0.1
    )
    assert result["total_revenue"] == 165.0


def test_premium_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "premium",
          "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_general_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0.1
    )
    assert result["total_revenue"] == 99.0


def test_invalid_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "student"}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_default_tier_and_orders():
    result = process_ticket_manifest(
        [{"is_confirmed": True}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_zero_quantity():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 0}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_negative_quantity():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": -2}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_earlybird_discount():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "EARLYBIRD"}]}], 0
    )
    assert result["total_revenue"] == 72.0


def test_bulk_discount():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 5}]}], 0
    )
    assert result["total_revenue"] == 205.0


def test_non_vip_fraud_order():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "FRAUD_RISK"}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_vip_fraud_order():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 1}, {"qty": 1, "promo": "FRAUD_RISK"},
                     {"qty": 2}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_lounge_fee():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": True, "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 165.0


def test_audit_rejected():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "unknown"}
         for _ in range(5)], 0
    )
    assert result["status"] == "AUDIT_REJECTED"


def test_tax_calculation():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0.1
    )
    assert result["total_revenue"] == 99.0


def test_gate_no_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_normal():
    assert monitor_gate_flow([[20, 50, 30]]) == "FLOW_NORMAL"


def test_gate_overflow():
    assert monitor_gate_flow([[60, 51]]) == "OVERFLOW"


def test_gate_streak_reset():
    assert monitor_gate_flow([[60, 40, 70]]) == "FLOW_NORMAL"
