#### ID: 5
#### Title: Failed placement shows error modal, Rebet, Close and X behave correctly
#### Priority: High
#### Risk Rationale: Failed bets must not charge the user, recovery actions must not duplicate or lose bets
#### Preconditions:
1. Open application with authorised user.
2. Balance reset via POST /api/reset-balance.
3. At least one match in list.
4. POST /api/place-bet can be forced to return 500 (network interception/mock).
#### Steps:
1. Select the "1" odds button and enter stake 10.00.
2. Enable 500 mock; click "Place Bet".
3. Disable mock, click "Rebet".
4. Close receipt. Select "1", enter 10.00, enable 500 mock, click "Place Bet".
5. Click "Close".
6. Select "1", enter 10.00, click "Place Bet" (mock still active).
7. Click top-right "X".
#### Expected result:
1. Selection appears in bet slip with correct match and odds O.
2. Button shows "Placing...", then error modal appears:
   - Title: "Something went wrong"
   - Body: bet could not be processed, suggests trying again
   - Actions: "Rebet" (primary), "Close" (secondary), "X"
   Displayed balance and GET /api/balance = B.
3. Modal closes; retry sends POST /api/place-bet with the same matchId, selection HOME, stake 10.00.
   Success receipt shown; displayed balance and GET /api/balance = B − 10.00.
4. Error modal appears; balance stays B − 10.00.
5. Modal closes; no active selection, stake field empty; balance stays B − 10.00.
6. Error modal appears; balance stays B − 10.00.
7. Same as step 5.