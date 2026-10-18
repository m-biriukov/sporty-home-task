#### ID: 1
#### Title: Successful bet placement
#### Priority: Critical
#### Risk Rationale: Core revenue flow
#### Preconditions:
1. Open application with authorised user.
2. Balance reset via POST /api/reset-balance
3. At least one match in list
#### Steps:
1. Select an "1" odds button
2. Enter valid stake (5.5).
3. Click place bet.
4. Close modal.
#### Expected result:
1. Selection appears in bet slip with correct match and odds O. 
2. Bet slip shows stake as 5.5 + potential payout = 5.5 * odds
3. Button shows "Placing..." and is disabled. 
   Success modal is shown with:
   - Bet ID (non-empty)
   - Match details (step 1)
   - Selection (HOME)
   - Stake (5.5)
   - Odds at placement
   - Potential payout
   - Placement timestamp 
- Displayed balance = Previous balance - 5.5
4. Main page shows no active selection, stake field empty
#### Related bugs: [BUG-001 - Past events shown in Upcoming list and accept bets](../Bugs/Past-events-displayed-in-match-list.md), [BUG-002 - Wrong potential payout in bet confirmation](../Bugs/Wrong-potential-payout-in-bet-confirmation.md), [BUG-003 - Teams swapped in bet confirmation](../Bugs/Teams-swapped-in-bet-confirmation.md), [BUG-006 - Balance not updated after bet placement](../Bugs/Balance-not-updated-after-bet-placement.md)
