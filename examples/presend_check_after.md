# Pre-send check

## When to use
Before any marketing delivery is scheduled, for every market, by a person or an agent.

## Never
- Never send or schedule. This playbook only reports.
- Never copy recipient rows into the report. Use counts.

## Steps
1. Confirm an unsubscribe link exists in the HTML.
2. Confirm the market legal footer block is present.
3. Compare every price against the market format (for example 1.299,00 € for AT, GR, HR, SI).
4. Confirm the audience includes the marketing-consent filter.
5. Confirm the send time is between 08:00 and 21:00 in the market's time zone.
6. Confirm a named person signed off the proof.

## Output
A table with one row per check: check name, PASS or FAIL, and the exact text that failed.
Overall verdict: BLOCK if any check fails, otherwise PASS.
