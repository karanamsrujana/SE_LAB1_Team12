# Lab 7 – Fuzz Testing with Hypothesis

## Objective
To perform fuzz testing using Hypothesis in Python by automatically generating different inputs and identifying errors and edge cases.

## Files
- `processor.py` – Contains the functions to be tested.
- `test_processor.py` – Contains Hypothesis-based test cases.

## Functions Tested
1. `decode_promo_voucher()` – Validates promotional voucher codes.
2. `calculate_seat_tier_price()` – Calculates ticket prices based on tier and row.
3. `parse_attendee_badge()` – Processes attendee details from CSV strings.

## Requirements
Install dependencies:

```bash
pip install pytest hypothesis
```

## Run Tests

```bash
pytest -v
```

## Expected Outcome
Identify unexpected inputs, unhandled exceptions, and edge cases using property-based testing.
