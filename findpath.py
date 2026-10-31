import graph
import collections

def pre_process(g : graph.Graph ,  start , end) -> graph.Graph :
    # start / end 不在图中，无法剪枝，直接崩溃
    nodes = g.get_all_nodes()
    edges = g.get_all_edges()
    adj = edges
    # 反向Adj
    reverse_adj = {}
    for s, es in edges.items():
        for e in es:
            reverse_adj.setdefault(e, set()).add(s)
    for node in (start, end):
        if node not in nodes:
            raise ValueError(f"节点 {node} 不在图中")


    # start正向BFS 
    from_start = {start}
    nq = collections.deque([start])
    while nq:
        cur = nq.popleft()
        ngs = adj[cur]
        for nxt in ngs:
            if nxt not in from_start:
                from_start.add(nxt)
                nq.append(nxt)

    # 从end开始的反向bfs
    if  end not in from_start : 
        return graph.Graph()
    else : 
        to_end = {end} 

    nq = collections.deque([end])
    while nq :
        cur = nq.popleft()
        rng = reverse_adj.get(cur, set())
        for prev in rng:
            if ( prev in from_start ) and ( prev not in to_end ):
                to_end.add(prev)
                nq.append(prev)

    new_edges = {}
    new_weights = {}
    for s in from_start: 
        new_end : set = edges[s] & (to_end) 
        new_edges[s] = new_end

    if g.is_weighted() : 
        for (s,es) in new_edges.items() : 
            for e in es: 
                new_weights[(s,e)] = g.get_edge_weight( s,e )

    res_new = graph.Graph(
            edges= new_edges,
            weights= new_weights if g.is_weighted() else None,
            nodes= to_end,
            directed=g.is_directed(),
            weighted=g.is_weighted()
            )
    return res_new
    
def find_all_path(start,  end , g : graph.Graph) -> list[list]:
    # 传入已经预处理的图，并且找到起点和重点之间的所有路径
    # 预处理已经将所有点处理完毕， 每个点至少在一个路径上
    # 回溯dfs
    allpath = []
    nodes =g.get_all_nodes()
    if not nodes:
        return []
    if start not in nodes  or end not in nodes:
        raise ValueError(f"节点 {start if start not in nodes else end} 不在图中")

    adj = {node: g.neighbors(node) for node in nodes}

    path = [start]
    on_path = {start}

    # 栈代替递归，省掉函数调用
    stack = [iter(adj[start])]
    while stack:
        nxt = next(stack[-1], None)
        if nxt is None:
            stack.pop()
            on_path.discard(path.pop())
            continue

        if nxt in on_path:
            continue

        if nxt == end:
            allpath.append(path + [end])
            continue

        path.append(nxt)
        on_path.add(nxt)
        stack.append(iter(adj[nxt]))

    return allpath

def find_with_preprocess(g , s ,e ) : 
    ng = pre_process(g, s, e) 
    return find_all_path(s, e, ng)


