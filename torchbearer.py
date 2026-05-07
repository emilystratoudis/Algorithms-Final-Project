"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Emily Stratoudis
Student ID:   828413515

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    return """
- A single shortest path run from S is not enough because that only tells us the cheapest distance from each location to S but for this problem we need the shortest path in the best order of all the relics and that we can not find from just doing the single run from S to each part.
- After all the inter location costs are known we just need to know the best order to visit them in before we reach the end of our path.
- We need to search over many orders because different orders all have diffferent costs and just choosing the shortest path order sometimes will not give us the least total cost so we have to try out different ones.

"""


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):

    #strating at spawn 
    seen = {spawn}
    sources = [spawn]

    #adding each relic
    for relic in relics:
        if relic not in seen:
            seen.add(relic)
            sources.append(relic)

    return sources


def run_dijkstra(graph, source):
    # using min heap for storing my distances and nodes
    pq = [(0, source)]

    # collecting all the nodes and initalizing the disatnces to infinity
    nodes = set(graph.keys())
    for node in graph:
        for vertex, cost in graph[node]:
            nodes.add(vertex)

    distance = {node: float("inf") for node in nodes}
    distance[source] = 0

    while pq:
        d, u = heapq.heappop(pq)

        # if not the lastets shortest distance skip
        if d > distance[u]:
            continue

        #explore others of the current
        for v, w in graph.get(u, []):
            #update if shorter path to v through u is found
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                heapq.heappush(pq, (distance[v], v))

    return distance


def precompute_distances(graph, spawn, relics, exit_node):
   
    dist_table = {}

    #running dijkstra for each source
    for source in select_sources(spawn,relics,exit_node):
       dist_table[source] = run_dijkstra(graph, source)

    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
   
    return """
-For nodes already finalized (in S): At the start of each iteration of the loop every finalized node actaully has the shortest path distance from the source.
-For nodes not yet finalized (not in S): At the start of each iteration of the loop every non finalized node stores the minumum distamce that we know so far based on the nodes that already have been finalized.
-Initialization : why the invariant holds before iteration 1: Before the first loop iteration, distance[source] = 0 and every other disatnce is infinity. This proves the invariant since the source has a path that has zero cost itself and no other paths have been discovered yet so it is the shortest ath distance from source at that moment.
-Maintenance : why finalizing the min-dist node is always correct: Assuming the invariant holds at the strat of the loop and the queue chooses the unfinalized node with the smallest distance. When that node then gets finialized, nonnegative edge weights would guarentee that any path after through another unfinalized node only can add cost the the finalized disatnce can't become smaller. And relaxing the outgoing edges update the best discovered path for all other non finalized edges so the invariant P still hold true.
-Termination : what the invariant guarantees when the algorithm ends: When the loop terminates there are no more nodes left to improve. It uses the invariant at exit and every finalized node has its true shortest path disatnce from the source and any unreachable nodes stay infinite.
-We need the correct distance from each path becuase that is what the planner uses to plan the final lowest cost route so if they are wrong the whole route could be incorrect.

"""


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    
    return """
-The failure mode: The greedy could choose the closest next relic with least cost but does not consider the entire global cost and the effect that local choice has on that and the rest of the route.
-Counter-example setup: S to A costs 1 and S to B costs 2 and A to B costs 100 and B to A costs 1 and A to T costs 1 and B to T costs 1.
-What greedy picks: Choose A first because it is shortest path from S.
-What optimal picks: Chooses B first then A and then T.
-Why greedy loses: Greedy looses since it has the path S -> A -> B -> T which has a cost of 102. But optimal chooses S -> B -> A -> T which only has a cost of 4.
-The algorithm hast to explore all different relic visit orders since the total cost depends on order of how you visit them.

"""


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    best = [float("inf"), []]

    #using my helper function to exlore all the possible roots
    _explore(dist_table, spawn, set(relics), [],0, exit_node, best)
    cost, path = best

    return cost, path



def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    
    # my pruning condition is safe since all the next traversal costs are nonnegative
    # so there is no point in continuing if I already spent more than the best route found 

    if cost_so_far >= best[0]:
        return
    
    #base case if there is nothign left to collect finish the route
    if len(relics_remaining) == 0:

        #shortest pah cost from curr to exit
        exitCost = dist_table[current_loc].get(exit_node, float("inf"))

        # if the end can't be reached its an invalid route
        if exitCost == float("inf"):
            return
        
        totalCost = cost_so_far + exitCost

        #updating our best if the route is better
        if totalCost < best[0]:
            best[0] = totalCost
            best[1] = list(relics_visited_order)
        return

    #try each relic that is left 
    for nextRelic in list(relics_remaining):

        #shortest path cost from curr to next 
        traversalCost = dist_table[current_loc].get(nextRelic, float("inf"))

        #skipping any unreachable relics
        if traversalCost == float("inf"):
            continue
        
        #next relic
        relics_remaining.remove(nextRelic)
        relics_visited_order.append(nextRelic)

        #building our route
        _explore(dist_table, nextRelic, relics_remaining, relics_visited_order, cost_so_far + traversalCost, exit_node,best)

        #backtracking
        relics_visited_order.pop()
        relics_remaining.add(nextRelic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):

    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
