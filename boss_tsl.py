import argparse
import json


def pretty(args):
    with open(args.filename, "r") as file:
        # text = file.read()
        liveset = json.load(file)
        print("Filename: {}".format(args.filename))
        print("Device: {}\n".format(liveset["device"]))


        #for patch in liveset["patchList"]:
        for i, patch in enumerate(liveset["patchList"]):
            print("{}. {}".format(i, patch["name"]))

            if not args.patch_list:
                pass

        if not args.patch_list:
            print(json.dumps(liveset, indent=4))


def main():
    parser = argparse.ArgumentParser(
        description="Print BOSS Tone Studio livesets.")
    parser.add_argument("filename", help="File name (*.tsl)")
    parser.add_argument("-p", "--patch_list", help="Display list of patches only",
                        action="store_true")
    args = parser.parse_args()

    pretty(args)


if __name__ == "__main__":
    main()
