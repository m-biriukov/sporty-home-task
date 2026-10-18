#### ID: 4
#### Title: Duplicate submission does not create two bets
#### Priority: Critical
#### Risk Rationale: Prevents double-charging users and duplicate financial liability
#### Preconditions:
1. Open application with authorised user.
2. Balance reset via POST /api/reset-balance
3. At least one match in list
#### Steps:
1. Select the "2" odds button
2. Enter stake as 50
3. Double-click "Place Bet" (two clicks without waiting)
#### Expected result:
1. Selection appears in bet slip with correct match and odds O.
2. No error; potential payout = 50.00 × odds.
3. After the first click, button shows "Placing..." and is disabled.
   Exactly one POST /api/place-bet request is sent.
   One success receipt with a single Bet ID is shown.
   Displayed balance and GET /api/balance = B − 50.00.
#### Related bugs: [BUG-007 - Repeated clicks on Place bet create multiple bets](../Bugs/Multiple-bets-on-repeated-place-bet-click.md)
