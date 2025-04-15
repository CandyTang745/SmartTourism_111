from rdflib import Graph
from pyvis.network import Network

def visualize_ttl(ttl_path="scenic_graph_fixed.ttl", output_html="scenic_kg.html"):
    # 1. 加载图谱
    g = Graph()
    g.parse(ttl_path, format="turtle")

    # 2. 创建 Pyvis 网络图
    net = Network(height="800px", width="100%", directed=True)
    net.force_atlas_2based()  # 自动布局效果更好

    for subj, pred, obj in g:
        s = subj.split("/")[-1]
        o = obj.split("/")[-1]
        p = pred.split("/")[-1]

        net.add_node(s, label=s)
        net.add_node(o, label=o)
        net.add_edge(s, o, label=p)

    # 3. 生成 HTML
    # net.show(output_html)
    html = net.generate_html()
    with open("scenic_kg.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"可视化图已生成：{output_html}")

if __name__ == "__main__":
    visualize_ttl()
