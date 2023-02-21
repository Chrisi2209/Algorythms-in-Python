from __future__ import annotations
from typing import List

import sys
sys.path.append('C:\\Programmieren\\VS_Code\\pythonAlgorithmusÜbungen\\kap2\\')

import generic_search

START_MISSIONARIES = 3
START_CANNIBALS = 3

class MCState:
    def __init__(self, mw: int, cw: int, boatw: bool):
        self.mw = mw
        self.cw = cw

        self.me = START_MISSIONARIES - mw
        self.ce = START_CANNIBALS - cw

        self.boatw = boatw

    def successors(self) -> List[MCState]:
        succ = []

        if self.boatw:
            if self.mw > 0:
                succ.append(MCState(self.mw - 1, self.cw, False))
            if self.mw > 1:
                succ.append(MCState(self.mw - 2, self.cw, False))
            if self.cw > 0:
                succ.append(MCState(self.cw - 1, self.cw, False))
            if self.cw > 1:
                succ.append(MCState(self.cw - 2, self.cw, False))
            if self.mw > 0 and self.cw > 0:
                succ.append(MCState(self.mw - 1, self.cw - 1, False))
                
        else:
            if self.me > 0:
                succ.append(MCState(self.mw + 1, self.cw, True))
            if self.me > 1:
                succ.append(MCState(self.mw + 2, self.cw, True))
            if self.ce > 0:
                succ.append(MCState(self.cw + 1, self.cw, True))
            if self.ce > 1:
                succ.append(MCState(self.cw + 2, self.cw, True))
            if self.me > 0 and self.ce > 0:
                succ.append(MCState(self.mw + 1, self.cw + 1, True))

            return succ
    
    def goal_test(self):
        if self.me == START_MISSIONARIES and self.ce == START_CANNIBALS:
            return True

        return False
