# HtmlToTxt
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/workink/TextPlusImage/blob/master/LICENSE)

A tool to extract html contents to txt files is given in this repository. Users need to give `input_csv`, `output_dir` as 
the input. The output is a collection of txt files saved in the `output_dir`, and a csv file mapping each original url to each txt file.

## Installing
Activate the virtualenv and install packages using `requirements.txt`.
```bash
pip install -r requirements.txt
```

## Usage
Pass `--helpshort` to see help on flags.
```
python html_to_txt.py --helpshort

       USAGE: html_to_txt.py [flags]
flags:

html_to_txt.py:
  --input_csv: The input csv file containing webpage urls
  --output_dir: The directory for output

Try --helpfull to get a list of all flags.
```

Sample usage.
```
python html_to_txt.py --input_csv="data/urls.csv" --output_dir="output_dir"
```
