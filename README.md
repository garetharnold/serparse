# serparse.py

This script processes JSON files from Serper.dev Playground and outputs the combined data into different formats while filtering out specific TLDs and domains/strings, and removing duplicates.

I made it for friends who want to use the Playground and get data quickly, without having to boot up the API.

## Requirements

- Python 3
- pandas

## Installation

1. Clone the repository:

   ```git clone https://github.com/garetharnold/serparse.git```
   
   ```cd serparse```

2. Install the required packages:
   
   ```pip3 install pandas```

3. (OPTIONAL) Download the `tlds.json` file from the following URL and place it in the same directory as `serparse.py`:

   https://github.com/garetharnold/email-tld-blocklist

4. You can create your own `tlds.json` file for TLD filtering:

   ```json
   {
     "blocked_tlds": [
       {
         "tld": ".xyz",
         "description": "Commonly associated with spam and low-quality emails."
       },
       {
         "tld": ".top",
         "description": "Commonly used by spammers."
       },
       {
         "tld": ".win",
         "description": "Frequently used for spam and fraudulent activities."
       },
       {
         "tld": ".vip",
         "description": "Known for a high volume of spam."
       },
       {
         "tld": ".click",
         "description": "Often used in phishing and spam emails."
       }
     ]
   }
   ```

5. You can create your own `blacklist.json` file for domain or string filtering:

```json
   {
     "blocked_domains": [
       "amazon.com",
       "ebay.com",
       "example.com",
       "string",
       "news",
       "wikipedia"
     ]
   }
```

## Usage

To run the script:

```python3 serparse.py -i filename1.json filename2.json```

Replace `filename1.json` and `filename2.json` with your actual JSON files. The output will be in CSV format.

### Output Formats

- **Default**: JSON
- **CSV**: `-o csv`
- **URL CSV**: `-o urls`

### Example

```python3 serparse.py -i input1.json input2.json -o csv```

This will process the input files, filter out unwanted TLDs and domains/strings, remove duplicates, and save the output in CSV format with a timestamped filename.

## Functions of the Code

- **Input Files**: The script accepts multiple JSON input files specified with the `-i` or `--input` option.
- **Output Format**: The output format can be specified with the `-o` or `--output` option. Supported formats are `csv`, `urls`, and `json` (default).
- **Filtering**: The script filters out entries based on TLDs specified in `tlds.json` and domains/strings specified in `blacklist.json`.
- **Duplicate Removal**: Duplicates are removed based on the domain.
- **Logging**: The script generates a log file that records which entries were removed due to duplicates or filtering.