"""
transferimages.py

Transfers container images between registries using docker or podman,
based on source-destination pairs defined in a YAML file.
"""
import yaml
import subprocess
from typing import Dict, List
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

def run_command(command: List[str]) -> str:
    """
    Runs a subprocess command and returns stdout.
    Raises subprocess.CalledProcessError on failure.
    """
    result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.strip()

def load_yaml(file: str) -> Dict:
    """
    Loads a YAML file and returns a dictionary.
    """
    with open(file, 'r') as f:
        return yaml.safe_load(f)

def transfer_images(cli_tool: str, src_dest_pairs: Dict) -> bool:
    """
    Transfers images using the provided CLI tool and a dictionary of source-destination pairs.
    """
    for pair in src_dest_pairs.get('transfers', []):
        source = pair.get('source')
        destination = pair.get('destination')

        try:
            print(f"Pulling image: {source}")
            logger.info(run_command([cli_tool, 'pull', source]))
            
            print(f"Tagging image: {source} -> {destination}")
            logger.info(run_command([cli_tool, 'tag', source, destination]))
            
            print(f"Pushing image: {destination}")
            logger.info(run_command([cli_tool, 'push', destination]))

        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(e.cmd)}")
            logger.error(f"Return code: {e.returncode}")
            logger.error(f"Error output: {e.stderr.strip()}")
            return False
    
    return True

if __name__ == '__main__':
    yaml_file = 'config.yaml'

    try:
        src_dest_pairs = load_yaml(yaml_file)
        print("YAML file loaded successfully!")
    except Exception as e:
        logger.error(f"Error: loading the YAML file: {e}")
        sys.exit(1)

    print("Enter the Command Line Tool you want to use to transfer images (docker/podman): ", end='', flush=True)
    try:
        cli_tool = input().strip().lower()
    except EOFError:
        logger.error("Error: No input received")
        sys.exit(1)

    if cli_tool not in ['docker', 'podman']:
        print("CLI tool not supported. Use 'docker' or 'podman'.")
        sys.exit(1)

    success_transfer = transfer_images(cli_tool, src_dest_pairs)

    if not success_transfer:
        print("Error in tranfering the images.")
        sys.exit(1)
