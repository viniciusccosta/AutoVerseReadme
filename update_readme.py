import json

from random       import choice
from urllib.parse import urlencode

# =====================================================================
EMOJIS_TIPO = {
    'Música'   : '🎵',
    'Livro'    : '📖',
    'Versículo': '✝️',
}

# =====================================================================
def ler_versos_do_arquivo_json():
    with open('./versos.json', 'r', encoding="utf-8") as versos_file:
        versos = json.load(versos_file)
    return versos

def escolher_verso_randomico(versos):
    verso  = choice(versos)
    return verso

def montar_url_readmetypingsvg(verso):
    SEPARATOR = ';;'
    BASE_URL  = 'https://readme-typing-svg.demolab.com/'
    
    args = {
        "font"     : "Fira Code",
        "height"   : 500,
        "width"    : 1000,
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
        # TODO: Remover todo SEPARATOR do texto original para não confundir com o separador
        args['lines'].append( linha )
    
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

def montar_texto(url):
    linhas = [
        '# AutoVerseReadme\n',
        f'[![Typing SVG]({url})](https://git.io/typing-svg)\n',
    ]
    
    texto = '\n'.join(linhas)
    
    return texto

def escrever_readme(texto):
    with open("./README.md", "w") as readme_file:
        readme_file.write(texto)
        
def main():
    versos = ler_versos_do_arquivo_json()
    verso  = choice(versos)
    url    = montar_url_readmetypingsvg(verso)
    texto  = montar_texto(url)
    
    escrever_readme(texto)

# =====================================================================
if __name__ == "__main__":
    main()