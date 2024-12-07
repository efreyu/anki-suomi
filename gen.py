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
    {
        "name": "generate_verbs",
        "call": gen_verbs.gen_verbs,
        "expected": True,
        "args": ['db/verbs1.json', 'Finnish Verbtype 1', 'Finnish_Verbs_1.apkg'],
    }
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
