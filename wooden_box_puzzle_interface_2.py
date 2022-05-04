import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque

def near(i):
    return set([(i[0]-1,i[1]), (i[0]+1,i[1]), (i[0],i[1]-1), (i[0],i[1]+1)])

def other_side(j, i):
    return (2*i[0]-j[0],2*i[1]-j[1])

class woodenBoxMap:
    def __init__(self, box, s):
        self.box = box
        self._visited = set()
        self.dfs(s)
        self.available = self._visited
    def dfs(self, s):
        self._visited.add(s)
        next = graph0[s] - self.box
        if next:
            for i in next - self._visited:
                self.dfs(i)
        return
    def next(self):
        _next = deque([])
        for i in self.box:
            for j in near(i)&self.available:
                k = other_side(j, i)
                if k in (back - self.box - not_good):
                    _next.append(woodenBoxMap(self.box^{k, i}, i))
        return _next
    def __eq__(self, other):
        return self.box == other.box and self.available == other.available
    def __repr__(self):
        return repr(self.box)
    def __hash__(self):
        li = list(map(lambda x:tuple(sorted(list(x))),(self.box,self.available)))
        return (li[0]+('!',)+li[1]).__hash__()

# 맵 x길이: M, y길이: N
M, N = map(int, input().split())

plt.xlim(0, M)
plt.ylim(0, N)
plt.grid()
wall, box, button, not_good = [[] for _ in range(4)]
def get_click(event):
    if event.button == 1:
        x = int(event.xdata)
        y = int(event.ydata)
        if x in range(0, M) and y in range(0, N):
            if (x, y) in not_good:
                not_good.remove((x, y))
                white = patches.Rectangle(
                (x, y),
                1, 1,
                facecolor = 'white',
                fill = True,
                )
                plt.gca().add_patch(white)
            elif (x, y) in button:
                button.remove((x, y))
                not_good.append((x, y))
                orange = patches.Rectangle(
                (x, y),
                1, 1,
                facecolor = 'orange',
                fill = True,
                )
                plt.gca().add_patch(orange)
            elif (x, y) in box:
                box.remove((x, y))
                button.append((x, y))
                blue = patches.Rectangle(
                (x, y),
                1, 1,
                facecolor = 'blue',
                fill = True,
                )
                plt.gca().add_patch(blue)
            elif (x, y) in wall:
                wall.remove((x, y))
                box.append((x, y))
                yellow = patches.Rectangle(
                (x, y),
                1, 1,
                facecolor = 'yellow',
                fill = True,
                )
                plt.gca().add_patch(yellow)
            else:
                wall.append((x, y))
                black = patches.Rectangle(
                    (x, y),
                    1, 1,
                    facecolor = 'black',
                    fill = True,
                )
                plt.gca().add_patch(black)
            plt.show()
cid = plt.connect('button_press_event', get_click)
plt.show()

wall, box, button, not_good = map(set, [wall, box, button, not_good])

# 배경(벽이 아닌 것)
back = set()
for i in range(M):
    for j in range(N):
        pos = (i, j)
        if pos not in wall:
            back.add(pos)

def graphize(back):
    graph = {}
    for i in back:
        a = set()
        for p in near(i):
            if p in back:
                a.add(p)
        graph[i] = a
    return graph

graph0 = graphize(back)

start = tuple(list(map(int, input().split())))
end = tuple(list(map(int, input().split())))

import time
t = time.time()

strt = woodenBoxMap(box, start)
fin = woodenBoxMap(button, end)

visited = deque([strt])
que = deque([strt])
predecessor = {}
while que:
    p = que.popleft()
    for i in p.next():
        if i not in visited:
            predecessor[i] = p
            visited.append(i)
            que.append(i)
    if fin in que:
        break

a = fin
r = deque()
while a != strt:
    r.appendleft(a)
    a = predecessor[a]
r.appendleft(strt)

def changed(s1, s2):
    return list(s1 - s2)[0], list(s2 - s1)[0]

s = r.popleft()
for i in r:
    print('{} -> {}'.format(*changed(s.box, i.box)))
    s = i

print(time.time() - t)
