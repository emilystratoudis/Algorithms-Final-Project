# The Torchbearer

**Student Name:** Emilya Stratoudis
**Student ID:** 828413515
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  A single shortest path run from S is not enough because that only tells us the cheapest distance from each location to S but for this problem we need the shortest path in the best order of all the relics and that we can not find from just doing the single run from S to each part. 

- **What decision remains after all inter-location costs are known:**
  After all the inter location costs are known we just need to know the best order to visit them in before we reach the end of our path. 

- **Why this requires a search over orders (one sentence):**
  We need to search over many orders because different orders all have diffferent costs and just choosing the shortest path order sometimes will not give us the least total cost so we have to try out different ones. 

---

## Part 2: Precomputation Design

### Part 2a: Source Selection


| Source Node Type | Why it is a source |
|---|---|
| 'spawn' | This is a source because every route starts first at the entrance so first we need to find the shortest path from the spawn to every point |
| 'relics' | This is a source because after a relic is visited the planner might have to go to another before it exiits so we also need the shortest path from each relic to each other. |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested Dictionary |
| What the keys represent | The outer key is the source node and the inner key is the destination node |
| What the values represent | Values are the shortest fuel cost from the source to destination|
| Lookup time complexity | O(1) for the average case|
| Why O(1) lookup is possible | It is possible because in python dictonaries use hashing which means a direct key lookup has average O(1) cost |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** k + 1
- **Cost per run:** O(m log n)
- **Total complexity:** O(k + 1) * m log n)
- **Justification (one line):** Dijkstra runs once from the start and once from each of the relics. Each of these runs costs the system O(m log n) time so for the total it would be (k + 1) since that is the number of times Dikstra runs times each of the runs which cost O(m log n). 

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  At the start of each iteration of the loop every finalized node actaully has the shortest path distance from the source.

- **For nodes not yet finalized (not in S):**
  At the start of each iteration of the loop every non finalized node stores the minumum distamce that we know so far based on the nodes that already have been finalized.  

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  Before the first loop iteration, distance[source] = 0 and every other disatnce is infinity. This proves the invariant since the source has a path that has zero cost itself and no other paths have been discovered yet so it is the shortest ath distance from source at that moment. 

- **Maintenance : why finalizing the min-dist node is always correct:**
  Assuming the invariant holds at the strat of the loop and the queue chooses the unfinalized node with the smallest distance. When that node then gets finialized, nonnegative edge weights would guarentee that any path after through another unfinalized node only can add cost the the finalized disatnce can't become smaller. And relaxing the outgoing edges update the best discovered path for all other non finalized edges so the invariant P still hold true. 

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the loop terminates there are no more nodes left to improve. It uses the invariant at exit and every finalized node has its true shortest path disatnce from the source and any unreachable nodes stay infinite. 

### Part 3c: Why This Matters for the Route Planner

We need the correct distance from each path becuase that is what the planner uses to plan the final lowest cost route so if they are wrong the whole route could be incorrect. 

---

## Part 4: Search Design

### Why Greedy Fails


- **The failure mode:** The greedy could choose the closest next relic with least cost but does not consider the entire global cost and the effect that local choice has on that and the rest of the route. 
- **Counter-example setup:** S to A costs 1 and S to B costs 2 and A to B costs 100 and B to A costs 1 and A to T costs 1 and B to T costs 1.
- **What greedy picks:** Choose A first because it is shortest path from S.
- **What optimal picks:** Chooses B first then A and then T.
- **Why greedy loses:** Greedy looses since it has the path S -> A -> B -> T which has a cost of 102. But optimal chooses S -> B -> A -> T which only has a cost of 4. 

### What the Algorithm Must Explore

The algorithm hast to explore all different relic visit orders since the total cost depends on order of how you visit them. 

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location |current_loc|node|It is the node where the current route found is stored|
| Relics already collected |relics_visited_order|list|it is the relics that have been visited already and they are stored in the order that they were chosen|
| Fuel cost so far |cost_so_far|int|it is the total fuel cost that is used by the current route found|

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen |set|
| Operation: check if relic already collected | Time complexity: O(1)|
| Operation: mark a relic as collected | Time complexity: O(1)|
| Operation: unmark a relic (backtrack) | Time complexity: O(1)|
| Why this structure fits |I used a set since the search is recurive and needs to be able to remove and add items fast when it trys all different relics|

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** O(k!) 
- **Why:** Since there is a k amount of relics, the worst case would be that the serach tries k choices first and then k-1 and then k -2 whihc gives us the factorial number of orders. 

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** best which tracks the smallest complete route cost found so far and what order got that cost.
- **When it is used:** It is used inside _explore() before expanding. 
- **What it allows the algorithm to skip:** when cost_so_far >= best[0]. 

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** at current state the algorithm sees current_loc, relics_remaining, relics_visited_order, cost_so_far, and dist_table.
- **What the lower bound accounts for:** it accounts for the fuel we already spent which is represented by cost_so_far. 
- **Why it never overestimates:** it never overestimates since any route that is complete route from the state has to already have the fuel that is already spent and future costs will be nonnegative. 

### Part 6c: Pruning Correctness

Pruning is safe since when cost_so_far is greater then or equal to the best[0], then the partial route is already at least as expensive as the best complete route found. 

---

## References
- Lecture notes
- geeksforgeeks website
