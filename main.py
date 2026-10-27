import graph as g 

e = {
        1 : {2}, 
        2 : {3} , 
        3 : {4, 5} , 
        }

def pre_process(g : g.Graph ,  start , end) -> ( 预处理之后的图 g.Graph ) : 
    res = g.Graph()
    from_start = g.Graph()
    to_end = g.Graph()
    # 先从start进行BFS，将访问到的所有节点加入res
    # 得到from_start

    #  从end开始在from_start中反向bfs，在res中再次剪枝， 只保留能到达end的
    # 得到to_end 这时to_end已经是交集

    # 得到节点集合
    # 从节点集合重建g中的边，也就是从g复制并且删除交集之外的节点
    # 返回res

    pass
    

#
# g = graph.Graph() 
# g.add_node(1)
# g.add_edge((1,2))
# print(g) 
