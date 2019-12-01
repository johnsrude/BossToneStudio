import argparse
import json


def pretty(filename):
    print('Filename: {}'.format(filename))

    with open(filename, 'r') as file:
        # text = file.read()
        parsed = json.load(file)
        print(json.dumps(parsed, indent=4))


def main():
    parser = argparse.ArgumentParser(description='Print BOSS Tone Studio livesets.')
    parser.add_argument('filename', help="File name (*.tsl")
    args = parser.parse_args()

    pretty(args.filename)

if __name__ == '__main__':
    main()