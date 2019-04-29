#获取结点名字
def load_name_of_data(node):
    if node["Name"] is not None:
        return node["Name"]
    else:
        return Exception("没有找到name")

#计算出入度
def load_value(in_degree, out_degree):
    return in_degree + out_degree
#获取结点的图片索引值
def load_image_index_of_node(node):
    if node["id"]is not None:
        return node["id"]
    elif node["Maritime_Mobile_Service_ID"] is not None:
        return node["Maritime_Mobile_Service_ID"]
    elif node["Country_Code"] is not None:
        return node["Country_Code"]
    else:
        return 0

# 获取结点的简单信息
def simple_data_of_node(data):#source_id
    single_data={}
    id_of_nodes=data.identity
    #type_of_data =str(data.labels)
    single_data["id"]=id_of_nodes
    single_data["image"]="./image/"+str(data.labels)[1:]+"/"+str(load_image_index_of_node(data))+'.jpg'
    single_data["name"]=load_name_of_data(data)
    return single_data
    #single_data["info"]=
#获取节点的关系结点

def relationship_of_node(graph,data,set2,relationships):
    single_data={}
    
    single_data["Type"]=(set2)
        
    single_data["nodes"]=relationship_nodes_of_node(graph,data,set2)

    if single_data not in relationships:
        relationships.append(single_data)
    return single_data

#返回结点的某类型关系的一度关系结点，返回结点个数为6个。
def relationship_nodes_of_node(graph,data,set2):
    nodes=[]
    id_of_nodes=data.identity
    type_of_data=str(data.labels)
    #type_of_link=load_type_of_link(relation)
    record_list=list(graph.run(
            "MATCH (p"+str(type_of_data)+
            ")-[r:" +str(set2)+
            "]-(m) WHERE id(p)="
            + str(id_of_nodes)+ 
            " RETURN m limit 6"))
    for record1 in record_list:
        #nodes=[]
        a=record1[0]
        #print(a)
        nodes.append(simple_data_of_node(a))
    return nodes
        



#获取边的类型

def load_type_of_link(relationship):
    relation_ship_mapping_dict_2_default = {
        "Berthed":"Berthed",
        "Flag_is":"Flag_is",
        "Trade":"Trade",
        "belong":"belong",
        "build":"build",
        "location":"location",
        "manage":"manage",
        "own":"own"
        }
    relation_ship_mapping_dict = relation_ship_mapping_dict_2_default
    query_key = str(type(relationship).__name__)
    return relation_ship_mapping_dict[query_key]
