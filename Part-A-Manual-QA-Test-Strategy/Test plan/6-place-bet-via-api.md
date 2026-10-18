#### ID: 6
#### Title: POST /api/place-bet rejects invalid requests with correct error classes
#### Priority: High
#### Risk Rationale: The API is the last line of defence, UI validation can be bypassed
#### Preconditions:
1. Valid user ID U for x-user-id.
2. Balance reset via POST /api/reset-balance.
3. Valid match ID M taken from GET /api/matches.
4. Base body: {"matchId": M, "selection": "HOME", "stake": 10.00}
#### Steps:
For each row: send the request (base body with the change shown), check the status, then check GET /api/balance.
#### Test Data:
| #  | Change from base request                                                   | Expected status  |
|----|----------------------------------------------------------------------------|------------------|
| 1  | No x-user-id header                                                        | 401              |
| 2  | x-user-id: "" (blank)                                                      | 401              |
| 3  | Malformed JSON: {"matchId":                                                | 400              |
| 4  | Body is an array: []                                                       | 400              |
| 5  | Body is a string: "bet"                                                    | 400              |
| 6  | Method GET                                                                 | 405              |
| 7  | Method PUT                                                                 | 405              |
| 8  | selection: "WIN"                                                           | 422              |
| 9  | selection missing                                                          | 422              |
| 10 | matchId: ""                                                                | 422              |
| 11 | matchId: "unknown-123"                                                     | 422              |
| 12 | matchId missing                                                            | 422              |
| 13 | stake missing                                                              | 422              |
| 14 | stake: "abc"                                                               | 422              |
| 15 | stake: 0.99                                                                | 422              |
| 16 | stake: 100.01                                                              | 422              |
| 17 | stake: 10.123                                                              | 422              |
| 18 | Extra field: "foo": "bar"                                                  | 200              |
| 19 | Two identical requests in parallel                                         | One 200, one 409 |
| 20 | Setup: reset balance, place bets until balance = €50.00; then stake: 50.01 | 422              |
#### Expected result:
- Rows 1–17: the expected status is returned and GET /api/balance = B (no deduction).
- Row 18: 200; extra field ignored; GET /api/balance = B − 10.00.
- Row 19: exactly one 200 and one 409; GET /api/balance = B − 20.00 (cumulative after row 18).
- Row 20: 422 (insufficient balance); GET /api/balance = €50.00.
#### Related bugs: [BUG-005 - place-bet API accepts stake above balance](../Bugs/Bet-stake-above-balance-accepted-via-api.md), [BUG-007 - Repeated clicks on Place bet create multiple bets](../Bugs/Multiple-bets-on-repeated-place-bet-click.md)
