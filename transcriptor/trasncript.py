import argparse
import os
import textwrap
from datetime import datetime

from deep_translator import GoogleTranslator
from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import NoTranscriptFound


def split_text(text, max_length):
    """Divide o texto em partes menores com no máximo max_length caracteres"""
    parts = []
    while len(text) > max_length:
        split_point = text.rfind(' ', 0, max_length)
        if split_point == -1:
            split_point = max_length
        parts.append(text[:split_point])
        text = text[split_point:].strip()
    parts.append(text)
    return parts


def format_text_for_a4(text, width=79):
    """Formata o texto para se ajustar a uma largura adequada para papel A4"""
    wrapper = textwrap.TextWrapper(width=width)
    word_list = wrapper.wrap(text=text)
    formatted_text = '\n'.join(word_list)
    return formatted_text


def translate_text(text, source_lang, target_lang):
    """Traduz o texto de source_lang para target_lang"""
    parts = split_text(text, 4999)
    translated_text = ''
    for part in parts:
        translated_part = GoogleTranslator(
            source=source_lang, target=target_lang
        ).translate(part)
        translated_text += translated_part + '\n'
    return translated_text


def save_transcription(author, info):
    """Salva a transcrição em um arquivo na pasta 'transcritos' com um '
    'nome baseado no canal e na data atual"""
    if not os.path.exists('transcritos'):
        os.makedirs('transcritos')

    # Obtém a data atual no formato YYYYMMDD
    current_date = datetime.now().strftime('%Y%m%d')
    # Cria um nome de arquivo baseado no nome do autor (canal) e na data atual
    filename = (
        f'transcritos/{author}_{current_date}.txt'.replace(' ', '_')
        .replace('.', '_')
        .replace('-', '_')
    )

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(info)

    return filename


def format_video_info(
    author, title, length, transcript, original_language, target_language
):
    """Formata as informações do vídeo e a transcrição"""
    original_formatted = format_text_for_a4(transcript)
    if original_language != target_language:
        translated_text = translate_text(
            transcript, original_language, target_language
        )
        translated_formatted = format_text_for_a4(translated_text)
        info = (
            f'Vídeo encontrado de {author} com duração de {length} '
            f'segundos.\n\n'
            f'Título: {title}\n\n'
            f'Transcrição ({original_language}):\n{original_formatted}\n\n'
            f'Transcrição ({target_language}):\n{translated_formatted}'
        )
    else:
        info = (
            f'Vídeo encontrado de {author} com duração de {length} '
            f'segundos.\n\n'
            f'Título: {title}\n\n'
            f'Transcrição ({original_language}):\n{original_formatted}'
        )

    return info


def load_youtube_video_info(url, original_language, target_language):
    """Carrega informações do vídeo do YouTube e a transcrição"""
    loader = YoutubeLoader.from_youtube_url(
        url, add_video_info=True, language=original_language
    )

    try:
        result = loader.load()
        if not result:
            return 'Nenhum resultado encontrado.', None

        author = result[0].metadata['author']
        title = result[0].metadata['title']
        length = result[0].metadata['length']
        transcript = (
            result[0].page_content
            if hasattr(result[0], 'page_content')
            else 'Transcrição não disponível.'
        )

        if transcript == 'Transcrição não disponível.':
            return 'Transcrição não disponível.', None

        info = format_video_info(
            author,
            title,
            length,
            transcript,
            original_language,
            target_language,
        )
        filename = save_transcription(author, info)

        return info, filename
    except NoTranscriptFound:
        return 'Transcrição não encontrada para este vídeo.', None
    except Exception as e:
        return f'Ocorreu um erro: {e}', None


def main():
    """Função principal para processar a transcrição do vídeo"""
    parser = argparse.ArgumentParser(
        description='Processar a transcrição de um vídeo do YouTube.'
    )
    parser.add_argument('url', type=str, help='URL do vídeo do YouTube')
    parser.add_argument(
        'original_language',
        type=str,
        choices=['pt', 'en'],
        help='Idioma original do vídeo (pt para português, en para inglês)',
    )
    parser.add_argument(
        'target_language', type=str, help='Idioma alvo para a transcrição'
    )

    args = parser.parse_args()

    info, filename = load_youtube_video_info(
        args.url, args.original_language, args.target_language
    )
    print(info)

    if filename:
        print(f'Transcrição salva em: {filename}')


if __name__ == '__main__':
    main()
