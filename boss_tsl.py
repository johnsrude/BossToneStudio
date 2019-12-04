import argparse
import json
import yaml

def main():
    parser = argparse.ArgumentParser(
        description="Print BOSS Tone Studio livesets.")
    parser.add_argument("filename", help="File name (*.tsl)")
    parser.add_argument("-L", "--patch_list", help="Display list of patches only",
                        action="store_true")
    parser.add_argument("-p", "--patch", help="Display single patch", nargs="+")
    args = parser.parse_args()
    if args.patch: args.patch = " ".join(args.patch)
    pretty(args)


def pretty(args):
    with open(args.filename, "r") as file:
        # text = file.read()
        liveset = json.load(file)
        print(f"Filename: {args.filename}")
        print(f"Device: {liveset['device']}\n")

        indent = "   "

        for i, patch in enumerate(liveset["patchList"]):
            if args.patch and args.patch not in patch["name"]: continue

            if i % 4 == 0:
                print(f"U{i // 4}")
            print(f"{indent * 1}{i % 4 + 1}: {patch['name']} ({i:02d})")

            if not args.patch_list:
                # print(json.dumps(params, indent=4))
                print_me80_patch(indent, patch)
        # if not args.patch_list:
        #     print(json.dumps(liveset, indent=4))


pedal_fx_dict = {
    "0": "WAH",
    "1": "VOICE",
    "2": "+1 OCT",
    "3": "+2 OCT",
    "4": "-1 OCT",
    "5": "FREEZE",
    "6": "OSC DELAY",
    "7": "OD/DS",
    "8": "MOD RATE",
    "9": "DELAY LEV",
}


def print_me80_patch(indent, patch):
    params = patch["params"]

    pedal_fx = params["pdlfx_sw"] != '0'
    pedal_fx_type = pedal_fx_dict[params['pdlfx_type']]
    noise = int(params['ns_thresh'])

    print_effects_chain(indent, noise, params, pedal_fx, pedal_fx_type)
    print_control_pedal(indent, params)

    # print(yaml.dump(params, allow_unicode=True, default_flow_style=False))
    print("")


def print_control_pedal(indent, params):
    ctl = "CTL "
    if params["ctl_mode"] == "1":
        ctl += "(TOGGLE): "
    else:
        ctl += "(MOMENTARY): "
    controls = ['PEDAL FX', 'REVERB', 'EQ/FX2', 'PREAMP', 'DELAY', 'MOD', 'OD/DS',
                'COMP/FX1']
    bitmap = list(f'{int(params["ctl_target"]):08b}')
    active_controls = [c for b, c in zip(bitmap, controls) if b == '1']
    print(f"{indent * 2}{ctl}{', '.join(active_controls)}")


def print_effects_chain(indent, noise, params, pedal_fx, pedal_fx_type):
    chain = "IN -> "
    if pedal_fx: chain += f"PEDAL FX ({pedal_fx_type}) -> "
    if params["comp_sw"] != '0': chain += "COMP/FX1 -> "
    if params["odds_sw"] != '0': chain += "OD/DS -> "
    if params["mod_sw"] != '0': chain += "PREAMP -> "
    if noise > 0: chain += f"NS ({noise}) -> "
    if params["pdlfx_sw"] == '0': chain += "PEDAL VOL -> "
    if params["mod_sw"] != '0': chain += "MOD -> "
    if params["fx2_sw"] != '0': chain += "EQ/FX2 -> "
    if params["dly_sw"] != '0': chain += "DELAY -> "
    if params["rev_sw"] != '0': chain += "REVERB -> "
    chain += f"OUT"
    pad = indent * 2
    print(f"{pad}{chain}")


if __name__ == "__main__":
    main()
