# 定义图对象
# 使用邻接链表

import copy

class Graph :
    # nodes : set , edges : {type of node : set(type of node)} , weights : { (s , e) : num } 
    def __init__(self, nodes = None , edges = None, directed = True, weights = None ,  weighted = False) -> None:
        self.__nodes__ = set(nodes) if nodes is not None else set()

        # self.__edges__ = {s: set(ends) for s, ends in edges.items()} if edges is not None else {}
        self.__edges__ = {} 

        if edges is not None : 
            for k,v in edges.items() : 
                self.__edges__[k] = set(v)

        self.__directed__ = directed
        if weighted :
            if weights == None :
                raise RuntimeError("weights 为空且 weighted 矛盾")
            else :
                self.__weights__ = dict(weights)
                # 现在检查是否对所有边都有权重定义，
                # 没有权重定义的默认设0
                # 仅允许在 __init__ 中补默认值
                for start, ends in self.__edges__.items():
                    for end in ends:
                        if (start, end) not in self.__weights__:
                            self.__weights__[(start, end)] = 0

        self.__weighted__ = weighted

    def undirected(self) -> None : 
        # 将图置为undirected 
        # 遍历一次edges , 创建边集合：二元组集合， 并且根据集合重建__edges__
        pair_weight = {}
        weights_src = self.__weights__ if self.__weighted__ else {}
        for start, ends in self.__edges__.items():
            for end in ends:
                # sorted 让 (u,v) 和 (v,u) 变成同一个元素
                key = tuple(sorted((start, end)))
                w = weights_src.get((start, end))

                # 同一对节点的两个方向权重必须一致，否则无向图表达不出来
                if (key in pair_weight and
                    pair_weight[key] is not None and
                    w is not None and
                    pair_weight[key] != w):
                    raise ValueError(
                        f" ( {start} , {end} ) 两个方向权重不同"
                        f"（{pair_weight[key]} vs {w}），无法转为无向图"
                    )
                # 只补空缺，不覆盖已记录的非空权重
                pair_weight[key] = w

        edges = {}
        weights = {}

        for key, w in pair_weight.items():
            u, v = tuple(key)
            edges.setdefault(u, set()).add(v)
            edges.setdefault(v, set()).add(u)
            if w is not None:
                weights[(u, v)] = w
                weights[(v, u)] = w

        self.__edges__ = edges
        # 无权视图下不动 __weights__
        if self.__weighted__:
            self.__weights__ = weights

        #最后再修改__directed__ 
        self.__directed__ = False
         
    def __str__(self) -> str:
        lines = []
        for start in sorted(set(self.__nodes__) | set(self.__edges__)):
            ends = sorted(self.__edges__.get(start, ()))
            if not ends:
                # 孤立节点没有出边，按 100 -> None 打印
                lines.append(f"{start} -> None")
                continue
            if self.__weighted__:
                items = [f"{end}({self.__weights__.get((start, end))})" for end in ends]
            else:
                items = [str(end) for end in ends]
            lines.append(f"{start} -> " + " , ".join(items))
        return "\n".join(lines)

    # 获得指向一个点的邻居集合
    def reverse_neighbors(self, node) -> set: 
        ns = self.to_node(node)
        return {n[0] if isinstance(n, tuple) else n for n in ns}

    # 获得一个点指向的邻居集合
    def neighbors(self, node) -> set :  
        ns = self.from_node(node)
        return {n[0] if isinstance(n, tuple) else n for n in ns}

    def add_node(self,node ) -> None: 
        self.__nodes__.add(node)

    def delete_node(self,node ) -> None: 
        # 删除节点 
        # 连同它在__edges__中作为起点、以及作为终点被其它节点指向的边一起清掉，
        # 否则edges里会留下悬空目标，破坏 __str__ 依赖的结构
        if node not in self.__nodes__:
            return

        # 直接pop会产生悬空权重问题
        for end in self.neighbors(node):
            self.delete_edge((node, end))
        for start in self.reverse_neighbors(node):
            self.delete_edge((start, node))

        # delete_edge 不清理空key，node 自己的空key要在这里清掉，
        # 否则 __str__ 的 nodes | edges 并集会打出一个已删除的节点
        self.__edges__.pop(node, None)
        self.__nodes__.discard(node)

    
    def delete_edge(self,edge : tuple) -> None: 
        # 删除边
        # 检查__directed__ , 同add_edge
        if len(edge) != 2:
            raise ValueError("edge 必须是二元组 (start, end)")

        def remove_weight( s , e) : 
            if self.__weighted__:
                self.__weights__.pop((s, e), None)

        start, end = edge
        self.__edges__.get(start, set()).discard(end)
        remove_weight(start,end)

        # 无向图 从终点处也要去除边
        if not self.__directed__:
            self.__edges__.get(end, set()).discard(start)
            remove_weight(end,start)

    def is_edge(self , start = None , end = None  ): 
        if start is None and end is None:
            return False
        return end in self.__edges__.get(start, ())

    def get_edge_weight(self, start , end) : 
        # 先检查是否__weighted__ 若否直接崩溃，
        if not self.__weighted__:
            raise RuntimeError("无权图没有权重信息")
        if self.is_edge(start,end) : 
            # 返回权
            return self.__weights__.get((start, end))
        else : 
            # 返回None
            return None
        

    def to_node(self, end)  -> set : 
        # 获取指向end的所有节点， end不在图中，返回None，end没有指向的节点则返回空集合
        # 有权图：返回二元组集合， 第一个元素是起点，第二个元素是权
        # 无权图：返回节点集合
        if end not in self.__nodes__:
            return None
        result = set()
        for start, ends in self.__edges__.items():
            if end not in ends:
                continue
            if self.__weighted__:
                result.add((start, self.__weights__.get((start, end))))
            else:
                result.add(start)
        return result
        
    def from_node(self, start) -> set :
        # 获取从start开始的所有节点， start不在图中，返回None，start没有指向的节点则返回空集合
        # 有权图：返回二元组集合， 第一个元素是终点，第二个元素是权
        # 无权图：返回节点集合
        if start not in self.__nodes__:
            return None
        ends = self.__edges__.get(start, set())
        if not ends:
            return set()
        if self.__weighted__:
            return {(end, self.__weights__.get((start, end))) for end in ends}
        return set(ends)

    def add_edge(self,  edge : tuple , weight = None ) -> None : 
        if self.__weighted__ and weight is None:
            raise ValueError(f"加权图不接受无权重边：{edge} 缺少 weight")
        if not self.__weighted__ and weight is not None:
            raise ValueError(
                f"无权图不接受权重：{edge} 带了 weight={weight}；"
            )

        # 传入二元组， 若二元组中有新node ， 先使用insert
        # 这时检查__directed__ ，无向 -> 双向加edge， 反之单向加edge
        if len(edge) != 2:
            raise ValueError("edge 必须是二元组 (start, end)")
        start, end = edge

        # 新节点先入库
        for node in (start, end):
            self.add_node(node)

        # 边
        self.__edges__.setdefault(start, set()).add(end)
        if not self.__directed__:
            self.__edges__.setdefault(end, set()).add(start)

        # 权：走到这里 weight 和 __weighted__ 已经保证一致，加权图必然有权
        if self.__weighted__:
            self.__weights__[(start, end)] = weight
            if not self.__directed__:
                self.__weights__[(end, start)] = weight

    # def weighted(self) -> None : 
    #     # 与unweighted 对称：只开开关，不补权重。已有边没权重的，读出来是None
    #     self.__weighted__ = True
    def unweighted(self) -> None : 
        # 将__weighted__ 置为false 但是不抹除已有的权重信息
        self.__weighted__ = False
        

