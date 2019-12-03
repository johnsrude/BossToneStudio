import argparse
import json
import yaml


def pretty(args):
    with open(args.filename, "r") as file:
        # text = file.read()
        liveset = json.load(file)
        print(f"Filename: {args.filename}")
        print(f"Device: {liveset['device']}\n")

        indent = "   "

        for i, patch in enumerate(liveset["patchList"]):
            if i % 4 == 0:
                print(f"U{i // 4}")
            print(f"{indent*1}{i % 4 + 1}: {patch['name']} ({i:02d})")

            if not args.patch_list:
                # print(json.dumps(patch["params"], indent=4))
                params = patch["params"]
                pad = indent * 2
                chain = "IN -> "
                if params["comp_sw"] != '0': chain += f"COMP/FX1 -> "
                if params["odds_sw"] != '0': chain += f"OD/DS -> "
                if params["mod_sw"] != '0': chain += f"MOD -> "
                if params["mod_sw"] != '0': chain += f"PREAMP -> "
                if params["pdlfx_sw"] != '0': chain += f"PEDAL FX -> "
                if params["fx2_sw"] != '0': chain += f"EQ/FX2 -> "
                if params["dly_sw"] != '0': chain += f"DELAY -> "
                if params["rev_sw"] != '0': chain += f"REVERB -> "
                chain += f"OUT"

                noise = int(patch['params']['ns_thresh'])
                if noise > 0:
                    chain += f"{pad}Noise: {noise}"

                print(f"{pad}{chain}")


                print(yaml.dump(patch["params"], allow_unicode=True, default_flow_style=False))
                print("")
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
