# make-n8n-converter_CrewAI

Welcome to the make-n8n-converter_CrewAI project, powered by [crewAI](https://crewai.com). This project is designed to convert Make.com workflow JSON files into n8n workflow files using a multi-agent AI system, leveraging the powerful and flexible framework provided by crewAI.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/make_to_nn_workflow_converter_using_json_files/config/agents.yaml` to define your agents
- Modify `src/make_to_nn_workflow_converter_using_json_files/config/tasks.yaml` to define your tasks
- Modify `src/make_to_nn_workflow_converter_using_json_files/crew.py` to add your own logic, tools and specific args
- Modify `src/make_to_nn_workflow_converter_using_json_files/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the make-n8n-converter Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Understanding Your Crew

The make-n8n-converter Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the make-n8n-converter Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
