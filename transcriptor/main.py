import os

from agents import CreatingContentAgents
from crewai import Crew
from dotenv import load_dotenv
from tasks import PreachDefiningTasks, VideoStoryTellingTasks

load_dotenv()

initial_tasks = PreachDefiningTasks()
final_tasks = VideoStoryTellingTasks()
agents = CreatingContentAgents()

print('##Bem vindo ao gerador de preces e videos##')
print('-------------------------------------------')
bible_verse = input('Sobre qual versículo vamos falar hoje?\n')

# cria os agentes para a geração do conteúdo
theologian_agent = agents.theologian_agent()
preacher_agent = agents.preacher_agent()

# cria as tarefas de geração de conteúdo
dedication_task = initial_tasks.dedication_task(theologian_agent, bible_verse)  # noqa: E501
preach_development_task = initial_tasks.preach_development_task(
    preacher_agent, bible_verse
)  # noqa: E501
preach_format_task = initial_tasks.preach_format_task(
    preacher_agent, bible_verse
)  # noqa: E501

# cria crew for preach
preach_crew = Crew(
    agents=[theologian_agent, preacher_agent],
    tasks=[dedication_task, preach_development_task, preach_format_task],
    verbose=True,
)

preaching = preach_crew.kickoff()

# Salvar o resultado da crew em um arquivo
output_file_name = (
    f'textos-gerados/{bible_verse}/texto-narracao|txt'.replace(' ', '_')
    .replace(':', '_')
    .replace('.', '_')
    .replace('|', '.')
)

# Extraindo o caminho do diretório do nome do arquivo
directory = os.path.dirname(output_file_name)

# Verificando se o diretório existe, se não, cria-o
if not os.path.exists(directory):
    os.makedirs(directory)

# Escrevendo no arquivo
with open(output_file_name, 'w', encoding='utf-8') as file:
    file.write(preaching)

print(f'Arquivo de saída salvo em {output_file_name}')

# cria agentes responsáveis pelo video
video_maker_agent = agents.video_maker_agent()

# cria tarefas de geração do video
storytelling_task = final_tasks.storytelling_task(video_maker_agent, preaching)

# cria crew para roteiro do video
video_crew = Crew(
    agents=[video_maker_agent], tasks=[storytelling_task], verbose=True
)

video = video_crew.kickoff()

# Definindo o nome do arquivo de saída
output_file_name = (
    f'textos-gerados/{bible_verse}/roteiro-video|txt'.replace(' ', '_')
    .replace(':', '_')
    .replace('.', '_')
    .replace('|', '.')
)

# Extraindo o caminho do diretório do nome do arquivo
directory = os.path.dirname(output_file_name)

# Verificando se o diretório existe, se não, cria-o
if not os.path.exists(directory):
    os.makedirs(directory)

# Escrevendo no arquivo
with open(output_file_name, 'w', encoding='utf-8') as file:
    file.write(video)

print(f'Arquivo de saída salvo em {output_file_name}')
print(video)
