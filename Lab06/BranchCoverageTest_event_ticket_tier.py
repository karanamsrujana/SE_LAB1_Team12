
import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


def test_invalid_manifest_type():
    with pytest.raises(ValueError):
        process_ticket_manifest(None, 0)


def test_negative_tax():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


def test_valid_empty_manifest():
    assert process_ticket_manifest([], 0)["status"] == "ZERO_SALES"


def test_unconfirmed_manifest():
    result = process_ticket_manifest(
        [{"is_confirmed": False, "tier": "vip"}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_confirmed_manifest():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 45.0


def test_vip_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 150.0


def test_premium_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "premium",
          "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_general_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 45.0


def test_unknown_tier_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "unknown"}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_empty_orders():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general", "orders": []}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_invalid_quantity_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 0}, {"qty": -1}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_valid_quantity_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_vip_fraud_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 1, "promo": "FRAUD_RISK"}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_non_vip_fraud_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "FRAUD_RISK"},
                     {"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 180.0


def test_earlybird_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "premium",
          "orders": [{"qty": 2, "promo": "EARLYBIRD"}]}], 0
    )
    assert result["total_revenue"] == 144.0


def test_bulk_discount_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 5, "promo": "OTHER"}]}], 0
    )
    assert result["total_revenue"] == 205.0


def test_no_bulk_discount_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "OTHER"}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_lounge_true():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": True, "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 120.0


def test_lounge_false():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": False, "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 45.0


def test_audit_rejected_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "unknown"}
         for _ in range(5)], 0
    )
    assert result["status"] == "AUDIT_REJECTED"


def test_zero_sales_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general", "orders": []}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_completed_branch():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0.1
    )
    assert result["status"] == "COMPLETED"


def test_gate_empty_branch():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_non_empty_branch():
    assert monitor_gate_flow([[]]) == "FLOW_NORMAL"


def test_gate_high_rate():
    assert monitor_gate_flow([[60]]) == "FLOW_NORMAL"


def test_gate_reset_branch():
    assert monitor_gate_flow([[60, 50, 60]]) == "FLOW_NORMAL"


def test_gate_overflow_branch():
    assert monitor_gate_flow([[60, 55]]) == "OVERFLOW"


def test_gate_separate_streams():
    assert monitor_gate_flow([[60], [70]]) == "FLOW_NORMAL"
