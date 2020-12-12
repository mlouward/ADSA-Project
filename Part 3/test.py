import numpy as np
I = float('inf')
# graph = np.array([[0,8,3,5,100],[8,0,2,100,5],[100,1,0,3,4],[6,100,150,0,7],[100,5,100,100,0]])
# graph = np.array([[0,2,100,3,100,100,100],[100,0,7,100,1,100,100],[100,100,0,100,100,2,100],[100,1,100,0,100,100,100],[100,100,7,100,0,100,4],[100,100,100,100,4,0,2],[1,100,100,1,100,100,0]])
graph = np.array([[0, 2, I, 11], [2, 0, 5, 20], [I, 5, 0, 3], [11, 20, 3 , 0]])


# print("Adjacency matrix")
print(graph)
v = len(graph)

# path reconstruction matrix
p = np.zeros(graph.shape)
for i in range(0,v):
    for j in range(0,v):
        p[i,j] = graph[i,j]
print(p)

for k in range(0, v):
    for i in range(0, v):
        for j in range(0, v // 2):
            p[i, j] = min(p[i, j], p[i, k] + p[k, j])
            p[j, i] = p[i, j]

print(p)