import graph

e = {
        1 : {2},
        2 : {3} ,
        3 : {4, 5} ,
        }

def pre_process(g : graph.Graph ,  start , end) -> graph.Graph :
    # start / end 不在图中，无法剪枝，直接崩溃
    for node in (start, end):
        if node not in g.__nodes__:
            raise ValueError(f"节点 {node} 不在图中")

    # 先从start进行BFS，将访问到的所有节点加入res
    # 得到from_start

    def neighbors(node) -> set:
        # from_node / to_node 在加权图下返回 (节点, 权) 二元组，剪枝只关心节点本身
        ns = g.from_node(node)
        return {n[0] if isinstance(n, tuple) else n for n in ns}

    def predecessors(node) -> set:
        ns = g.to_node(node)
        return {n[0] if isinstance(n, tuple) else n for n in ns}

    # 正向BFS：start 能到达的所有节点（含 start 自身）
    from_start = {start}
    queue = [start]
    while queue:
        cur = queue.pop(0)
        for nxt in neighbors(cur):
            if nxt not in from_start:
                from_start.add(nxt)
                queue.append(nxt)

    #  从end开始在from_start中反向bfs，在res中再次剪枝， 只保留能到达end的
    # 得到to_end 这时to_end已经是交集
    # end 不在 from_start 中则交集为空
    to_end = {end} if end in from_start else set()
    queue = [end]
    while queue:
        cur = queue.pop(0)
        for prev in predecessors(cur):
            if prev in from_start and prev not in to_end:
                to_end.add(prev)
                queue.append(prev)

    # 得到节点集合
    # 从节点集合重建g中的边，也就是从g复制并且删除交集之外的节点
    # 返回res
    # 保留 g 的 directed / weighted 属性，权重一并复制
    nodes = set(g.__nodes__)
    edges = {start_: set(ends) for start_, ends in g.__edges__.items()}
    weights = dict(g.__weights__) if g.__weighted__ else None
    res = graph.Graph(nodes = nodes, edges = edges,
                  directed = g.__directed__,
                  weights = weights, weighted = g.__weighted__)

    # 交集之外的节点全部删掉；若 start 到不了 end，这里会删空，返回空图
    for node in list(res.__nodes__):
        if node not in to_end:
            res.delete_node(node)

    return res
    

#
# g = graph.Graph() 
# g.add_node(1)
# g.add_edge((1,2))
# print(g) 
