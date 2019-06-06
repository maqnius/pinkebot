# pinkebot (Telegram-Bot)

Divides a number by the number of group members in a telegram groupchat.

The formula is:

```python
result = arg / (number_groupmembers - 1) # - 1 because bot excludes itself from calculation
```

## Usage
```
/preis [Number] ([Currency])
```
If there is a second argument (Currency) it is appended to the result.

## Example
```
Testuser:
>>> /preis 5 €

Adam Riese:
>>> Pro Person: 2.50 €
```
