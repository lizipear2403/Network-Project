# 测试脚本
# 引入NetworkX库来做对比以验证算法正确性
# 步骤：生成随机图 -> 在随机图中随机选取两点来求之间的所有路径
# 使用NetworkX库和本算法进行两边计算，来进行测试
import networkx
import graph 
import findpath
import random



i = 0 
# 创建一个在TestFiles/下的文件 命名随循环变量递增，格式Test-i


# 测试脚本无法足够充分的测试图, 原因是无法生成具有足够路径复杂度的图



while i < 1000: 
    # 生成一个1-10000的随机数 k 
    
    g_local = graph.Graph() # 有向无权图
    g_nx = networkx.DiGraph()
    max = random.randint(1,10000) 

    s_1 = random.randint(1,max) 
    e_1 = random.randint(1,max) 

    for count  in range(1, max):

        g_nx.add_edge(s_1,e_1) 
        g_local.add_edge((s_1,e_1))

        s = random.randint(1,max) 
        e = random.randint(1,max) 
        g_nx.add_edge(s,e) 
        g_local.add_edge((s,e))
    
    path_l = findpath.find_with_preprocess( g_local, s_1, e_1) 
    path_n = list( networkx.all_simple_paths(g_nx , source= s_1 , target= e_1))
    path_l.sort()
    path_n.sort()

    if ( len(path_n) >= 5) : 
        print(path_l)
        print(path_n)

    assert(path_l == path_n)
    i = i + 1  



    # gen_edge -> (a,b) -> 
