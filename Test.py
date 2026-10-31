# 测试脚本
# 引入NetworkX库来做对比以验证算法正确性
# 步骤：生成随机图 -> 在随机图中随机选取两点来求之间的所有路径
# 使用NetworkX库和本算法进行两边计算，来进行测试
import networkx
import graph 
import findpath
import random
import time

# n = random.randint(1 , 1000)
n  = 23
c = 0 
time_l = 0 
time_n = 0 

while c < 10 : 
    p =  0.17 
    print(n , p)
    # 生成ER随机图
    g = networkx.erdos_renyi_graph(  n, p  , directed=True) 
    print()
    g_ = graph.Graph(nodes=g.nodes())
    for edge in g.edges(): 
        g_.add_edge((edge))
        # print(g_)

    s = random.choice(list(g_.get_all_nodes()))
    e = random.choice(list(g_.get_all_nodes()))


    t1 = time.time()
    l_ = sorted( findpath.find_with_preprocess( g_, s,e ))
    t2 = time.time()
    l = sorted( networkx.all_simple_paths(g, source=s , target=e)  )
    t3 = time.time()
    time_l += t2 - t1 
    time_n += t3 - t2 

    # print(f"Local usage ={t2 - t1}, networkx usage = {t3 - t2}"  )
    print( l == l_ )
    c  =  c + 1 
print(time_l/10 ,time_n/10)
