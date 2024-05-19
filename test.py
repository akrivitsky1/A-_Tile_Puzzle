import unittest
import random
from tiles import TilesNode
from astar import AStar, heuristic


class TestFifteensPuzzle(unittest.TestCase):
    def setUp(self):
        start_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 11], [13, 14, 15, 12]]
        self.fifteens_root = TilesNode(state=start_state)
        self.goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        self.goal_node = TilesNode(state=self.goal_state)

    @staticmethod
    def generate_random_test_case(steps=10):
        current_node = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
        )
        for _ in range(steps):
            children = current_node.get_children()
            current_node = random.choice(children)
        return current_node

    def test_randomly_generated_test_cases(self):
        random.seed(42)  # Seed the random number generator
        test_cases = [self.generate_random_test_case() for _ in range(10)]
        for test_case in test_cases:
            solution = AStar(test_case, heuristic)
            self.assertTrue(solution[-1].is_goal())

    def test_seed_consistency(self):
        random.seed(42)  # Seed the random number generator
        first_run = [self.generate_random_test_case().state for _ in range(10)]

        random.seed(42)  # Reset the seed
        second_run = [self.generate_random_test_case().state for _ in range(10)]

        self.assertEqual(
            first_run,
            second_run,
            "Generated test cases differ across runs with same seed.",
        )

    def test_is_goal(self):
        self.assertFalse(self.fifteens_root.is_goal())
        self.assertTrue(self.goal_node.is_goal())

    def test_generate_children(self):
        children = self.fifteens_root.get_children()
        self.assertIsInstance(children, list)
        for x in children:
            self.assertIsInstance(x, TilesNode)

        self.assertEqual(len(children), 4)

        child1 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0], [13, 14, 15, 12]]
        )
        child2 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 15, 11], [13, 14, 0, 12]]
        )
        child3 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 10, 11], [13, 14, 15, 12]]
        )
        child4 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 0, 8], [9, 10, 7, 11], [13, 14, 15, 12]]
        )

        true_children = [child1, child2, child3, child4]

        for child in children:
            self.assertIn(child, true_children)

    def test_evaluate_heuristic(self):
        goal_node = TilesNode(state=self.goal_state)
        self.assertEqual(heuristic(goal_node), 0)

    def test_astar(self):
        solution = AStar(self.fifteens_root, heuristic)
        for x in solution:
            self.assertIsInstance(x, TilesNode)
        self.assertTrue(solution[-1].is_goal())
        self.assertLessEqual(len(solution), 20)

    def test_node_equality(self):
        node1 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 11], [13, 14, 15, 12]]
        )
        node2 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 11], [13, 14, 15, 12]]
        )
        node3 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0], [13, 14, 15, 12]]
        )

        self.assertEqual(node1, node2, "Nodes with the same state should be equal.")
        self.assertNotEqual(
            node1, node3, "Nodes with different states should not be equal."
        )

    def test_node_hashing(self):
        node1 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 11], [13, 14, 15, 12]]
        )
        node2 = TilesNode(
            state=[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 0, 11], [13, 14, 15, 12]]
        )

        self.assertEqual(
            hash(node1),
            hash(node2),
            "Hashes of nodes with the same state should be equal.",
        )
        node_set = set()
        node_set.add(node1)
        self.assertIn(
            node2, node_set, "Nodes with the same state should be found in a set."
        )

    def test_get_children_bounds(self):
        node = TilesNode(
            state=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        )
        children = node.get_children()
        for child in children:
            self.assertNotEqual(
                child.state[0][0], 0, "Empty space should not move out of bounds."
            )

    def test_get_children_corners(self):
        corners = [
            TilesNode(
                state=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
            ),
            TilesNode(
                state=[[12, 13, 14, 0], [4, 5, 6, 3], [8, 9, 10, 11], [0, 1, 2, 15]]
            ),
        ]
        for node in corners:
            self.assertEqual(
                len(node.get_children()), 2, "Corners should have 2 children."
            )

    def test_get_children_edges(self):
        edges = [
            TilesNode(
                state=[[4, 0, 2, 3], [1, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
            ),
            TilesNode(
                state=[[1, 4, 2, 3], [0, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
            ),
        ]
        for node in edges:
            self.assertEqual(
                len(node.get_children()), 3, "Edges should have 3 children."
            )

    def test_get_children_center_1(self):
        center = [
            TilesNode(
                state=[[1, 2, 3, 4], [5, 6, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
            ),
            TilesNode(
                state=[[1, 2, 3, 4], [5, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
            ),
        ]
        for node in center:
            self.assertEqual(
                len(node.get_children()), 4, "Center should have 4 children."
            )

    def test_get_children_count(self):
        corners = [
            TilesNode(
                state=[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
            ),
            TilesNode(
                state=[[12, 13, 14, 0], [4, 5, 6, 3], [8, 9, 10, 11], [0, 1, 2, 15]]
            ),
        ]
        for node in corners:
            self.assertEqual(
                len(node.get_children()), 2, "Corners should have 2 children."
            )

    def test_is_goal_jumbled(self):
        node = TilesNode(
            state=[[12, 1, 10, 7], [11, 9, 6, 2], [5, 4, 3, 8], [13, 14, 0, 15]]
        )
        self.assertFalse(node.is_goal())

    def test_heuristic_goal(self):
        goal_node = TilesNode(state=self.goal_state)
        self.assertEqual(heuristic(goal_node), 0)

    def test_astar_unsolvable(self):
        state = [[1, 2, 3, 4], [5, 6, 8, 7], [9, 10, 11, 12], [13, 14, 15, 0]]
        root = TilesNode(state=state)
        self.assertFalse(root.is_solvable())

    def test_astar_already_solved(self):
        goal_node = TilesNode(state=self.goal_state)
        solution = AStar(goal_node, heuristic)
        self.assertEqual(len(solution), 1)
        self.assertTrue(solution[0].is_goal())

    def test_heuristic_consistency(self):
        state = [[12, 1, 10, 7], [11, 9, 6, 2], [5, 4, 3, 8], [13, 14, 0, 15]]
        node = TilesNode(state=state)
        for child in node.get_children():
            # h(n) <= cost(n, n') + h(n')
            self.assertLessEqual(
                heuristic(node),
                heuristic(child) + 1,
                "Heuristic is not consistent for transition from state:\n"
                + str(node.state)
                + "\nto state:\n"
                + str(child.state),
            )

    def test_solution_validity(self):
        random.seed(42)  # Seed the random number generator
        for i in range(10):
            solution = AStar(self.generate_random_test_case(steps=30), heuristic)

            for i in range(len(solution) - 1):
                current_state = solution[i].state
                next_state = solution[i + 1].state

                # Find the 0 (empty slot) in both states
                current_zero_pos = [
                    (x, y)
                    for x, row in enumerate(current_state)
                    for y, val in enumerate(row)
                    if val == 0
                ][0]
                next_zero_pos = [
                    (x, y)
                    for x, row in enumerate(next_state)
                    for y, val in enumerate(row)
                    if val == 0
                ][0]

                # Ensure that the positions differ by only one move
                delta_x = abs(current_zero_pos[0] - next_zero_pos[0])
                delta_y = abs(current_zero_pos[1] - next_zero_pos[1])

                # Ensure only one move has been made and it's valid
                self.assertTrue(
                    (delta_x == 1 and delta_y == 0) or (delta_x == 0 and delta_y == 1)
                )

                # Ensure only the tiles between the two positions have swapped
                for x in range(4):
                    for y in range(4):
                        if (x, y) != current_zero_pos and (x, y) != next_zero_pos:
                            self.assertEqual(current_state[x][y], next_state[x][y])
