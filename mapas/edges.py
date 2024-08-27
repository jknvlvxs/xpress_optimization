import pickle

def parse_cenario(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    edges = []
    ref_found = False
    transport_found = False

    for line in lines:
        line = line.strip()

        if "Refinarias instaladas:" in line:
            ref_found = True
            transport_found = False
            continue

        if "Quantidades transportadas dos subprodutos:" in line:
            ref_found = False
            transport_found = True
            continue

        if ref_found and line:
            if "-" in line:
                ref_found = False
            if ":" in line:
                cidade, valor = line.split(":")
                cidade = cidade.strip()
                valor = (valor.strip())
                edges.append({"CIDADE A": "Macaé", "CIDADE B": cidade, "VALOR": valor, "ITEM": "Petróleo"})

        if transport_found and line:
            if "---" in line:
                transport_found = False
            if ":" in line:
                parts = line.split(":")
                if "-->" in parts[1]:
                    cidade_a, cidade_b = parts[1].split("-->")
                    cidade_a = cidade_a.strip()
                    cidade_b = cidade_b.strip()
                    item = parts[2].strip()
                    valor = (parts[3].strip())
                    edges.append({"CIDADE A": cidade_a, "CIDADE B": cidade_b, "VALOR": valor, "ITEM": item})
    return edges


def save_edges_to_pkl(edges, output_file):
    with open(output_file, 'wb') as file:
        pickle.dump(edges, file)
        
def save_edges_to_txt(edges, output_file):
    with open(output_file, 'w') as file:
        for edge in edges:
            file.write(f"{edge['CIDADE A']} {edge['CIDADE B']} {edge['VALOR']} {edge['ITEM']}\n")


# Exemplo de uso
for i in range(1, 7):
    edges = parse_cenario(f'cenario_{i}/output.txt')
    save_edges_to_txt(edges, f'mapas/dados/arestas/edges_{i}.txt')
    save_edges_to_pkl(edges, f'mapas/dados/arestas/edges_{i}.pkl')