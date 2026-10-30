import graph

def pre_process(g : graph.Graph ,  start , end) -> graph.Graph :
    # start / end 不在图中，无法剪枝，直接崩溃
    for node in (start, end):
        if node not in g.__nodes__:
            raise ValueError(f"节点 {node} 不在图中")

    # 先从start进行BFS，将访问到的所有节点加入res
    # 得到from_start

    # 正向BFS：start 能到达的所有节点（含 start 自身）
    from_start = {start}
    queue = [start]
    while queue:
        cur = queue.pop(0)
        for nxt in g.neighbors(cur):
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
        for prev in g.reverse_neighbors(cur):
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
    
def find_all_path(start,  end , g : graph.Graph) -> list[list]:
    # 传入已经预处理的图，并且找到起点和重点之间的所有路径
    # 预处理已经将所有点处理完毕， 每个点至少在一个路径上
    # 回溯dfs
    allpath = []
    # dfs from start
    # find end -> 添加一条路径
    # -> 返回上一个节点 -> 选择不同的节点进行dfs
    # -> 找到end 添加路径 -> 返回
    # 以此类推直到返回到start
    # 注意添加的路径为完整节点顺序列表
    # start 到不了 end 时 pre_process 返回空图，视为零条路径，直接返回空列表
    if not g.__nodes__:
        return []
    if start not in g.__nodes__ or end not in g.__nodes__:
        raise ValueError(f"节点 {start if start not in g.__nodes__ else end} 不在图中")

    # def neighbors(node) -> set:
    #     # from_node 在加权图下返回 (节点, 权) 二元组，找路径只关心节点本身
    #     ns = g.from_node(node)
    #     return {n[0] if isinstance(n, tuple) else n for n in ns}
    #
    path = [start]
    on_path = {start}

    def dfs(cur) :
        # 到达 end：当前栈中 path 就是一条完整节点顺序列表，拷贝存入
        if cur == end:
            allpath.append(list(path))
            return
        # 选择不同的节点进行dfs；
        # on_path 剪掉环，保证路径是简单路径
        for nxt in g.neighbors(cur):
            if nxt in on_path:
                continue
            path.append(nxt)
            on_path.add(nxt)
            dfs(nxt)
            # 回溯：返回上一个节点，撤销选择
            path.pop()
            on_path.discard(nxt)

    dfs(start)
    return allpath

def find_with_preprocess(g , s ,e ) : 
    ng = pre_process(g, s, e) 
    return find_all_path(s, e, ng)


