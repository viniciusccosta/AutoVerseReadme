import json
import requests

from random       import choice
from urllib.parse import urlencode
from jinja2       import Environment, FileSystemLoader

# =====================================================================
EMOJIS_TIPO = {
    'Música'   : '🎵',
    'Livro'    : '📖',
    'Versículo': '✝️',
}

# =====================================================================
def realizar_download_do_json():
    FILE_ID  = '13XoxjPstWGxQ-o-45E_zWESLdKk5iPk6'
    FILE_URL = f'https://drive.google.com/uc?id={FILE_ID}'
    
    response = requests.get(FILE_URL)
    with open('./versos.json', 'wb') as versos_file:
        versos_file.write( response.content )

def ler_versos_do_arquivo_json():
    with open('./versos.json', 'r', encoding="utf-8") as versos_file:
        versos = json.load(versos_file)
    return versos

def ler_texto_atual():
    with open('./README.md', 'r', encoding='utf-8') as readme_file:
        texto_atual = readme_file.read()
    
    return texto_atual

def escolher_verso_randomico(versos):
    verso  = choice(versos)
    return verso

def montar_url_readmetypingsvg(verso):
    SEPARATOR = ';'
    BASE_URL  = 'https://readme-typing-svg.demolab.com/'
    
    args = {
        "font"     : "Fira Code",
        "height"   : (len(verso.get('linhas', 0)) + 1) * 30,
        "width"    : 500,
        "size"     : 20,
        "pause"    : 100,
        "color"    : "A9FEF7",
        "center"   : True,
        "vCenter"  : True,
        "multiline": True,
        "duration" : 1500,
        "repeat"   : True,
        "lines"    : [],
    }
    
    # Inserindo o texto:
    for linha in verso.get("linhas"):
        linha_limpa = linha.replace(SEPARATOR, '')
        args['lines'].append( linha_limpa )
    
    # Inserindo a referência no final:
    tipo = verso.get('tipo')
    ref  = verso.get('referencia')
    args['lines'].append(f'{EMOJIS_TIPO.get(tipo)} {ref} {EMOJIS_TIPO.get(tipo)}')
    
    # Convertendo a lista para uma string:
    args['lines'] = SEPARATOR.join(args['lines'])
    
    # Gerando URL:
    enconded_args = urlencode(args)
    full_url      = f'{BASE_URL}?separator={SEPARATOR}&{enconded_args}'
    
    return full_url

def renderizar_template(url):
    env      = Environment(loader=FileSystemLoader("."))
    template = env.get_template("template.md")
    texto    = template.render(url=url)
    return texto

def escrever_readme(texto):
    with open("./README.md", "w", encoding='utf8') as readme_file:
        readme_file.write(texto)
        
def main():
    realizar_download_do_json()
    
    versos      = ler_versos_do_arquivo_json()
    texto_atual = ler_texto_atual()
    
    for _ in range(5):                                 # Evitando loop infinto e a mesma frase/texto do readme atual
        verso       = escolher_verso_randomico(versos)
        url         = montar_url_readmetypingsvg(verso)
        texto       = renderizar_template(url)
        
        if texto != texto_atual:
            break
    
    escrever_readme(texto)

# =====================================================================
if __name__ == "__main__":
    main()