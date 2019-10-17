# slitherlink
Python script that solves Slither Link puzzle. Check example of such a puzzle here: https://www.janko.at/Raetsel/Slitherlink/0870.a.htm

It can solve small puzzles very fast. For the biggest ones (like 45 columns per 30 rows) it can take a few hours. The plan is to optimize it:
- optimize the code of tests
- minimize the number of tests by testing not all the cells, but only those close to recent changes. It might be smarter.
