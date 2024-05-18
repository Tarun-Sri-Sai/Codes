from argparse import ArgumentParser
from pprint import pprint
from typing import Any
import os
import json
import sys


def parse_arguments() -> tuple[dict[str, Any], ArgumentParser]:
    parser = ArgumentParser(description='Material Builder')
    sub_parsers = parser.add_subparsers(dest='subcommand')

    # 'complete' subcommand
    complete = sub_parsers.add_parser(
        'complete',
        description='Combines all units into one directory for a subject')
    complete.add_argument(
        'subject_name',
        help='Name of the subject to generate complete material for')

    unit = sub_parsers.add_parser(
        'unit',
        description='Creates the next unit directory for a subject')
    unit.add_argument(
        'subject_name',
        help='Name of the subject to create new unit for')

    # 'prompts' subcommand
    prompts = sub_parsers.add_parser(
        'prompts',
        description='Generates ChatGPT prompts for topics in topics.yml')
    prompts.add_argument(
        'start',
        help='Prefix for the prompt, e.g: Build a study guide in Markdown for')
    prompts.add_argument(
        '--input', '-i', dest='input_file',
        help=('A JSON file containing key-value pairs with the topic as key, '
              'and a list of subtopics as its value'))
    prompts.add_argument('--output', '-o', dest='output_file',
                         help='A TXT file to write prompts to')
    prompts.add_argument('--prompt', '-p', dest='optional_prompt',
                         help='Optional suffix for the prompt')

    # 'print' subcommand
    print = sub_parsers.add_parser(
        'print',
        description='Print the ChatGPT response to unit file')
    print.add_argument('subject_name',
                       help='Name of the subject to append content to')
    print.add_argument('unit', type=int,
                       help='Unit number to append content to')

    # 'clean' subcommand
    clean = sub_parsers.add_parser(
        'clean', description='Remove sections from Markdown content')
    clean.add_argument('subject',
                       help='Name of the subject to remove sections from')
    clean.add_argument('unit', type=int,
                       help='Unit number to remove sections from')
    clean.add_argument('headings',
                       help='Comma-separated headings of sections to remove')

    return vars(parser.parse_args()), parser


def combine_units(args: dict[str, Any], parser: ArgumentParser) -> None:
    try:
        dest_dir = os.path.join(args['subject_name'], 'complete')
        os.makedirs(dest_dir, exist_ok=True)

        src_dir = args['subject_name']

        dest_file = os.path.join(dest_dir, f'{args["subject_name"]}.md')
        with open(dest_file, 'w', encoding='utf-8') as writer:
            files = [os.path.abspath(os.path.join(dir_path, file))
                     for dir_path, _, files in os.walk(src_dir)
                     for file in files if file.endswith('.md')]

            writer.write(f'# {args["subject_name"].upper()}\n')
            count = 0
            for file in files:
                try:
                    with open(file, 'r', encoding='utf-8') as reader:
                        text = reader.read()
                        writer.write(text.replace(
                            f'# {args["subject_name"].upper()}\n', ''))
                    count += 1
                except:
                    break

            print(f'Generated complete file for {count} units')
    except Exception as e:
        print(f'Error trying to combine units due to {e}')
        parser.print_help()
        raise


def add_unit(args: dict[str, Any], parser: ArgumentParser) -> None:
    try:
        for i in range(MAX_UNITS := 1000):
            dest_dir = os.path.join(args['subject_name'], f'unit_{i + 1}')
            os.makedirs(dest_dir, exist_ok=True)

            dest_file = os.path.join(dest_dir, f'unit_{i + 1}.md')
            if os.path.isfile(dest_file):
                continue

            with open(dest_file, 'w') as f:
                print(f'# {args["subject_name"].upper()}\n', file=f)
                print(f'## Unit-{i + 1}', file=f)

            print(f'Generated {dest_file}')
            return

        raise ValueError(f"{MAX_UNITS} units is too much.")

    except Exception as e:
        print(f'Error trying to add unit due to {e}')
        parser.print_help()
        raise


