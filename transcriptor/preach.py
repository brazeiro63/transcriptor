# Importar bibliotecas necessárias
import os
import sys
from textwrap import dedent

from crewai import Agent, Crew, Task
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração das chaves de API (substitua com suas chaves reais)
openai_api_key = os.getenv('OPENAI_API_KEY')
# groq_api_key = os.getenv('GROQ_API_KEY')

gpt3_llm = ChatOpenAI(model='gpt-3.5-turbo', api_key=openai_api_key)
gpt4o_llm = ChatOpenAI(model='gpt-4o', api_key=openai_api_key)
# passage = 'Josué 1:9'

# Definição dos agentes:

pastor = Agent(
    role='Protestant Preacher',
    goal=(
        'Create a motivational text based on a passage from the '
        'Bible, designed to give strength, motive and purpose to the '
        'people who read it.'
    ),
    backstory=(
        'Experienced theologian, concerned with the well-being of '
        'the faithful, endowed with extreme empathy and a good heart.'
    ),
    verbose=True,
    memory=True,
    llm=gpt4o_llm,
    allow_delegation=False,
)

screenplayer = Agent(
    role='Gospel video Scrennplayer',
    goal=(
        'Create detailed and cohesive scripts for videos, guiding '
        'AI on narrative, visual descriptions and audio, ensuring an '
        'engaging and emotional experience for the audience.'
    ),
    backstory=("""
        Experienced screenwriter and video producer. He is well
        aware of YouTube's requirements for making videos go viral.
        Specialized in awakening a feeling of welcome in the public.
    """),
    verbose=True,
    memory=False,
    llm=gpt3_llm,
    allow_delegation=False,
)

# Definição de tarefas

write = Task(
    description=dedent("""
    1. Create a motivational text based on the following biblical
       passage {passage}.
    2. identify the target audience this text is intended for and
       create a persona to represent them.
    3. Do not use the same persona every time.
    4. The text must have an emotional, comforting tone, aimed at
       the identified persona and contain between 250 and 300 words.
    """),
    expected_output=dedent("""
    A text with an engaging, eloquent and sensitive style,
    with no date or time references, aimed at the persona identified,
    in Brazilian Portuguese (pt-BR), structured like a letter, not signed,
    showing:
    \n\nAssunto: [subject] \n\nIntenção:[Intention]
    \n\nPúblico: [target_audience] \n\n[letter text]
    """),
    agent=pastor,
    output_file='output-files/pregacao.md',
    verbose=2,
)


screenplay = Task(
    description=dedent("""
    Using the exact same text created by in task write, create a script for
    a YouTube video, containing prompts for generating images, and
    defining music and sound effects.
    """),
    expected_output=dedent("""
    A script describing the opening, scenes and ending of the video.
    Each of these elements contains the prompt for the image generation
    AI, the duration of the scene, the description, and the text
    content of the scene. Everything written in Brazilian Portuguese
    (pt-BR), except the prompt, which must be in American English.
                           show:
                           \n\nCena:[scene]
                           \n\nDescrção:[description]
                           \n\nTexto:[text]
                           \n\nPROMPT:[image prompt]
    """),
    agent=screenplayer,
    output_file='output-files/roteiro.md',
    verbose=2,
)


crew1 = Crew(
    agents=[pastor, screenplayer],
    tasks=[write, screenplay],
    verbose=2,
    memory=False,
)


# Executar a tarefa com a entrada do arquivo


def execute_task(passagem):
    crew1.kickoff(inputs={'passage': passagem})


# Chamada
if __name__ == "__main__":
    # Receba o argumento da linha de comando
    if len(sys.argv) != 2:
        print("Uso: python meu_script.py <texto>")
        sys.exit(1)

    passagem = sys.argv[1]
    execute_task(passagem)
