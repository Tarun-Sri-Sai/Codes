import os
import argparse
import yaml
import pprint
import typing


def parse_arguments() -> tuple[dict[str, typing.Any], argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(description='Material Builder')
    sub_parsers = parser.add_subparsers(dest='subcommand')

    subcommands = {
        'complete': sub_parsers.add_parser(
            'complete',
            description='Combines all units into one directory for a subject'),
        'unit': sub_parsers.add_parser(
            'unit',
            description='Creates the next unit directory for a subject'),
        'prompts': sub_parsers.add_parser(
            'prompts',
            description='Generates ChatGPT prompts for topics in topics.yml'),
        'print': sub_parsers.add_parser(
            'print',
            description='Print the ChatGPT response to unit file')
    }

    subcommands['complete'].add_argument('subject_name',
                                         help='Name of the subject')
    subcommands['unit'].add_argument('subject_name',
                                     help='Name of the subject')
    subcommands['prompts'].add_argument('start',
                                        help='Prompt start')
    subcommands['prompts'].add_argument('--input', '-i',
                                        dest='input_file',
                                        help='Input yaml file')
    subcommands['prompts'].add_argument('--output', '-o',
                                        dest='output_file',
                                        help='Output text file')
    subcommands['prompts'].add_argument('--prompt', '-p',
                                        dest='optional_prompt',
                                        help='Optional prompt')
    subcommands['print'].add_argument('subject_name',
                                      help='Name of the subject')
    subcommands['print'].add_argument('unit',
                                      type=int,
                                      help='Unit number')

    return vars(parser.parse_args()), parser


def combine_units(args: dict[str, typing.Any],
                  parser: argparse.ArgumentParser) -> None:
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
                            f'# {args["subject_name"].upper()}\n',
                            ''))
                    count += 1
                except:
                    break

            print(f'Generated complete file for {count} units')
    except Exception as e:
        print(f'Error trying to combine units due to {e}')
        parser.print_help()
        raise


def add_unit(args: dict[str, typing.Any],
             parser: argparse.ArgumentParser) -> None:
    try:
        for i in range(MAX_UNITS := 1000):
            dest_dir = os.path.join(args['subject_name'], f'unit_{i + 1}')
            os.makedirs(dest_dir, exist_ok=True)

            dest_file = os.path.join(dest_dir, f'unit_{i + 1}.md')
            if os.path.isfile(dest_file):
                continue

            with open(dest_file, 'w') as f:
                print(f'# {args["subject_name"].upper()}\n', file=f)
                print(f'## Unit-{i + 1}\n', file=f)

            print(f'Generated {dest_file}')
            return

        raise ValueError(f"{MAX_UNITS} units is too much. Don't you think?")

    except Exception as e:
        print(f'Error trying to add unit due to {e}')
        parser.print_help()
        raise


def ensure_dir_path_exists(file_path: str) -> None:
    dir_path = os.path.dirname(file_path)
    if not dir_path:
        return

    os.makedirs(dir_path, exist_ok=True)


def generate_prompts(args: dict[str, typing.Any],
                     parser: argparse.ArgumentParser) -> None:
    try:
        input_file = args['input_file'] or 'topics.yml'
        if not os.path.isfile(input_file):
            raise ValueError(f'{input_file} does not exist')

        optional_prompt = args.get('optional_prompt', None)
        start = args['start']

        try:
            with open(input_file, 'r') as f:
                data = yaml.safe_load(f)

            prompts = []
            for unit_name, children in data.items():
                prompts.append(f'# {unit_name}')
                for heading, topics in children.items():
                    print(f'Topic heading: {heading}\nTopics:')
                    pprint.pprint(topics)

                    end = f'from the topic "{heading.strip()}".'

                    for topic in topics:
                        prompt_words = [start, f'"{topic}"', end]
                        if optional_prompt:
                            prompt_words.append(optional_prompt)

                        prompts.append(' '.join(prompt_words))

        except AttributeError:
            raise ValueError(f'Invalid data in {input_file}')

        print(f'Generated {len(prompts)} prompts')

        output_file = args.get('output_file', 'prompts.txt')
        ensure_dir_path_exists(output_file)

        with open(output_file, 'w') as f:
            print(*prompts, sep='\n', file=f)

    except Exception as e:
        print(f'Error trying to generate prompts due to {e}')
        parser.print_help()
        raise


def print_to_unit(args: dict[str, typing.Any],
                  parser: argparse.ArgumentParser) -> None:
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

        data = data.replace('\n#', '\n###')

        with open(dest_file, 'a', encoding='utf-8') as f:
            print(data, file=f)
        print(f'Finished writing output from {os.path.basename(input_file)}')
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
    }
    try:
        subcommand_switch[args['subcommand']](args, parser)
    except Exception as _:
        parser.print_help()
        raise


if __name__ == '__main__':
    main()
