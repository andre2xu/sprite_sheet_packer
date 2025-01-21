# Sprite Sheet Packer &nbsp;![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=yellow) ![Qt](https://img.shields.io/badge/Qt-white?style=flat&logo=qt)

A free software for packing your sprites. It also supports (colored) PNG gridded sprite sheets as input.
<br><br>

Works on the following operating systems:
- Windows
- Ubuntu
- Debian


<br><small>*P.S I cannot test it on a Mac but it should still work.*</small>

<br>

## Installation
Clone the repo to your desired folder.
```
git clone https://github.com/andre2xu/sprite_sheet_packer.git

cd sprite_sheet_packer
```

<br>Create a Python virtual environment and activate it.

```
python -m venv venv

./venv/Scripts/activate  # Windows

source ./venv/bin/activate  # Linux
```

<br>Install the dependencies in the virtual environment.

```
pip install -r requirements.txt
```

<br>Run PyInstaller to create the executable. It will be inside a folder called 'dist'.

```
pyinstaller main_single_file.spec
```