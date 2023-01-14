class Stack:
    def __init__(self, content=()):
        self.stack: list[int] = list(content)

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def __repr__(self):
        return f"<Stack - {self.stack}>"


def hanoi(begin: Stack, temp: Stack, end: Stack, n: int) -> None:
    if n == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, end, temp, n - 1)
        hanoi(begin, temp, end, 1)
        hanoi(temp, begin, end, n - 1)


def my_hanoi(begin: Stack, temp: Stack, end: Stack, n: int) -> None:
    ########### RESEARCH
    """
    if n == 1:
        end.push(begin.pop())  # unterstes auf ende gebracht

    if n == 2:
        temp.push(begin.pop())
        end.push(begin.pop())  # unterstes auf ende gebracht
        my_hanoi(temp, begin, end, n - 1)

        # n = 1 und dass beginn und temp ausgetauscht sind
        # end.push(temp.pop())
    
    if n == 3:     
        end.push(begin.pop())
        temp.push(begin.pop())
        temp.push(end.pop())
        end.push(begin.pop())  # unterstes auf Ende gebracht
        my_hanoi(temp, begin, end, n - 1)
        # n = 2 nur dass begin und temp ausgetauscht sind
    
        # begin.push(temp.pop())
        # end.push(temp.pop())
        # # n = 1
        # end.push(begin.pop())

    if n == 4:
        ######
        temp.push(begin.pop())
        end.push(begin.pop())
        end.push(temp.pop())
        temp.push(begin.pop())
        begin.push(end.pop())
        temp.push(end.pop())
        temp.push(begin.pop())
        end.push(begin.pop())  # unterstes auf Ende gebracht
        ####### Lösung für n = 3 nur dass temp und end vertauscht sind
        my_hanoi(temp, begin, end, n - 1)
        # n = 3 nur dass begin und temp ausgetauscht sind

        # end.push(temp.pop())
        # begin.push(temp.pop())
        # begin.push(end.pop())
        # end.push(temp.pop())  # unterstes auf Ende gebracht
        # # n = 2 nur dass begin und temp ausgetauscht sind
        # temp.push(begin.pop())
        # end.push(begin.pop())
        # # n = 1
        # end.push(temp.pop())

    if n == 5:
        #####
        end.push(begin.pop())
        temp.push(begin.pop())
        temp.push(end.pop())
        end.push(begin.pop())
        begin.push(temp.pop())
        end.push(temp.pop())
        end.push(begin.pop())
        ##### n = 3 nur dass end und temp ausgetauscht sind
    """
    ##### result
    if n == 1:
        end.push(begin.pop())
        return 

    my_hanoi(begin, end, temp, n - 1)
    end.push(begin.pop())  # würde zum oberen dazugehören, wenn es temp und end für jedes n tauschen würde
    my_hanoi(temp, begin, end, n - 1)



if __name__ == "__main__":
    for test in range(1, 10000):
        tower1 = Stack()
        tower2 = Stack()
        tower3 = Stack()
        num_discs = test
        for i in range(1, num_discs + 1):
            tower1.push(i)

        my_hanoi(tower1, tower2, tower3, num_discs)
        print(tower1)
        print(tower2)
        print(tower3)



