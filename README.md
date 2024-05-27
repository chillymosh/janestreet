These are various solutions to a Jane Street mock interview question.

```
Unit Conversions.

Write a program that can answer unit conversion questions. e.g. How many meters x inches given a list of facts of units.

Format of facts = tuple(strings, float, string)
Fomat of queries = tuple(float, string, string)

example facts:
    m = 3.28 ft
    ft = 12 in
    hr = 60 min
    min = 60 sec

 example queries:
    2 m = ? in --> answer = 78.72
    13 in = ? m --> answer = 0.330 (roughly)
    13 in = ? hr --> 'not convertible!'
```