def ensure_dir_path_exists(file_path: str) -> None:
    dir_path = os.path.dirname(file_path)
    if not dir_path:
        return

    os.makedirs(dir_path, exist_ok=True)


def generate_prompts(args: dict[str, Any], parser: ArgumentParser) -> None:
    try:
        input_file = args['input_file'] or 'topics.json'
        if not os.path.isfile(input_file):
            raise ValueError(f'{input_file} does not exist')

        optional_prompt = args.get('optional_prompt', None)
        start = args['start']

        try:
            with open(input_file, 'r') as f:
                data = json.load(f)

            prompts = []
            for heading, topics in data.items():
                print(f'Topic heading: {heading}\nTopics:')
                pprint(topics)

                end = f'from the topic "{heading.strip()}".'

                for topic in topics:
                    prompt_words = [start, f'"{topic}"', end]
                    if optional_prompt:
                        prompt_words.append(optional_prompt)

                    prompts.append(' '.join(prompt_words))

        except AttributeError:
            raise ValueError(f'Invalid data in {input_file}')

        print(f'Generated {len(prompts)} prompt(s)')

        output_file = args.get('output_file') or 'prompts.txt'
        ensure_dir_path_exists(output_file)

        with open(output_file, 'w') as f:
            print(*prompts, sep='\n', file=f)

    except Exception as e:
        print(f'Error trying to generate prompts due to {e}')
        parser.print_help()
        raise


def print_to_unit(args: dict[str, Any], parser: ArgumentParser) -> None:
    try:
        unit_no = args['unit']
        dest_dir = os.path.join(args['subject_name'],
                                f'unit_{unit_no}')
        os.makedirs(dest_dir, exist_ok=True)

        dest_file = os.path.join(dest_dir, f'unit_{unit_no}.md')
        if not os.path.isfile(dest_file):
            raise ValueError(f'Unit-{unit_no} is not there, '
                             "generate it using 'unit' subcommand")

        input_file = args.get('input_file', 'input.md')
        if not os.path.isfile(input_file):
            raise ValueError(f'{input_file} does not exist')

        with open(input_file, 'r', encoding='utf-8') as f:
            data = f.read()

        data = ('\n' + data).replace('\n#', '\n###')

        with open(dest_file, 'a', encoding='utf-8') as f:
            f.write(data)
        print(f'Finished writing output from {os.path.basename(input_file)}')

    except Exception as e:
        print(f'Error trying to print to unit due to {e}')
        parser.print_help()
        raise


def remove_sections(args: dict[str, Any], parser: ArgumentParser) -> None:
    try:
        unit_name = f"unit_{args['unit']}"
        dest_dir = os.path.join(args['subject'], unit_name)
        dest_file = os.path.join(dest_dir, unit_name + '.md')

        with open(dest_file, 'r', encoding='utf-8') as f:
            lines = [l.rstrip() for l in f.read().splitlines()]

        patterns = [x.strip() for x in args['headings'].split(',')]

        result = []
        i, line_count = 0, len(lines)
        while i < line_count:
            line = lines[i]
            if not line.startswith('#'):
                result.append(lines[i])
                i += 1
                continue
            stripped_content = line[line.rfind('#') + 1:].strip()
            i += 1
            if (line.startswith('#') and len(stripped_content) > 0
                    and any(p for p in patterns if p in stripped_content)):
                heading_level = line.count('#')
                while (i < line_count
                       and not (lines[i].startswith('#')
                                and lines[i].count('#') <= heading_level)):
                    i += 1
            else:
                result.append(line)
                i += 1

        with open(dest_file, 'w', encoding='utf-8') as f:
            print('\n'.join(result), file=f)

    except Exception as e:
        print(f'Error trying to print to unit due to {e}')
        parser.print_help()
        raise


def main() -> None:
    args, parser = parse_arguments()

    subcommand_switch = {
        'complete': combine_units,
        'unit': add_unit,
        'prompts': generate_prompts,
        'print': print_to_unit,
        'clean': remove_sections,
    }
    try:
        subcommand_switch[args['subcommand']](args, parser)
    except Exception as _:
        sys.exit(1)


if __name__ == '__main__':
    main()
