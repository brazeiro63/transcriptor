# Importar bibliotecas necessárias
import os
from textwrap import dedent

from crewai import Agent, Crew, Task
from crewai_tools import (
    FileReadTool,
)
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração das chaves de API (substitua com suas chaves reais)
openai_api_key = os.getenv('OPENAI_API_KEY')
# groq_api_key = os.getenv('GROQ_API_KEY')

# gpt3_llm = ChatOpenAI(model='gpt-3.5-turbo', api_key=openai_api_key)
gpt4o_llm = ChatOpenAI(model='gpt-4o', api_key=openai_api_key)
file_tool = FileReadTool('transcritos/Bispo_Bruno_Leonardo_20240622_txt')

# Definição dos agentes:

editor = Agent(
    role='Senior Editor',
    goal='Editing  and transform a video transcript into a text suitable '
    'for a less educated, believing and God-fearing audience.',
    backstory=(
        'Driven by sensibility, empaty and care of others, you are '
        'responsible for create inspirational texts to blog posts, '
        'based on the row text received in the input file.'
    ),
    verbose=True,
    memory=True,
    tools=[file_tool],
    llm=gpt4o_llm,
    allow_delegation=False,
)

# Definição de tarefas

edit_task = Task(
    description=dedent("""
    1.  Analyze the content of the text {input_text} and identify
        the subject covered, the intention and the target audience;
    2.  Rewrite the text with different form, organization and styles
        from the original, using simple, direct and more emotional language,
        aimed at an audience with a lower level of education.
    3.  Remova referências ao WhatsApp e a números de telefone, em
        vez disso refira-se aos comentários.
    4.  Remove redundancies and long-winded content so that the
        narration of the text does not take more than 3 minutes.
    """),
    expected_output=dedent("""
    A text with an engaging, eloquent and sensitive style,
    with no date or time references, aimed at people with less education,
    in Brazilian Portuguese (pt-BR), structured like a letter, not signed,
    showing:
    \n\nAssunto: [subject] \n\nIntenção:[Intention]
    \n\nPúblico: [target_audience] \n\n[letter text]
    """),
    agent=editor,
    output_file='output-files/letter.md',
    verbose=2,
)

crew1 = Crew(agents=[editor], tasks=[edit_task], verbose=2, memory=False)

# Função para ler o conteúdo de um arquivo


def read_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Executar a tarefa com a entrada do arquivo


def execute_task(file_path):
    read_file_content(file_path)
    crew1.kickoff()

    # Salvar o resultado da style_task em um arquivo


# Exemplo de uso: substitua 'caminho/para/o/arquivo.txt'
# pelo caminho real do arquivo de entrada
execute_task('transcritos/Bispo_Bruno_Leonardo_20240622_txt')
