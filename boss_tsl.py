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
                # print(json.dumps(params, indent=4))
                print_patch(indent, patch)
        # if not args.patch_list:
        #     print(json.dumps(liveset, indent=4))

pedal_fx_dict = {
    "0" : "WAH",
    "1" : "VOICE",
    "2" : "+1 OCT",
    "3" : "+2 OCT",
    "4" : "-1 OCT",
    "5" : "FREEZE",
    "6" : "OSC DELAY",
    "7" : "OD/DS",
    "8" : "MOD RATE",
    "9" : "DELAY LEV",
}

def print_patch(indent, patch):
    params = patch["params"]
    pad = indent * 2

    pedal_fx = params["pdlfx_sw"] != '0'
    pedal_fx_type = pedal_fx_dict[params['pdlfx_type']]
    noise = int(params['ns_thresh'])

    chain = "IN -> "
    if pedal_fx: chain += f"PEDAL FX ({pedal_fx_type}) -> "
    if params["comp_sw"] != '0': chain += f"COMP/FX1 -> "
    if params["odds_sw"] != '0': chain += f"OD/DS -> "
    if params["mod_sw"] != '0': chain += f"PREAMP -> "
    if noise > 0: chain += f"NS ({noise}) -> "
    if params["pdlfx_sw"] == '0': chain += f"PEDAL VOL -> "
    if params["mod_sw"] != '0': chain += f"MOD -> "
    if params["fx2_sw"] != '0': chain += f"EQ/FX2 -> "
    if params["dly_sw"] != '0': chain += f"DELAY -> "
    if params["rev_sw"] != '0': chain += f"REVERB -> "
    chain += f"OUT"
    print(f"{pad}{chain}")
    print(f"CTL: TBD")
    print(yaml.dump(params, allow_unicode=True, default_flow_style=False))
    print("")


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
