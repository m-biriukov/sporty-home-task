#### ID: 3
#### Title: Stake exceeding available balance is rejected
#### Priority: Critical
#### Risk Rationale: Prevents bets the user can’t cover
#### Preconditions:
1. Open application with authorised user.
2. Balance reset via POST /api/reset-balance
3. At least one match in list
4. Make a balance lower than 100 (make a bet for 50 Euro)
#### Steps:
1. Select the "2" odds button
2. Enter stake Balance + 0.01.
3. Clear field, enter stake B, click "Place Bet".
#### Expected result:
1. Selection appears in bet slip with correct match and odds O.
2. "Insufficient balance" error is shown, Place bet button is blocked (/api/balance shows balance)
3. No error, bet placed successfully, balance changed (/api/balance shows 0 Euro)
#### Related bugs: [BUG-005 - place-bet API accepts stake above balance](../Bugs/Bet-stake-above-balance-accepted-via-api.md)
