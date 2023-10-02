"""A script to run a Chat Completion on files."""
import argparse
from pathlib import Path
from typing import Dict, List

import openai
import yaml


ROOT_DIR = Path(__file__).resolve().parent
SUPPORTED_MODELS = {"text-davinci-003", "gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-4"}


class Configuration:
    """A class to define configuration.

    Attributes:
        openai_token (str): The OpenAI API token used for authentication.
        model (str): The name of the machine learning model to be used.
        openai_completion_options (dict): A dictionary of options for OpenAI completions.
    """
    def __init__(self, config_path: Path):
        """Creates an instance of the class.

        Args:
            config_path: Absolute path to yml configuration file.

        Raises:
            AssertionError: If the specified model is not in the list of supported models.
            AssertionError: If top_p != 1.
        """
        with open(config_path, "r") as file:
            data = yaml.safe_load(file)
        self.openai_token = data['openai_token']
        self.model = data['model']
        self.openai_completion_options = data['openai_completion_options']

        assert self.model in SUPPORTED_MODELS, f'Unknown model: {self.model}'
        assert self.openai_completion_options['top_p'] == 1, \
            f'Multiple choices output is not supported: set top_p = 1.'


def parse_input(input_path: Path) -> List[Dict[str, str]]:
    """Parses the input file and returns a list of messages.

    Args:
        input_path: Path to the input file.

    Returns:
        A list of messages, where each message is a dictionary with 'role' and 'content'.
    """
    messages = []
    def append_messages(role: str, text: List[str]):
        if text[0] == '':
            text = text[1:]
        if text[-1] == '':
            text = text[:-1]
        messages.append({'role': role, 'content': '\n'.join(text)})

    with open(input_path, 'r') as file:
        cur_role, cur_text = None, []
        for line in file:
            line = line.strip()
            if line.startswith('__'):
                if cur_role is not None:
                    append_messages(cur_role, cur_text)
                cur_role, cur_text = line[2:].lower(), []
                continue
            cur_text.append(line)
        append_messages(cur_role, cur_text)
    return messages


def main(config_path: str, input_path: str, output_path: str):
    """Main function to run the script.

    Args:
        config_path: Path to the configuration file.
        input_path: Path to the input file.
        output_path: Path to the output file.
    """
    config = Configuration(ROOT_DIR / Path(config_path))
    messages = parse_input(ROOT_DIR / Path(input_path))

    openai.api_key = config.openai_token
    response = openai.ChatCompletion.create(
        model=config.model,
        messages=messages,
        **config.openai_completion_options
    )

    token_usage = response["usage"]["total_tokens"]
    result = response["choices"][-1]["message"]["content"]
    # stop_reason =

    with open(ROOT_DIR / Path(output_path), 'w') as file:
        file.write(result)
    print(f'Done! Model used: {config.model}. Tokens used: {token_usage}.')


if __name__ == '__main__':
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description='ChatGPT Argument Parser')
    parser.add_argument(
        '-c',
        '--config',
        default='config.yml',
        help='Relative path to the configuration file (default: config.yml).'
    )
    parser.add_argument(
        '-i',
        '--input',
        default='input.md',
        help='Relative path to the input file (default: input.md).'
    )
    parser.add_argument(
        '-o',
        '--output',
        default='output.md',
        help='Relative path to the output file (default: output.md).'
    )

    args = parser.parse_args()
    main(args.config, args.input, args.output)
