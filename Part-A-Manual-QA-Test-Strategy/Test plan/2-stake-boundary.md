#### ID: 2
#### Title: Validate stake boundary
#### Priority: High
#### Risk Rationale: Prevents bets outside business limits
#### Preconditions:
1. Open application with authorised user.
2. Balance reset via POST /api/reset-balance (balance ≥ €100.00)
3. At least one match in list
4. "X" odds button selected; selection appears in bet slip with correct match and odds O
#### Steps:
For each row: clear the stake field, enter the value, check the result.
#### Test Data:
| # | Stake  | Expected message           | Placement |
|---|--------|----------------------------|-----------|
| 1 | 0.50   | Minimum stake is €1.00     | Blocked   |
| 2 | 0.99   | Minimum stake is €1.00     | Blocked   |
| 3 | 1.00   | None                       | Allowed   |
| 4 | 1.01   | None                       | Allowed   |
| 5 | 99.99  | None                       | Allowed   |
| 6 | 100.00 | None                       | Allowed   |
| 7 | 100.01 | Maximum stake is €100.00   | Blocked   |
| 8 | 105.00 | Maximum stake is €100.00   | Blocked   |