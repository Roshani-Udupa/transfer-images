import yaml
import subprocess

def run_podman_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Success {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error {e.stderr}")

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def process_images(yaml_file):
    data = load_yaml(yaml_file)
    
    for item in data['transfers']:
        source = item['source']
        destination = item['destination']
        
        run_podman_command(f"podman pull {source}")
        run_podman_command(f"podman tag {source} {destination}")
        run_podman_command(f"podman push {destination}")


if __name__ == '__main__':
    yaml_file = 'config.yaml'
    process_images(yaml_file)
