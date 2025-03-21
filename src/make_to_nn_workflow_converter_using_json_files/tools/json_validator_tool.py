"""
Tool for validating JSON against validation rules.
"""

from crewai.tools import BaseTool
import json
import re
from typing import Optional, Dict, List, Any, ClassVar, Union

class JsonValidatorTool(BaseTool):
    """
    Tool for validating JSON against validation rules.
    
    This tool takes a JSON input and validates it against the validation rules
    provided during initialization. The validation rules can be a markdown string
    containing the rules for validating the JSON structure.
    """
    
    name: ClassVar[str] = "JSON Validator"
    description: ClassVar[str] = "Validates JSON against validation rules"
    validation_rules: Optional[str] = None
    
    def __init__(self, validation_rules=None, result_as_answer=True):
        """
        Initialize the JsonValidatorTool with validation rules.
        
        Args:
            validation_rules (str): Markdown string containing validation rules
            result_as_answer (bool): Whether to return the tool output directly as the task result
        """
        super().__init__(result_as_answer=result_as_answer)
        # Set validation rules after init
        if validation_rules:
            object.__setattr__(self, 'validation_rules', validation_rules)
    
    def _run(self, json_input: Union[str, Dict]) -> Dict:
        """
        Run the validation on the provided JSON input.
        This is the required method for BaseTool.
        
        Args:
            json_input: The JSON to validate, either as a string or dict
            
        Returns:
            Dict: A dictionary containing validation results
        """
        return self._execute(json_input)
    
    def _execute(self, json_input):
        """
        Execute the validation against the provided JSON input.
        
        Args:
            json_input (str or dict): The JSON to validate, either as a string or dict
            
        Returns:
            dict: A dictionary containing validation results
        """
        try:
            # Convert string input to JSON if needed
            if isinstance(json_input, str):
                try:
                    json_data = json.loads(json_input)
                except json.JSONDecodeError:
                    return {
                        "is_valid": False,
                        "message": "Invalid JSON format",
                        "details": ["The provided input is not valid JSON"]
                    }
            else:
                json_data = json_input
            
            # Perform validation
            return self._validate_json(json_data)
            
        except Exception as e:
            return {
                "is_valid": False,
                "message": f"Validation error: {str(e)}",
                "details": [str(e)]
            }
    
    def _validate_json(self, json_data):
        """
        Validate the JSON data against the validation rules.
        
        Args:
            json_data (dict): The JSON data to validate
            
        Returns:
            dict: A dictionary containing validation results
        """
        issues = []
        
        # Basic structural validation
        if not isinstance(json_data, dict):
            return {
                "is_valid": False,
                "message": "JSON must be an object",
                "details": ["The root element must be a JSON object"]
            }
        
        # Validate Make.com workflow basic structure
        self._validate_make_workflow_structure(json_data, issues)
        
        # Apply additional validation from validation rules if provided
        if self.validation_rules:
            additional_issues = self._apply_validation_rules(json_data)
            issues.extend(additional_issues)
        
        # Return validation result
        if issues:
            return {
                "is_valid": False,
                "message": "JSON validation failed",
                "details": issues
            }
        else:
            return {
                "is_valid": True,
                "message": "JSON structure is valid",
                "details": []
            }
    
    def _validate_make_workflow_structure(self, json_data, issues):
        """
        Validate the basic structure of a Make.com workflow.
        
        Args:
            json_data (dict): The JSON data to validate
            issues (list): List to append validation issues to
        """
        # Check for required top-level fields for Make.com workflow
        required_fields = ["name", "flow"]
        missing_fields = [field for field in required_fields if field not in json_data]
        
        if missing_fields:
            issues.append(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Validate flow array
        if "flow" in json_data:
            if not isinstance(json_data["flow"], list):
                issues.append("'flow' must be an array")
            else:
                # Validate each item in the flow
                for i, item in enumerate(json_data["flow"]):
                    if not isinstance(item, dict):
                        issues.append(f"Item {i} in 'flow' must be an object")
                        continue
                    
                    # Check for required fields in each flow item
                    for field in ["type", "id", "name"]:
                        if field not in item:
                            issues.append(f"Item {i} in 'flow' is missing required field '{field}'")
        
        # Check name field
        if "name" in json_data and not isinstance(json_data["name"], str):
            issues.append("'name' must be a string")
    
    def _apply_validation_rules(self, json_data):
        """
        Apply validation rules extracted from the markdown documentation.
        
        Args:
            json_data (dict): The JSON data to validate
            
        Returns:
            list: List of validation issues found
        """
        issues = []
        
        if not self.validation_rules or not isinstance(self.validation_rules, str):
            return []
        
        # Extract validation patterns from markdown
        
        # Example: Check for required fields based on validation rules
        required_fields_pattern = re.compile(r'Required fields[:\s]+([^\n]+)', re.IGNORECASE)
        match = required_fields_pattern.search(self.validation_rules)
        
        if match:
            fields_text = match.group(1).strip()
            fields = [f.strip() for f in fields_text.split(',')]
            
            for field in fields:
                if field and field not in json_data:
                    issues.append(f"Missing required field from validation rules: {field}")
        
        # Example: Check for valid node types
        node_types_pattern = re.compile(r'Valid (node|module) types[:\s]+([^\n]+)', re.IGNORECASE)
        match = node_types_pattern.search(self.validation_rules)
        
        if match and "flow" in json_data and isinstance(json_data["flow"], list):
            types_text = match.group(2).strip()
            valid_types = [t.strip() for t in types_text.split(',')]
            
            for i, item in enumerate(json_data["flow"]):
                if "type" in item and valid_types and item["type"] not in valid_types:
                    issues.append(f"Item {i} has invalid type: {item['type']}. Valid types are: {', '.join(valid_types)}")
        
        # Example: Check if structure complies with n8n format requirements
        n8n_format_pattern = re.compile(r'n8n format requires[:\s]+([^\n]+)', re.IGNORECASE)
        match = n8n_format_pattern.search(self.validation_rules)
        
        if match:
            format_text = match.group(1).strip()
            issues.append(f"Note for conversion: {format_text}")
        
        return issues 