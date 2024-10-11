import re
import json

def extract_tables(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex para encontrar as tabelas
    tables = re.findall(r'### Tabela \d+\n\n\|.*?\|', content, re.DOTALL)

    extracted_tables = []

    for index, table in enumerate(tables, start=1):
        # Extrair título da tabela
        title_match = re.search(r'### Tabela \d+\n\n', table)
        title = f"TABELA {index}" if title_match is None else title_match.group(0).strip()

        # Extrair linhas da tabela
        rows = table.split('\n')[2:]  # Ignorar as duas primeiras linhas (cabeçalho)
        rows = [row for row in rows if row.strip()]  # Remover linhas vazias

        # Inicializar variáveis
        produtos = []
        svas = []
        total = None

        for row in rows:
            # Extrair valores da linha
            values = re.findall(r'\|([^|]*)\|', row)
            values = [v.strip() for v in values if v.strip()]  # Remover espaços

            if len(values) > 0:
                # Identificar se a linha contém PRODUTO ou SVA
                if "PRODUTO" in values[0].upper():
                    produtos.append(float(values[1]))
                elif "SVA" in values[0].upper():
                    svas.append(float(values[1]))
                elif "TOTAL" in values[0].upper():
                    total = float(values[1])

        # Adicionar dados extraídos à lista
        extracted_tables.append({
            "Tabela": index,
            "Conteúdo": {
                "Título": title,
                "Produto": produtos,
                "SVA": svas,
                "Total": total
            }
        })

    return {"Tabelas": extracted_tables}

# Chamar a função com o caminho do arquivo
output = extract_tables('markdown_tables9.md')

# Salvar a saída em um arquivo JSON
with open('extracted_tables_output.json', 'w', encoding='utf-8') as json_file:
    json.dump(output, json_file, ensure_ascii=False, indent=4)

print("Extração concluída e salva em 'extracted_tables_output.json'.")