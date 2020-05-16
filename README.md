# The Problem
## tl;dr
I have `n` people seated around a circular table. At each step, I choose any two people and switch their seats. What is the minimum number of steps required such that every person has sat either to the right or to the left of everyone else? [Full Detail at MSE](http://math.stackexchange.com/questions/833541/making-friends-around-a-circular-table).

## Flavor Text

King Arthur meets his knights at a round table, with a total of `n` people at the table. Two individuals consider themselves "bromigos" if they have sat next to each other at some meeting. A list of "bromigos" is currently maintained in the chancellor's scrolls.

Tradition demands that, at every meeting, the seating arrangement must stay the same, save for a pair of knights chosen by the King (one of whom could be the King himself) who must switch seats.

Having recently heard of 6.006 at MIT, King Arthur has become interested in the minimum number of steps it would take for a new set of knights (and King Arthur) to all be "bromigos".

Given that the size of the castle is finite, King Arthur hopes that your space complexity will also be reasonable.