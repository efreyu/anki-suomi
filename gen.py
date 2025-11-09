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
import generators.verbs_cloze as gen_cloze_verbs

generators = [
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs1.json', 'Finnish::Verbtypes::Verbtype1', 'Finnish_Verbs_1.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs2.json', 'Finnish::Verbtypes::Verbtype2', 'Finnish_Verbs_2.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs3.json', 'Finnish::Verbtypes::Verbtype3', 'Finnish_Verbs_3.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs4.json', 'Finnish::Verbtypes::Verbtype4', 'Finnish_Verbs_4.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs5.json', 'Finnish::Verbtypes::Verbtype5', 'Finnish_Verbs_5.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs6.json', 'Finnish::Verbtypes::Verbtype6', 'Finnish_Verbs_6.apkg']},
    # {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs7.json', 'Finnish::Verbtypes::Verbtype7', 'Finnish_Verbs_7.apkg']},
    {"name": "numbers", "call": gen_numbers.gen_numbers, "expected": True, "args": ['db/numbers/numbers1.json', 'Suomi::Numerot::Kirjakielinen-1::normaali', 'Suomi_Kirjakielinen_1n.apkg', 'regular', 445256733, 902348237123]},
    {"name": "numbers", "call": gen_numbers.gen_numbers, "expected": True, "args": ['db/numbers/numbers1.json', 'Suomi::Numerot::Kirjakielinen-1::käänteinen', 'Suomi_Kirjakielinen_1k.apkg', 'reverse', 445256734, 902348237223]},
    # {"name": "dialogs", "call": gen_dialogs.gen_dialogs, "expected": True, "args": ['db/lessons/27-lesson/dialog1.json', 'Finnish::Lessons::Lesson27::Olga', 'Finnish_Lessons27_Olga.apkg']},
    # {"name": "dialogs", "call": gen_dialogs.gen_dialogs, "expected": True, "args": ['db/lessons/27-lesson/dialog2.json', 'Finnish::Lessons::Lesson27::Alex', 'Finnish_Lessons27_Alex.apkg']},
    # {"name": "dialogs", "call": gen_dialogs.gen_dialogs, "expected": True, "args": ['db/lessons/27-lesson/dialog3.json', 'Finnish::Lessons::Lesson27::Pedro', 'Finnish_Lessons27_Pedro.apkg']},
    # {"name": "cloze_verbs", "call": gen_cloze_verbs.gen_verbs_cloze, "expected": True, "args": [987654321, 'db/verbs_cloze/verbs1/*.json', 'Finnish::Verbtypes Cloze::Verbtype1', 'Finnish_Verbs_Cloze_1.apkg']},
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