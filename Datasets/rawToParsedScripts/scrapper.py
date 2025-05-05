import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

data = []
class_keywords = ['legislacao_LegislationPage-article', 'body-text_root']
tags = ['article', 'div']

options = Options()
# options.add_argument('--headless')  # Rodar sem abrir janela
# options.add_argument('--disable-gpu')  # Opcional: recomendado no Windows
# options.add_argument('--window-size=1920,1080')  # Definir tamanho da janela

folder_path = 'results'
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(folder_path, file_name)

        df = pd.read_csv(file_path)
        question_id = 0

        for _, row in df.iterrows():
            question_id += 1
            print("Question: ", question_id)
            legalPrinciples = row['Princípios']
            for legalPrinciple in legalPrinciples.split(';'):
                print("Legal Principle: ", legalPrinciple)
                driver = webdriver.Chrome(options=options)
                driver.get(f'https://www.jusbrasil.com.br/busca?q={legalPrinciple}')
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                link = soup.find('a', class_="link_root__cF5pa link_typeprimary__tABe6 "
                                             "featured-snippet-header_link__cdPPG")
                driver.quit()

                if link and link.has_attr('href'):
                    print(link['href'])
                    driver = webdriver.Chrome(options=options)
                    law_url = link['href']
                    driver.get(law_url)
                    time.sleep(2)

                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    article = soup.find(tags, class_=lambda c: c and any(class_keyword in c for class_keyword in class_keywords))
                    driver.quit()

                    if article:
                        paragraphs = article.find_all('p')

                        # Lista para guardar os textos extraídos
                        formatted_text = []

                        for p in paragraphs:
                            # Se houver um <a> dentro, pega o texto do <a> + o que vem depois
                            if p.a:
                                link_text = p.a.get_text(strip=True)
                                full_text = p.get_text(strip=True)

                                # Se o texto começa com Art., Parágrafo ou § (símbolos comuns), junta bonitinho
                                if full_text.startswith(link_text):
                                    formatted_text.append(f"{link_text} {full_text[len(link_text):].strip()}")
                                else:
                                    formatted_text.append(full_text)
                            else:
                                # Caso não tenha <a>, pega o texto normal
                                formatted_text.append(p.get_text(strip=True))

                        # Agora junta os parágrafos com duas quebras de linha para separar melhor
                        output_text = '\n\n'.join(formatted_text)

                        # Exibe ou salva
                        print(output_text)
                        data.append({
                            "prova": file_name,
                            "questao": question_id,
                            "lei": legalPrinciple,
                            "conteudo_lei": output_text
                        })

results_df = pd.DataFrame(data)

results_df.to_csv('conteudo_lei.csv', index=False)