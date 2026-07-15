# PSX CHD Renamer

A utility tool for renaming PlayStation 1 (PSX) CHD (MAME Compressed Hunks of Data) and ISO files with proper naming conventions and metadata extraction.

## Features

- **Automatic Renaming**: Renames PSX CHD/ISO files based on standardized naming conventions
- **Metadata Extraction**: Extracts game information from CHD/ISO files
- **Batch Processing**: Process multiple CHD/ISO files at once
- **Safe Operations**: Includes validation and backup options
- **Flexible Naming**: Support for custom naming patterns

## Prerequisites
### Required tools
- First make sure that [uv](https://docs.astral.sh/uv/) is installed on your computer and can be called from your shell. It is the recommended tool for this project.
- Also, make sure that `chdman` is also installed and can be called from your shell. You can find a comprehensive tutorial on [the chdman Recalbox Wiki](https://wiki.recalbox.com/en/tutorials/utilities/rom-conversion/chdman)
### Datasource
The script gets the correct names of the games from two sources:
- Redump XML file for PS1: the bundled [assets/redump-psx.dat](assets/redump-psx.dat) file, updated on 2026-06-15. If you need a more recent version, go to [redump official website](http://redump.org/downloads/) and download a new one.
- PSX data center: the cached lookup data in [assets/psxdatacenter_cache.json](assets/psxdatacenter_cache.json), last updated on 2026-07-14. To refresh it, remove the file and run the tool again.

Redump will be the prime choice; PSX data center will only be queried if a match is not found on Redump.

## Installation
- Clone the project and open a shell on the extracted directory
```bash
git clone https://github.com/yourusername/psx-chd-renamer_revamp.git
cd psx-chd-renamer_revamp
```

- Install the project and dev dependencies with uv:
```bash
uv sync --extra dev
```
- uv will create and manage the project environment automatically for you, so you do not need to activate anything manually.

## Usage
Once you are in the project directory, just run
```bash
uv run main.py [options][path]
```

### Options
- `--chdman`: Specify the location of the chdman binary. You can also modify the CHDMAN_PATH variable in the main file to change it. By default, it is assumed that is already installed in your PATH, so you do not need to provide it
- `--base-dir`: Directory that contains the CHD/ISO games to be renamed, you need to provide the path with quotes or just change the BASE_DIR variable in the main file.
- `--dry-run`: Preview changes without renaming. Just preview the changes without renaming it. It's the behavior by default
- `--no-dry-run`: Perform the actual renaming. For the files renaming to take place, you need to specify this option.

### Examples

```bash
# Rename files in current directory
uv run main.py --base-dir .

# Dry run to see what would change
uv run main.py --dry-run --base-dir .
# or
uv run main.py .

# Process subdirectories recursively
uv run main.py --no-dry-run --base-dir '/path/to/games' 
```

## Requirements

- Python 3.12
- uv 0.11+
- Dependencies listed in `pyproject.toml`

## File Naming Convention

Files are renamed following this pattern:
```
[PS1] Game Name (extra metadata) (disc number) [region_code][languages if specified on sources] [serial id]
```

Examples: 
- `[PS1] Rival Schools - United by Fate (Arcade Disc) (Disc 1) [US] [SLUS-00681].chd`
- `[PS1] WRC - FIA World Rally Championship Arcade [EU][E,F,G,S,I,N,P,Sw,No,Da,Fi] [SCES-03907].chd`

## Contributing

Contributions are welcome! Please submit issues and pull requests.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Disclaimer

- This tool is for personal use only. Ensure you have legal rights to any CHD or ISO files you process.

## Data Credits and Attribution

This repository bundles metadata parsing tables derived from community database archives. 

1. **Redump Data:** Game data are partly sourced from Redump.org. This data is utilized strictly for non-commercial game preservation and validation purposes under fair-use principles.
2. **PSXDataCenter Data:** Game data are partly sourced directly from [PSXDataCenter](https://psxdatacenter.com). In accordance with their terms, this data is distributed freely with full credit attributed back to the original maintainers.

This project is a non-commercial, personal tool. All rights to the underlying video game metadata belong to their respective community curators.