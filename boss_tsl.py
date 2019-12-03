import argparse
import json
import yaml


def pretty(args):
    with open(args.filename, "r") as file:
        # text = file.read()
        liveset = json.load(file)
        print(f"Filename: {args.filename}")
        print(f"Device: {liveset['device']}\n")

        indent = "    "

        for i, patch in enumerate(liveset["patchList"]):
            if i % 4 == 0:
                print(f"\nU{i // 4}")
            print(f"{indent*1}{i % 4 + 1}: {patch['name']} ({i:02d})")

            if not args.patch_list:
                # print(json.dumps(patch["params"], indent=4))
                chain = "IN ->"

                chain += " OUT"
                print(f"{patch['name']:>4} )")
                print(f"{chain}")
                print(f"Noise: {patch['params']['ns_thresh']}")
                # print(yaml.dump(patch["params"], allow_unicode=True,
                #                 default_flow_style=False))
        # if not args.patch_list:
        #     print(json.dumps(liveset, indent=4))


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
