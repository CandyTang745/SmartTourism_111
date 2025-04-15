import spacy
from pymongo import MongoClient
from rdflib import Graph, URIRef, Namespace
from pyvis.network import Network

# ========== 1. 初始化 ==========

# 加载中文 NLP 模型
nlp = spacy.load("zh_core_web_trf")

# 连接 MongoDB

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["tourism_db"]
collection = db["scenic_spots"]

# RDF 命名空间
SCENIC = Namespace("http://example.org/scenic/")

# ========== 2. 信息抽取 ==========

def extract_knowledge(text, place_name="未知"):
    doc = nlp(text)
    triples = []

    # 简单关系规则
    if "位于" in text:
        idx = text.find("位于")
        loc = text[idx+2: idx+15]
        triples.append((place_name, "位于", loc.strip("，。 ")))

    if "开放时间" in text:
        idx = text.find("开放时间")
        time_info = text[idx: idx+20]
        triples.append((place_name, "开放时间", time_info.strip("，。 ")))

    if "门票" in text:
        idx = text.find("门票")
        ticket_info = text[idx: idx+20]
        triples.append((place_name, "门票信息", ticket_info.strip("，。 ")))

    if "包括" in text:
        idx = text.find("包括")
        content = text[idx+2: idx+25]
        parts = content.strip("，。 ").split("、")
        for p in parts:
            if p.strip():
                triples.append((place_name, "包含", p.strip()))

    # 抽取实体（如人名、地名）
    for ent in doc.ents:
        if ent.label_ == "LOC":
            triples.append((place_name, "相关地点", ent.text))

    return triples

# ========== 3. 图谱构建 ==========

def build_graph(triples):
    g = Graph()
    for subj, pred, obj in triples:
        s = URIRef(SCENIC + subj)
        p = URIRef(SCENIC + pred)
        o = URIRef(SCENIC + obj)
        g.add((s, p, o))
    return g

# ========== 4. 可视化 (可选) ==========

def visualize_graph(triples, output_html="scenic_kg.html"):
    net = Network(height="800px", width="100%", directed=True)
    for s, p, o in triples:
        net.add_node(s, label=s)
        net.add_node(o, label=o)
        net.add_edge(s, o, label=p)
    net.show(output_html)

# ========== 5. 主流程 ==========

def main():
    all_triples = []
    i = 1
    for doc in collection.find():

        print(i)
        i += 1
        name = doc.get("name")
        desc = doc.get("introduction")
        if name and desc:
            triples = extract_knowledge(desc, name)
            all_triples.extend(triples)

    print(f"共抽取三元组数量: {len(all_triples)}")

    # 构建 RDF 图谱
    g = build_graph(all_triples)
    g.serialize("scenic_graph.ttl", format="turtle")
    print("知识图谱已保存为 scenic_graph.ttl")

    # 可视化
    visualize_graph(all_triples)
    print("图谱可视化已保存为 scenic_kg.html")

if __name__ == "__main__":
    main()
