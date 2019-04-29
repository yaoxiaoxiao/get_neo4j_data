from help import *

#获取结点的数据信息
def load_data_of_node(graph, data,nodes_list):#参数说明： graph，为了从图数据库取数据，
    single_data={}
    relationships=[{"Type":"Berthed","nodes":[]},{"Type":"Flag_is","nodes":[]},{"Type":"Trade","nodes":[]},{"Type":"belong","nodes":[]},
            {"Type":"build","nodes":[]},{"Type":"location","nodes":[]},{"Type":"manage","nodes":[]},{"Type":"own","nodes":[]}]
    re=[]
    id_of_nodes=data.identity
    type_of_data=str(data.labels)
    #计算出入度(权重值)
    record = list(graph.run("MATCH (p"+str(type_of_data)+") WHERE id(p)="+ str(id_of_nodes)+ " RETURN size((p)<--()) AS in_degree,size((p)-->()) AS out_degree"))

    value = load_value(record[0][0],record[0][1])
    single_data["id"]=id_of_nodes # 结点id
    single_data["name"]=load_name_of_data(data)#结点名字
    single_data["category"]=str(data.labels)[1:]#结点类别
    single_data["value"]=value# 结点出入度
    #结点照片路径
    single_data["image"]="./image/"+str(data.labels)[1:]+"/"+load_image_index_of_node(data)+'.jpg'
    single_data["properties"]=dict(data)#结点属性
    del single_data["properties"]["Name"]#删除结点属性中的Name
    single_data["relationship"]=re
#====================================================================
    relation_list=list(graph.run("MATCH (p"+str(type_of_data)+")-[r*..1]-() WHERE id(p)="+ str(id_of_nodes)+ " RETURN r"))
    for relation in relation_list:
        b=relation[0]
        #print(b)
        for c in b:
            set2=load_type_of_link(c)
            relationships.append(relationship_of_node(graph,data,set2,relationships))

    for x in relationships:
        if x not in re:
            re.append(x)
    a=len(relationships)
    for i in re[0:8]:
        for j in re[8:a+1]:
            if i["Type"]==j["Type"]:
                b=re.index(i)
                del re[b]

    if single_data not in nodes_list:
        nodes_list.append(single_data)


def load_data_of_links(links,source,destination,links_list):
    single_link_data={}
    relationship=[]
    single_link_data["id"]=links.identity
    single_link_data["type"]=load_type_of_link(links)
    single_link_data["properties"]=dict(links)
    single_link_data["source"]=str(source.identity)
    single_link_data["target"]=str(destination.identity)
    single_link_data["relationship"]=relationship
    relationship.append(simple_data_of_node(source))
    relationship.append(simple_data_of_node(destination))
    if single_link_data not in links_list:
        links_list.append(single_link_data)
        #return single_link_data

#获取全部数据
def requir_record_data(graph,records_data,nodes_list,links_list):
    for record  in records_data:
        source = record[0]
        destination=record[2]
        relationship_list=record[1]
        load_data_of_node(graph,source,nodes_list)
        load_data_of_node(graph,destination,nodes_list)
        for relationship in relationship_list:
            #print(relationship)
            load_data_of_links(relationship,source,destination,links_list)