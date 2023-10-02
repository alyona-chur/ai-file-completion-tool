# AI Text Completion Tool

This is a Python implementation for using OpenAI's GPT models for text completion on files.

## Installation

1. Clone the repository.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Create configuration and input files.

## Usage

The script can be run with the following command:
```
python run_completion.py -c config.yml -i input.md -o output.md
```
The `-c`, `-i`, and `-o` flags stand for the relative paths to configuration, input, and output files, respectively. If these arguments are not provided, the script will default to files named `config.yml`, `input.md`, and `output.md` in the same directory as the script.

## Examples

Examples of configuration, input, and output files can be found in the project directory.

- The **configuration file** is a YAML file with the following.
- The **input file** is a markdown file with messages separated by lines starting with ```__```. The line after ```__``` should contain the role of the message (either 'system', 'user', or 'assistant'), and the lines that follow until the next line starting with ```__``` are the content of the message.

```markdown
__SYSTEM
Hello! How can I assist you today?

__USER
I need help with my homework.
```

- The **output file** is a markdown file with the generated text. The text is written as is, without any formatting.
