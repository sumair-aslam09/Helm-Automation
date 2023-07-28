Template Generator using Jinja2
-------------------------------
Python function that uses the Jinja2 Python module to substitute placeholders in a template file. The function should take a key-value hash map and the name of the template file as input. It will then replace the placeholders in the template using the keys in the hashmap.The script will also validate the YAML format of each output file and display the validation resul

Run the script using the following command:
-------------------------------------------
python main.py <template_file_1> <template_file_2> <output_file_1> <output_file_2>
Replace <template_file_1> and <template_file_2> with the paths to the template files you want to use, and <output_file_1> and <output_file_2> with the paths where you want the rendered output files to be created.
.
Example:
--------
Suppose you have two template files: service.j2 and deployment.j2, and you want to generate output files service.yaml and deployment.yaml.

Here's how you can run the script:
----------------------------------
python main.py templates/service.j2 templates/deployment.j2 output/service.yaml output/deployment.yaml

The script will render the templates using the defined data and create the respective output files (service.yaml and deployment.yaml) in the output directory.

Template Files:
---------------
templates/service.j2: The Jinja2 template file for generating Kubernetes Service definitions.
templates/deployment.j2: The Jinja2 template file for generating Kubernetes Deployment definitions.
Output Files:
-------------
output_files/service.yaml: The rendered YAML file for the Kubernetes Service definition.
output_files/deployment.yaml: The rendered YAML file for the Kubernetes Deployment definition.
