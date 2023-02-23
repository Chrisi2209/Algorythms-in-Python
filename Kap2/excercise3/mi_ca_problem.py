from __future__ import annotations
from typing import List, Callable, Optional

import sys
sys.path.append('C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\kap2\\')

from generic_search import Node, PriorityQueue, Queue

START_MISSIONARIES = 100
START_CANNIBALS = 80

class MCState:
    def __init__(self, mw: int, cw: int, boatw: bool):
        self.mw = mw
        self.cw = cw

        self.me = START_MISSIONARIES - mw
        self.ce = START_CANNIBALS - cw

        self.boatw = boatw

    def __repr__(self):
        return f"mw = {self.mw}, cw = {self.cw}    me = {self.me}, ce = {self.ce}    boatw = {self.boatw}"
    
    __str__ = __repr__
    
    def goal_test(self):
        if self.me == START_MISSIONARIES and self.ce == START_CANNIBALS:
            return True

        return False

    def successors(self: MCState) -> List[MCState]:
        succ = []
        if self.boatw:
            if self.mw > 0:
                succ.append(MCState(self.mw - 1, self.cw, False))
            if self.mw > 1:
                succ.append(MCState(self.mw - 2, self.cw, False))
            if self.cw > 0:
                succ.append(MCState(self.mw, self.cw - 1, False))
            if self.cw > 1:
                succ.append(MCState(self.mw, self.cw - 2, False))
            if self.mw > 0 and self.cw > 0:
                succ.append(MCState(self.mw - 1, self.cw - 1, False))
                
        else:
            if self.me > 0:
                succ.append(MCState(self.mw + 1, self.cw, True))
            if self.me > 1:
                succ.append(MCState(self.mw + 2, self.cw, True))
            if self.ce > 0:
                succ.append(MCState(self.mw, self.cw + 1, True))
            if self.ce > 1:
                succ.append(MCState(self.mw, self.cw + 2, True))
            if self.me > 0 and self.ce > 0:
                succ.append(MCState(self.mw + 1, self.cw + 1, True))

        return [state for state in succ if state.is_legal()]

    def is_legal(self):
        if 0 < self.me < self.ce or 0 < self.mw < self.cw:
            return False
        return True
    
    def heuristic(self):
        return self.ce + self.me
    
    def __eq__(self, other: MCState):
        if self.me == other.me and self.mw == other.mw and self.ce == other.ce and self.cw == other.cw and self.boatw == other.boatw:
            return True
        
        return False
    
    def __hash__(self):
        return hash((self.mw, self.cw, self.me, self.ce, self.boatw))


def bfs(successors: Callable, goal_test: Callable, initial: MCState) -> Optional[MCState]:
    explored: set = {initial}
    frontier: Queue = Queue()

    frontier.push(Node(initial, None))

    while not frontier.empty:
        current_state: Node = frontier.pop()
        print(current_state.state)

        if goal_test(current_state.state):
            return current_state

        childs: list[MCState] = successors(current_state.state)

        for child in childs:
            if child not in explored:
                child_node = Node(child, current_state)
                explored.add(child_node)
                frontier.push(child_node)

def astar(successors: Callable, goal_test: Callable, initial: Node, heuristic: Callable) -> Optional[Node]:
    explored: set = {initial}
    frontier: PriorityQueue = PriorityQueue()

    frontier.push(Node(initial, None, 0, heuristic(initial)))

    while not frontier.empty:
        print("\n", frontier, "\n")
        current_node: Node = frontier.pop()

        if goal_test(current_node.state):
            return current_node
        
        childs: list = successors(current_node.state)
        print("node: ", str(current_node.state))
        print(f"childs: {childs}")
        for child in childs:
            if child not in explored:
                explored.add(child)
                frontier.push(Node(child, current_node, current_node.cost + 1, heuristic(child)))

    return None

def trace_back_mc(end_state: Node) -> List[MCState]:
    curr_state: Node = end_state
    traceback: list = []
    while curr_state.parent is not None:
        traceback.append(curr_state.state)
        curr_state = curr_state.parent

    return traceback[::-1]

def mc_traceback_tostring(traceback: List[MCState]) -> str:
    return "\n".join([str(state) for state in traceback])


if __name__ == "__main__":
    start = MCState(START_MISSIONARIES, START_CANNIBALS, True)
    end = astar(MCState.successors, MCState.goal_test, start, MCState.heuristic)
    if end == None:
        print("no solution found.")
    else:
        traceback: list[Node] = trace_back_mc(end)
        print(mc_traceback_tostring(traceback))

