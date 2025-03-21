from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from crewai_tools import JSONSearchTool
from crewai_tools import WebsiteSearchTool

@CrewBase
class MakeToNnWorkflowConverterUsingJsonFilesCrew():
    """MakeToNnWorkflowConverterUsingJsonFiles crew"""

    @agent
    def Parser(self) -> Agent:
        return Agent(
            config=self.agents_config['Parser'],
            tools=[FileReadTool(), JSONSearchTool()],
        )

    @agent
    def Mapping_Expert(self) -> Agent:
        return Agent(
            config=self.agents_config['Mapping_Expert'],
            tools=[],
        )

    @agent
    def Validator(self) -> Agent:
        return Agent(
            config=self.agents_config['Validator'],
            tools=[],
        )

    @agent
    def Generator(self) -> Agent:
        return Agent(
            config=self.agents_config['Generator'],
            tools=[],
        )


    @task
    def extract_workflow_structure(self) -> Task:
        return Task(
            config=self.tasks_config['extract_workflow_structure'],
            tools=[FileReadTool(), JSONSearchTool()],
        )

    @task
    def map_modules_to_nodes(self) -> Task:
        return Task(
            config=self.tasks_config['map_modules_to_nodes'],
            tools=[WebsiteSearchTool(), JSONSearchTool(), FileReadTool()],
        )

    @task
    def assemble_n8n_workflow(self) -> Task:
        return Task(
            config=self.tasks_config['assemble_n8n_workflow'],
            tools=[],
        )

    @task
    def validate_n8n_workflow(self) -> Task:
        return Task(
            config=self.tasks_config['validate_n8n_workflow'],
            tools=[],
        )

    @task
    def generate_workflow_file(self) -> Task:
        return Task(
            config=self.tasks_config['generate_workflow_file'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the MakeToNnWorkflowConverterUsingJsonFiles crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential, # Process the tasks in sequence
            verbose=True, # Enable verbose output for the crew
            memory=True, # Enable memory for the crew
        )
