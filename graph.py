# 定义图对象
# 使用邻接链表

# 此为edges 示例
# example = {
#         1:{2,3} ,
#         2:{3,4,1} ,
#         3:{2},
#         4:{2}
#         }
#

class Graph : 
    def __init__(self,nodes = set() , edges = {}, directed = True, weights = {} ,  weighted = False) -> None:
        # 创建空
        # self.__nodes__ = if   nodes : then   nodes  else : set() 
        # self.__edges__ = if   edges : then   edges  else :  {}
        # if weights and weighted : 
        #     self.__weights__ = {}
        #     # 产生权重
        # else： 
        self.__nodes__ = nodes
        self.__edges__ = edges 
        # self,__weights__ = weights 
        #     不一致， 直接崩溃
        self.__directed__ = True
        self.__weighted__ = weighted
        # __weighted__ 应由传入时选择，且只能由有权图变为无权图的方法， 我已注释掉weighted方法
    def undirected(self) -> None : 
        # 将图置为undirected 
        # 遍历一次edges , 创建边集合：二元组集合， 并且根据集合重建__edges__
        pair_weight = {}
        # 无权视图下 __weights__ 只是留存的惰性数据：不参与转换，也不被抹除
        weights_src = self.__weights__ if self.__weighted__ else {}
        for start, ends in self.__edges__.items():
            for end in ends:
                # frozenset 让 (u,v) 和 (v,u) 折叠成同一个元素，天然去重
                key = frozenset((start, end))
                w = weights_src.get((start, end))
                # 同一对节点的两个方向权重必须一致，否则无向图表达不出来
                if (key in pair_weight and pair_weight[key] is not None
                        and w is not None and pair_weight[key] != w):
                    raise ValueError(
                        f"边 {start} <-> {end} 两个方向权重不同"
                        f"（{pair_weight[key]} vs {w}），无法转为无向图"
                    )
                # 只补空缺，不覆盖已记录的非空权重
                if pair_weight.get(key) is None:
                    pair_weight[key] = w

        edges = {}
        weights = {}
        for key, w in pair_weight.items():
            if len(key) == 2:
                u, v = tuple(key)
            else:
                # 自环，frozenset 只剩下一个元素
                u = v = next(iter(key))
            edges.setdefault(u, set()).add(v)
            edges.setdefault(v, set()).add(u)
            if w is not None:
                weights[(u, v)] = w
                weights[(v, u)] = w

        self.__edges__ = edges
        # 无权视图下不动 __weights__，保证 unweighted() 留下的权重信息不丢
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
    def add_node(self,node ) -> None: 
        # 插入一个孤立Node
        if node in self.__nodes__:
            return
        self.__nodes__.add(node)
        # self.__edges__.add((node , None))
    def delete_node(self,node ) -> None: 
        # 删除节点 
        # 连同它在__edges__中作为起点、以及作为终点被其它节点指向的边一起清掉，
        # 否则edges里会留下悬空目标，破坏 __str__ 依赖的结构
        if node not in self.__nodes__:
            return
        self.__nodes__.discard(node)
        self.__edges__.pop(node, None)
        for start in list(self.__edges__):
            self.__edges__[start].discard(node)
            if not self.__edges__[start]:
                del self.__edges__[start]
        for key in [k for k in self.__weights__ if node in k]:
            del self.__weights__[key]
    def delete_edge(self,edge) -> None: 
        # 删除边
        # 检查__directed__ , 同add_edge
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
            raise ValueError("edge 必须是二元组 (start, end)")
        start, end = edge
        self.__edges__.get(start, set()).discard(end)
        self.__weights__.pop((start, end), None)
        if not self.__directed__:
            self.__edges__.get(end, set()).discard(start)
            self.__weights__.pop((end, start), None)
        # 删空的目标集合不要留下空key
        for node in (start, end):
            if node in self.__edges__ and not self.__edges__[node]:
                del self.__edges__[node]
    def is_edge(self , start = None , end = None  ): 
        if start is None and end is None:
            return False
        return end in self.__edges__.get(start, ())
    def get_edge_weight(self, start , end) : 
        # 先检查是否__weighted__ 若否直接崩溃，
        if not self.__weighted__:
            raise RuntimeError("无权图没有权重信息；加权与否只能在创建时用 Graph(weighted=True) 指定")
        if self.is_edge(start,end) : 
            # 返回权
            return self.__weights__.get((start, end))
        else : 
            # 返回None
            return None
        

    def to_node(self, end) : 
        # 获取指向end的所有节点， end不在图中，返回None，end没有指向的节点则返回空集合
        # 有权图：返回二元组集合， 第一个元素是起点，第二个元素是权
        # 无权图：返回节点集合
        
    def from_node(self, start) :
        # 获取从start开始的所有节点， start不在图中，返回None，start没有指向的节点则返回空集合
        # 有权图：返回二元组集合， 第一个元素是终点，第二个元素是权
        # 无权图：返回节点集合

    def add_edge(self,  edge , weight = None ) -> None : 
# 必须先于任何写操作校验，崩的时候图里不能留下半条边
        if self.__weighted__ and weight is None:
            raise ValueError(f"加权图不接受无权重边：{edge} 缺少 weight")
        if not self.__weighted__ and weight is not None:
            raise ValueError(
                f"无权图不接受权重：{edge} 带了 weight={weight}；"
                f"加权与否只能在创建时用 Graph(weighted=True) 指定"
            )

        # 传入二元组， 若二元组中有新node ， 先使用insert
        # 这时检查__directed__ ，无向 -> 双向加edge， 反之单向加edge
        if not isinstance(edge, (tuple, list)) or len(edge) != 2:
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
        

# 流程一致性 -> 只能由__init__创建对象 ->
# 无权 -> add_node , delete 相关无误，-> add_edge  若传入权重直接崩溃
# 有权 -> add_node ， delete正常 -> add_edge 无权重直接报错
# 只能由有权图变为无权图， 无权图不得变为有权图 ，相关操作若实质性需要再写外部函数，不得放入类方法中

