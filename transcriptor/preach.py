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
    2. identify the target audience this text is intended for.
    3. The text must have an emotional, comforting tone, as it is
       targeted to an individual of the identified target audience
       and contain between 350 and 400 words.
    """),
    expected_output=dedent("""
    A text with an engaging, eloquent and sensitive style,
    with no date or time references, aimed at the target audience
    dentified, and calling the recipient 'querido amigo, querida amiga', in
    Brazilian Portuguese (pt-BR), structured like a letter, not signed,
    with numbers written in full, showing:
    \n\nAssunto: [subject] \n\nIntenção:[Intention]
    \n\nPúblico: [target_audience] \n\n[letter text]
    """),
    agent=pastor,
    output_file='output-files/pregacao{passage}.md',
    verbose=2,
)


screenplay = Task(
    description=dedent("""
    Using the exact same text created by in task write, create a script for
    a YouTube video, containing prompts for generating images, and
    defining music and sound effects.
    """),
    expected_output=dedent("""
    A script describing the opening, up to 10 scenes and ending of the video.
    Each of these elements contains:
      the detailed prompt for the AI image generation with at least 15 words
        and add the text 'ar 16:9, photo realistic, photographic quality'
        to the end of the prompt.
      the duration of the scene;
      the description; and
      text content of the scene.
    Everything written in Brazilian Portuguese (pt-BR),
      except the prompt, which must be in American English.
    The output must be written in table format to an csv file
    with the columns:
    \nCena:[scene]
    \nDuração:[duration in seconds]
    \nPROMPT:[PROMPT enclosed in quotes]
    \nDescrição:[description]
    \nTexto:[text]
    """),
    agent=screenplayer,
    output_file='output-files/roteiro{passage}.md',
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
        print(
            "Uso: python preach.py 'livro capitulo"
            "[:versículo][-versículo final]'"
            )
        sys.exit(1)

    passagem = sys.argv[1]
    execute_task(passagem)

