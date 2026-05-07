# Development Log – The Torchbearer

**Student Name:** Emilya Stratoudis
**Student ID:** 828413515

---

## Entry 1 – 5/6/2026: Initial Plan

So first I will try to implement the Dijkstra's algoirthm since it is kind of what the whole project builds off on. After I have that implemented I will try to make the distance table so I can write the recusive search over the orders in from the table. I think the hardest part will be stopping to explore a path if its too expensive without missing actual valid values that will give me the best route. I will test my results with the test given and I solved the problem myself on the side too so I will also use that to see if I am getting correct results.

---

## Entry 2 – 5/6/2026:

I forgot to skip unreachable paths with infinity at first.

---


## Entry 4 – [5/6/2026]: Post-Implementation Reflection

I noticed after that in my select_sources I never actually used exit_node but it did pass the parameter and the test so I did not end up changing it but it could be added and used in the future. Also maybe there would be a better way to search through the relic orders rather then just try every single one. Since we dont have a lot of them it is fine for my code but if there a lot it would take a really long time to run. Lastly, my recursive function could be cleaned up while I was testing it the backtracking was getting confusing so I could make that more clear. 

---

## Final Entry – 5/6/2026: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis |0.5|
| Part 2: Precomputation Design |0.75|
| Part 3: Algorithm Correctness |0.75|
| Part 4: Search Design |0.5|
| Part 5: State and Search Space |0.5|
| Part 6: Pruning |0.5|
| Part 7: Implementation |2 - 3|
| README and DEVLOG writing |1 - 2|
| **Total** |6 - 7|
