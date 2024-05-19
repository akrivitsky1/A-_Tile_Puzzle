from tiles import TilesNode
from queue import PriorityQueue

def heuristic(node: TilesNode) -> int:
    """Evaluate the heuristic value of the current node using the Manhattan distance."""
    goal_positions = {  # Defined goal positions for each tile for quick lookup.
        1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3),
        5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3),
        9: (2, 0), 10: (2, 1), 11: (2, 2), 12: (2, 3),
        13: (3, 0), 14: (3, 1), 15: (3, 2), 0: (3, 3)
    }
    total_distance = 0
    for i in range(4):
        for j in range(4):
            value = node.state[i][j]
            if value != 0:  # Ignoring the empty tile
                goal_x, goal_y = goal_positions[value]
                total_distance += abs(goal_x - i) + abs(goal_y - j)
    return total_distance  # Return the total Manhattan distance as the heuristic value.

def AStar(root, heuristic: callable) -> TilesNode or None:
    unexplored = PriorityQueue()
    counter = 0
    unexplored.put((0, counter, root))
    explored = set()
    g_score = {root: 0}
    f_score = {root: heuristic(root)}

    while not unexplored.empty():
        _, _, current = unexplored.get()
        if current.is_goal():
            return current.get_path()
        explored.add(current)

        for child in current.get_children():
            if child in explored:
                continue
            tentative_g_score = g_score[current] + 1
            if child not in g_score or tentative_g_score < g_score[child]:
                child.parent = current
                g_score[child] = tentative_g_score
                f_score[child] = tentative_g_score + heuristic(child)
                if child not in [item[-1] for item in unexplored.queue]:
                    counter += 1
                    unexplored.put((f_score[child], counter, child))

    return None  # return None if no path was found
