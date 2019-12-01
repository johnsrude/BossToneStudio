import argparse


def main():
    parser = argparse.ArgumentParser(description='Print BOSS Tone Studio livesets.')
    parser.add_argument('filename', help="File name (*.tsl")
    args = parser.parse_args()
    print('Filename: {}'.format(args.filename))

if __name__ == '__main__':
    main()