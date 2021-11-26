# ftxcoinstaker

Ref: https://medium.com/@cjolowicz/hypermodern-python-d44485d9d769#2050


Flow:

Init
 - Load SR Zones
 - Load / Create Internal DB / JSON File
 - Map Open Order with SR Zones

Loop:
 - Get Timestamp
 - Get all open orders
    - Check if some 'sell' orders have been executed since the previous timestamps
    - Redistribute gains (Place / Update lower orders across lower Resistances / take profit)
    - Check if some 'buy' orders have been executed since the previous timestamps
    - Place / Update higher orders across upper Resitances Zones
 - Slack Summary
 - Get current price:
    - if current price > higher sr range => place trailing stop order
 - Slack Alerts