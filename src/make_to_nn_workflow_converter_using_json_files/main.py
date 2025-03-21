#!/usr/bin/env python
import sys
import os
from make_to_nn_workflow_converter_using_json_files.crew import MakeToNnWorkflowConverterUsingJsonFilesCrew
import json
# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# =========== INPUT DATA =========== #
def get_input_data():
    # Calculate the path to the knowledge directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_file = os.path.join(project_root, "knowledge", "test_workflow_input.json")
    
    try:
        with open(input_file, 'r') as file:
            input_data = json.load(file)
        return input_data
    except FileNotFoundError:
        print(f"Warning: Input data file not found at {input_file}. Using default input.")
        # Return the default input as a fallback
        return {
            "name": "Test Workflow",
            "flow": [
                {"type": "http", "id": "1", "name": "HTTP Request"},
                {"type": "email", "id": "2", "name": "Send Email"}
            ]
        }
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in input file at {input_file}. Using default input.")
        # Return the default input as a fallback
        return {
            "name": "Test Workflow",
            "flow": [
                {"type": "http", "id": "1", "name": "HTTP Request"},
                {"type": "email", "id": "2", "name": "Send Email"}
            ]
        }

# =========== MAPPING CONFIG =========== #
# Load the mapping config from the JSON file
def get_mapping_config():
    # Calculate the path to the knowledge directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    mapping_file = os.path.join(project_root, "knowledge", "mapping_config.json")
    
    try:
        with open(mapping_file, 'r') as file:
            mapping_config = json.load(file)
        return mapping_config
    except FileNotFoundError:
        print(f"Warning: Mapping config file not found at {mapping_file}. Using default mapping.")
        # Return the default mapping as a fallback
        return {
            "webhook": "Webhook Trigger",
            "filter": "IF",
            "transformer": "Set",
            "action": "Function",
            "internal": "n8n-nodes-base.noOp",
            "salesforce": "n8n-nodes-base.salesforce",
            "mailchimp": "n8n-nodes-base.mailchimp"
        }
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in mapping config file at {mapping_file}. Using default mapping.")
        # Return the default mapping as a fallback
        return {
            "webhook": "Webhook Trigger",
            "filter": "IF",
            "transformer": "Set",
            "action": "Function",
            "internal": "n8n-nodes-base.noOp",
            "salesforce": "n8n-nodes-base.salesforce",
            "mailchimp": "n8n-nodes-base.mailchimp"
        }

# =========== VALIDATION RULES =========== #
# Read the validation rules from the knowledge markdown file
def get_validation_rules():
    # Calculate the path to the knowledge directory
    # Current file is in src/make_to_nn_workflow_converter_using_json_files/main.py
    # Knowledge dir is in root/knowledge
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    validation_file = os.path.join(project_root, "knowledge", "n8n_workflow_json_structure.md")
    
    try:
        with open(validation_file, 'r') as file:
            validation_rules = file.read()
        return validation_rules
    except FileNotFoundError:
        print(f"Warning: Validation rules file not found at {validation_file}. Using placeholder value.")
        return "sample_value"

# =========== RUN =========== #
def run():
    """
    Run the crew.
    """
    inputs = {
        'make_json_input': get_input_data(),
        'mapping_config': get_mapping_config(),
        'validation_rules': get_validation_rules()
    }
    MakeToNnWorkflowConverterUsingJsonFilesCrew().crew().kickoff(inputs=inputs)

# =========== TRAIN =========== #
def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'make_json_input': get_input_data(),
        'mapping_config': get_mapping_config(),
        'validation_rules': get_validation_rules()
    }
    try:
        MakeToNnWorkflowConverterUsingJsonFilesCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

# =========== REPLAY =========== #
def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MakeToNnWorkflowConverterUsingJsonFilesCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

# =========== TEST =========== # 
def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'make_json_input': get_input_data(),
        'mapping_config': get_mapping_config(),
        'validation_rules': get_validation_rules()
    }
    try:
        MakeToNnWorkflowConverterUsingJsonFilesCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

# =========== MAIN =========== #
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: main.py <command> [<args>]")
        sys.exit(1)

    command = sys.argv[1]
    if command == "run":
        run()
    elif command == "train":
        train()
    elif command == "replay":
        replay()
    elif command == "test":
        test()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
