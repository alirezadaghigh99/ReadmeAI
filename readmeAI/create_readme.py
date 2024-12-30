import os
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser


def extract_dependencies(file_path):
    with open(file_path, "r") as f: 
        content = f.read()
        imports = re.findall(r'^(?:import|from) (\S+)', content, re.MULTILINE)
        return imports
    
def analyse_file_purpose(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        llm = ChatOpenAI(model="gpt-4o")
        prompt = PromptTemplate(template="Explain the purpose of this code:\n{content}")
        output_parser = StrOutputParser()

        chain = prompt | llm | output_parser
        result = chain.invoke({"content": content})
        print(result)
        return result

def find_entry_point(repo_path):
    entry_points = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py') or file.endswith('.js'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    if re.search(r'if __name__ == ["\']__main__["\']', f.read()):
                        entry_points.append(file_path)
    return entry_points

def generate_readme_section(description, dependencies, entry_points):
    llm = ChatOpenAI(model="gpt-4o")
    prompt = PromptTemplate(template="""
        Generate a README section with the following details:
        Description: {description}
        Dependencies: {dependencies}
        Entry Points: {entry_points}
        """)
    output_parser = StrOutputParser()
    print("generating readme section")
    chain = prompt | llm | output_parser
    return chain.invoke({"description":description, "dependencies":dependencies, "entry_points":entry_points})



def create_readme(repo_path):
    all_files = set()
    all_dependencies = set()
    file_descriptions = {}

    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".py") or file_path.endswith(".js"):
                all_files.add(file_path)
                dependencies = extract_dependencies(file_path)
                all_dependencies.update(dependencies)
                description = analyse_file_purpose(file_path)
                file_descriptions[file] = description

    entry_points = find_entry_point(repo_path)
    readme_content = generate_readme_section(
        description="Project to automatically generate a README",
        dependencies=list(all_dependencies),
        entry_points=entry_points
    )
    with open(os.path.join("readmes", "README.md"), "w") as f:
        f.write(readme_content)
    print("README generated!")
                