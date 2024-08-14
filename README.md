# ProgrammingLanguageProject


Parsing Error Detection: 

Parsing: 42 + 10 +
Parsing failed: Invalid factor at position 9 

Parsing: 42 + 10 ^
Parsing failed: Invalid token: ^ at position 9

Parsing: 42 ^ 10
Parsing failed: Invalid token: ^ at position 4

Parsing: 42 + 10 True
Parsing failed: Expected end of input at position 12

Parsing: + 42 + 10
Parsing failed: Invalid factor at position 1

Parsing: 42 + 10 3
Parsing failed: Expected end of input at position 9

Parsing: True 42 + 10
Parsing failed: Expected end of input at position 7 //why at position 7?

*******************************
Parsing: 42 + 10 + True
Parsing successful - NOT GOOD - We need to declair an error 

Parsing: True + 42 + 10
Parsing successful - NOT GOOD - We need to declair an error
*******************************
*after the "42 + 10" it expects an operator or EOF -> so if the string has operator we want to have only integer before&after

Fixed - 

Parsing: True + 42 + 10
Parsing failed: Cannot use boolean in arithmetic expression


Boolean:

True = 1
False = 0 
