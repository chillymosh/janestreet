from __future__ import annotations
from queue import Queue

"""
example facts:
    m = 3.28 ft
    ft = 12 in
    hr = 60 min
    min = 60 sec

 example queries:
    2 m = ? in --> answer = 78.72
    13 in = ? m --> answer = 0.330 (roughly)
    13 in = ? hr --> 'not convertible!'
"""


Fact = tuple[str, float | int, str]
Query = tuple[float | int, str, str]


class Node:
    def __init__(self, unit: str) -> None:
        self.unit: str = unit
        self.edges: list[Edge] = []

    def add_edge(self, multiplier: float, other_node: Node) -> None:
        edge = Edge(multiplier, other_node)
        self.edges.append(edge)


class Edge:
    def __init__(self, multiplier: float, node: Node):
        self.multiplier = multiplier
        self.node = node


def parse_facts(facts: list[Fact]) -> dict[str, Node]:
    name_to_node: dict[str, Node] = {}
    for left_unit, multiplier, right_unit in facts:
        if left_unit not in name_to_node:
            left_node = Node(left_unit)
            name_to_node[left_unit] = left_node
        if right_unit not in name_to_node:
            right_node = Node(right_unit)
            name_to_node[right_unit] = right_node
        name_to_node[left_unit].add_edge(multiplier, name_to_node[right_unit])
        name_to_node[right_unit].add_edge(1 / multiplier, name_to_node[left_unit])

    return name_to_node


def answer_query(query: Query, facts: dict[str, Node]) -> float | None:
    starting_amount, from_unit, to_unit = query
    if from_unit not in facts:
        return None
    if to_unit not in facts:
        return None

    from_node = facts[from_unit]
    to_node = facts[to_unit]

    to_visit: Queue[tuple[Node, float]] = Queue()
    to_visit.put((from_node, starting_amount))
    visited = {from_node}
    while not to_visit.empty():
        current_node, current_amount = to_visit.get()
        if current_node == to_node:
            return current_amount

        for edge in current_node.edges:
            if edge.node not in visited:
                visited.add(edge.node)
                with_latest_multiplier = current_amount * edge.multiplier
                to_visit.put((edge.node, with_latest_multiplier))

    return None


facts = parse_facts([("m", 3.28, "ft"), 
                     ("ft", 12, "in"), 
                     ("hr", 60, "min"), 
                     ("min", 60, "sec")])

queries = [(2, "m", "in"), 
           (13, "in", "m"), 
           (13, "in", "hr")]

for query in queries:
    result = answer_query(query, facts)
    if result is None:
        print(f"{query[0]} {query[1]} = not convertible!")
    else:
        print(f"{query[0]} {query[1]} = {result:.3f} {query[2]}")
