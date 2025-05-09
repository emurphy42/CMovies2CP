# CMovies2CP

## Usage

1. Download the latest release, if not present or not up to date, clone this repository with `git clone https://github.com/emurphy42/CMovies2CP.git --recurse-submodules`.
2. Install Python, 3.13 was used for the development of this.
3. Depending on your platform and your Python install, install requirements using:
    - `pip install -r requirements.txt`
    - `py -m pip install -r requirements.txt`
    - `python3 -m pip install -r requirements.txt`
    - `python -m pip install -r requirements.txt`
4. Place your Custom Movies mod in CM2CP's folder so that its manifest is `<CM2CP Folder>/<name of mod>/manifest.json`
5. Rename the mod to `input`, so that the manifest is `<CM2CP Folder>/input/manifest.json`
6. Run `main.py`, preferably through a terminal using one of the following commands:
   - `py main.py`
   - `python3 main.py`
   - `python main.py`
7. Find the converted mod in `output/`
   - Only converts manifest.json and content.json
   - Manually copy other files from `input/` to `output/`
