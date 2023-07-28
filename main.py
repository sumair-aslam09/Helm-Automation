import yaml
import argparse
from jinja2 import Template

# Function to check if the given template file exists
def check_template_file(template_file):
    try:
        with open(template_file, 'r'):
            pass
    except FileNotFoundError:
        print(f"Template file '{template_file}' not found.")
        return False
    except Exception as e:
        print(f"An error occurred while checking the template file '{template_file}': {e}")
        return False
    return True

# Function to check if the given template contains placeholders
def check_template_data(template_file):
    with open(template_file, 'r') as f:
        template_content = f.read()

    # Check if there are any placeholders in the template
    if "{{" not in template_content or "}}" not in template_content:
        raise ValueError("No placeholders found in the template: {}".format(template_file))

# Function to generate a rendered output from a template file and template data
def generate_file(template_file, template_data):
    # Validate template data
    if template_data is None:
        raise ValueError("Template data is missing for the file: {}".format(template_file))

    with open(template_file, 'r') as f:
        template_content = f.read()

    # Create a Template object using the content of the template file
    template = Template(template_content)

    # Render the template using the provided template_data, substituting placeholders with corresponding values
    rendered_output = template.render(template_data)
    return rendered_output



# Function to write the rendered output to the output file
def write_output_file(rendered_content, output_file):
    try:
        with open(output_file, 'w') as f:
            f.write(rendered_content)
        print(f"Output File '{output_file}' has been created.")
    except FileNotFoundError as e:
        print(f"Error: The directory for '{output_file}' does not exist.")
    except PermissionError as e:
        print(f"Error: Permission denied while writing '{output_file}'.")
    except Exception as e:
        print(f"An error occurred while writing the output file '{output_file}': {e}")




# Function to validate YAML format for output file
def is_valid_yaml_file(output_file):
    try:
        with open(output_file, 'r') as file:
            yaml.safe_load(file)
            return True
    except yaml.parser.ParserError as e:
        print(f"Invalid YAML format for file '{output_file}': {e}")
        return False
    except FileNotFoundError as e:
        print(f"Error: The file '{output_file}' does not exist.")
        return False
    except Exception as e:
        print(f"Error occurred while checking YAML file '{output_file}': {e}")
        return False

# Main function to process template files and generate output files
def main(template_files, output_files):
    if len(template_files) != len(output_files):
        print("Error: Number of template files and output files should be the same.")
        return

    # Define key-value pairs for the service data
    service = {
        "service_apiVersion": "v1",
        "service_kind": "Service",
        "service_name": "my-service",
        "service_selector_name": "MyApp",
        "service_port_name": "http",
        "service_protocol": "TCP",
        "service_port": 80,
        "service_targetPort": 9376,
        "service_type": "ClusterIP"
    }

    # Define key-value pairs for the deployment data
    deployment = {
        "deployment_apiversion": "BBSI-PROD",
        "deployment_kind": "deployment",
        "deployment_name": "nginx-deployment",
        "deployment_app_name_label": "nginx",
        "deployment_metadata": None,
        "deployment_annotations": None,
        "deployment_spec": False,
        "deployment_spec_replicas": 3,
        "deployment_spec_selector": None,
        "deployment_image_name": "nginx:1.14.2",
        "deployment_container_name": "nginx",
        "deployment_port": 80,
        "readiness_probe_path": "ref-data/management/health/readiness",
        "readiness_probe_type": "httpGet",
        "readiness_probe_port": 80,
        "readiness_probe_initialDelaySeconds": 100,
        "readiness_probe_periodSeconds": 20,
        "readiness_probe_timeoutSeconds": 10,
        "readiness_probe_failureThreshold": None,
        "liveness_probe_path": "ref-data/management/health/liveness",
        "liveness_probe_type": "httpGet",
        "liveness_probe_port": 80
    }

    for template_file, output_file in zip(template_files, output_files):
        # Check if the template file exists and if it contains placeholders
        if check_template_file(template_file):
            try:
                # Check if the template data is not None and if the template contains placeholders
                check_template_data(template_file)

                # Get the data based on the template_file
                if template_file == 'templates/service.j2':
                    template_data = service
                elif template_file == 'templates/deployment.j2':
                    template_data = deployment
                else:
                    print(f"Unknown template file: {template_file}")
                    continue

                # Render the template using the provided data and get the rendered output
                rendered_output = generate_file(template_file, template_data)

                # Write the rendered output to the output file
                write_output_file(rendered_output, output_file)
            except ValueError as e:
                print(f"An error occurred for template '{template_file}': {e}")

    # Check YAML Validation for each output file
    print("YAML VAlidation of Output file")
    print("-------------------------------")
    for output_file in output_files:
        if is_valid_yaml_file(output_file):
            print(f"The '{output_file}' is a valid YAML file.")
        else:
            print(f"The '{output_file}' is an invalid YAML file.")


if __name__ == "__main__":
    # Create an ArgumentParser object to handle command-line arguments
    parser = argparse.ArgumentParser(description="Generate template files using Jinja2.")

    # Add two required positional arguments: template_files and output_files
    # These arguments will be provided when running the script
    parser.add_argument("template_files", nargs=2, type=str, help="Paths to the template files")
    parser.add_argument("output_files", nargs=2, type=str, help="Paths to the output files")

    # Parse the command-line arguments provided by the user
    args = parser.parse_args()

    # Extract the template_files and output_files from the parsed arguments
    template_files = args.template_files
    output_files = args.output_files

    # Call the main function with the provided template_files and output_files
    main(template_files, output_files)
