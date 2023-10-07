# Slotheader HTTP headers saver
The Slotheader HTTP headers saver is a Python tool designed to retrieve and save HTTP headers from given URLs. It can be useful for mass analyzing and storing response headers from web services and websites. This tool supports both single-threaded and multi-threaded processing for handling multiple URLs efficiently.

## Usage

1. Make sure you have Python 3 installed on your system.

2. Download or clone the repository to your local machine.

3. Open a terminal and navigate to the directory containing the downloaded files.

4. Run the tool with the following command:

   ```bash
   python slotheader.py target [--save-dir SAVE_DIR] [--single-thread]
Replace target with the URL or filepath containing URLs.

Header files will be saved in the specified directory or the current directory.


## Adding to PATH

To use the tool globally, add it to your system's PATH:

1. Find the full directory path.

2. On Linux/macOS, edit ~/.bashrc or ~/.zshrc and add:

    ```bash
    export PATH="$PATH:/full/path/to/directory"
  On Windows, edit Environment Variables and add the path to the "Path" variable.

3. Restart the terminal and run the tool using `slotheader.py`. 
 
## License
This tool is open-source under the MIT License.

Created by Jordi Gerritsen
