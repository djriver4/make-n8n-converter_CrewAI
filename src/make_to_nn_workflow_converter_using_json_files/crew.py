from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import FileReadTool
from crewai_tools import JSONSearchTool
from crewai_tools import WebsiteSearchTool
from .tools.json_validator_tool import JsonValidatorTool

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
        # Can't access self.inputs here, will pass validation_rules through the task
        return Agent(
            config=self.agents_config['Validator'],
            tools=[JsonValidatorTool(result_as_answer=True)],
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
            # Customize WebsiteSearchTool with appropriate chunk parameters
            # The min_chunk_size should be greater than chunk_overlap
            tools=[
                WebsiteSearchTool(
                    config=dict(
                        # Using the chunker configuration based on EmbedChain docs
                        chunker=dict(
                            chunk_size=1000,
                            chunk_overlap=100,
                            min_chunk_size=150  # Ensure min_chunk_size > chunk_overlap
                        )
                    )
                ),
                JSONSearchTool(), 
                FileReadTool()
            ],
        )

    @task
    def assemble_n8n_workflow(self) -> Task:
        return Task(
            config=self.tasks_config['assemble_n8n_workflow'],
            tools=[],
        )

    @task
    def validate_n8n_workflow(self) -> Task:
        # Here we can access self.inputs when the task is created
        validation_rules = self.inputs.get('validation_rules', None) if hasattr(self, 'inputs') else None
        return Task(
            config=self.tasks_config['validate_n8n_workflow'],
            tools=[JsonValidatorTool(validation_rules=validation_rules, result_as_answer=True)],
            input_args={'validation_rules': validation_rules}
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
            tasks=[
                self.extract_workflow_structure(),
                self.map_modules_to_nodes(),
                self.assemble_n8n_workflow(),
                self.validate_n8n_workflow(),
                self.generate_workflow_file()
            ], # Specify tasks in explicit order
            process=Process.sequential, # Process the tasks in sequence
            verbose=True, # Enable verbose output for the crew
            memory=True, # Enable memory for the crew
        )
