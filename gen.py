import subprocess
import sys


# Function to install a package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# List of required packages
required_packages = ["genanki", "gtts", "requests"]

# Install missing packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing missing package: {package}")
        install_package(package)

import generators.verbs as gen_verbs
import generators.numbers as gen_numbers
import generators.dialogs as gen_dialogs

generators = [
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs1.json', 'Finnish Verbtype 1', 'Finnish_Verbs_1.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs2.json', 'Finnish Verbtype 2', 'Finnish_Verbs_2.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs3.json', 'Finnish Verbtype 3', 'Finnish_Verbs_3.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs4.json', 'Finnish Verbtype 4', 'Finnish_Verbs_4.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs5.json', 'Finnish Verbtype 5', 'Finnish_Verbs_5.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs6.json', 'Finnish Verbtype 6', 'Finnish_Verbs_6.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs7.json', 'Finnish Verbtype 7', 'Finnish_Verbs_7.apkg']},
    #
    # {"name": "numbers", "call": gen_numbers.gen_numbers, "expected": True, "args": ['db/numbers/numbers1.json', 'Finnish Numbers 101', 'Finnish_Numbers_1.apkg']},

    {"name": "dialogs", "call": gen_dialogs.gen_dialogs, "expected": True, "args": ['db/27-dialogue/dialog1.json', 'Finnish::Dialogs27::Olga', 'Finnish_Dialogs27_Olga.apkg']},
    # {"name": "dialogs", "call": gen_dialogs.gen_dialogs, "expected": True, "args": ['db/27-dialogue/dialog2.json', 'Finnish::Dialogs27::Alex', 'Finnish_Dialogs27_Alex.apkg']},
    # {"name": "dialogs", "call": gen_dialogs.gen_dialogs, "expected": True, "args": ['db/27-dialogue/dialog2.json', 'Finnish::Dialogs27::Pedro', 'Finnish_Dialogs27_Pedro.apkg']},
]

def main():
    runners_succeed = True
    failed_runners = []
    for generator in generators:
        print(f"Running generator: {generator['name']}")
        result = generator["call"](*generator["args"])
        if result != generator["expected"]:
            runners_succeed = False
            print(f"Generator {generator['name']} failed: expected {generator['expected']}, got {result}")
            failed_runners.append(generator["name"])

    if not runners_succeed:
        print("Some generators failed!")
        for test in failed_runners:
            print(f"  - {test}")
        sys.exit(1)
    else:
        print("All data generated")
        sys.exit(0)

if __name__ == '__main__':
    main()
    sys.exit(0)