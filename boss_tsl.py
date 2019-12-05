import argparse
import json
import yaml

def main():
    parser = argparse.ArgumentParser(
        description="Print BOSS Tone Studio livesets.")
    parser.add_argument("-L", "--patch_list", help="Display list of patches only",
                        action="store_true")
    parser.add_argument("filename", help="File name (*.tsl)")
    parser.add_argument("patch", help="Display only 1 patch which may have spaces in "
                                      "the name", nargs="*")
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
            print(f"{indent}{i % 4 + 1}: {patch['name']} ({i:02d})"
                  f"{indent*2}{control_string(patch['params'])}")

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

comp_fx1_dict = {
    "0": "COMP",
    "1": "T.WAH UP",
    "2": "T.WAH DOWN",
    "3": "OCTAVE",
    "4": "SLOW GEAR",
    "5": "DEFRETTER",
    "6": "RING MOD",
    "7": "AC SIM",
    "8": "Single>Hum",
    "9": "Hum>Single",
    "10": "SOLO",
}

od_ds_dict = {
    "0": "BOOST",
    "1": "OVERDRIVE",
    "2": "T-SCREAM",
    "3": "BLUES",
    "4": "TURBO OD",
    "5": "DISTORTION",
    "6": "TURBO DS",
    "7": "METAL DS",
    "8": "CORE",
    "9": "FUZZ",
    "10": "OCT FUZZ",
}

mod_dict = {
    "0": "PHASER",
    "1": "FLANGER",
    "2": "TREMOLO",
    "3": "CHORUS",
    "4": "VIBRATO",
    "5": "PITCH SHIFT",
    "6": "HARMONIST",
    "7": "ROTARY",
    "8": "UNI-V",
    "9": "DELAY",
    "10": "OVERTONE",
}

delay_dict = {
    "0": "1-99 ms",
    "1": "100-600 ms",
    "2": "500-6000 ms",
    "3": "ANALOG",
    "4": "TAPE",
    "5": "MODULATE",
    "6": "REVERSE",
    "7": "CHO + DELAY",
    "8": "TEMPO",
    "9": "TERA ECHO",
    "10": "PHRASE LOOP",
}

preamp_dict = {
    "0": "AC",
    "1": "CLEAN",
    "2": "TWEED",
    "3": "CRUNCH",
    "4": "COMBO",
    "5": "LEAD",
    "6": "DRIVE",
    "7": "STACK",
    "8": "METAL",
}

eq_fx2_dict = {
    "0": "PHASER",
    "1": "TREMOLO",
    "2": "BOOST",
    "3": "DELAY",
    "4": "CHORUS",
    "5": "EQ",
}

reverb_dict = {
    "0": "ROOM",
    "1": "HALL",
    "2": "SPRING",
}

def print_me80_patch(indent, patch):
    params = patch["params"]

    pedal_fx = params["pdlfx_sw"] != '0'
    pedal_fx_type = pedal_fx_dict[params['pdlfx_type']]
    noise = int(params['ns_thresh'])

    print_effects_chain(indent, noise, params, pedal_fx, pedal_fx_type)

    # print(yaml.dump(params, allow_unicode=True, default_flow_style=False))
    print("")


def control_string(params):
    ctl = "CTL "
    if params["ctl_mode"] == "1":
        ctl += "(TOGGLE): "
    else:
        ctl += "(MOMENTARY): "
    controls = ['PEDAL FX', 'REVERB', 'EQ/FX2', 'PREAMP', 'DELAY', 'MOD', 'OD/DS',
                'COMP/FX1']
    bitmap = list(f'{int(params["ctl_target"]):08b}')
    active_controls = [c for b, c in zip(bitmap, controls) if b == '1']
    ctl_str = f"{ctl}{', '.join(active_controls)}"
    return ctl_str


def print_effects_chain(indent, noise, params, pedal_fx, pedal_fx_type):
    chain = "IN -> "
    if pedal_fx: chain += f"PEDAL FX ({pedal_fx_type}) -> "
    if params["comp_sw"] != '0':
        chain += f"COMP/FX1 ({comp_fx1_dict[params['comp_type']]}) -> "
    if params["odds_sw"] != '0':
        chain += f"OD/DS ({od_ds_dict[params['odds_type']]}) -> "
    if params["amp_sw"] != '0':
        chain += f"PREAMP  ({preamp_dict[params['amp_type']]})-> "
    if noise > 0:
        chain += f"NS ({noise}) -> "
    if params["pdlfx_sw"] == '0':
        chain += f"PEDAL VOL ({pedal_fx_dict[params['pdlfx_type']]}) -> "
    if params["mod_sw"] != '0':
        chain += f"MOD ({mod_dict[params['mod_type']]}) ->  "
    if params["fx2_sw"] != '0':
        chain += f"EQ/FX2 ({eq_fx2_dict[params['fx2_type']]}) -> "
    if params["dly_sw"] != '0':
        chain += f"DELAY ({delay_dict[params['dly_type']]}) -> "
    if params["rev_sw"] != '0':
        chain += f"REVERB ({reverb_dict[params['rev_type']]}) -> "
    chain += f"OUT"
    pad = indent * 2
    print(f"{pad}{chain}")


if __name__ == "__main__":
    main()
