import subprocess
import sys


# Function to install a package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# List of required packages
required_packages = ["genanki", "gtts", "pydub", "requests"]

# Install missing packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing missing package: {package}")
        install_package(package)

import generators.verbs as gen_verbs

generators = [
    {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs1.json', 'Finnish Verbtype 1', 'Finnish_Verbs_1.apkg']},
    {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs2.json', 'Finnish Verbtype 2', 'Finnish_Verbs_2.apkg']},
    {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs3.json', 'Finnish Verbtype 3', 'Finnish_Verbs_3.apkg']},
    {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs4.json', 'Finnish Verbtype 4', 'Finnish_Verbs_4.apkg']},
    {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs5.json', 'Finnish Verbtype 5', 'Finnish_Verbs_5.apkg']},
    {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs6.json', 'Finnish Verbtype 6', 'Finnish_Verbs_6.apkg']},
    {"name": "generate_verbs", "call": gen_verbs.gen_verbs, "expected": True, "args": ['db/general_verbs/verbs7.json', 'Finnish Verbtype 7', 'Finnish_Verbs_7.apkg']}
]

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
