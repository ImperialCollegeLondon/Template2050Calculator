# Template2050Calculator
A template for automatically converting [2050 Calculator](https://www.imperial.ac.uk/2050-calculator) models into web applications. The layout is based off the [UK Mackay Carbon Calculator](https://mackaycarboncalculator.beis.gov.uk/overview/emissions-and-primary-energy-consumption) and is a simple design that can be customised further. It uses [Anvil](https://anvil.works) to create the web app using Python.

## Web App Setup Process

To go from a functioning excel model to a web app requires 2 main steps: convert the model into an executable, run and host the web app. There are a few parts to each step, detailed below.

### 1. Convert the model to an executable.
#### Ensure excel model has required named ranges:
In order for the spreadsheet to be converted into a model, it requires certain named ranges to be added to the template:

 - `outputs_summary_table` - covers the summary table (including the column headers) in the `WebOutputs` sheet.
 - Inputs - `input.lever.ambition`, `input.lever.start`, `input.lever.end`
 - Outputs - `output.lever.names`, plus whatever outputs (graphs) are desired and detailed in the summary table. Note: the Mackay Calculator has a typo in the summary table, change the contents of cell `WebOutputs!G771` to `output.land.map.numberunits`

#### Convert spreadsheet to executable
Clone the [calc2050_spreadsheet_converter](https://github.com/ImperialCollegeLondon/calc2050_spreadsheet_converter) with:
```bash
git clone https://github.com/ImperialCollegeLondon/calc2050_spreadsheet_converter.git
```

Make sure that you have [Docker](https://www.docker.com/get-started) installed. If using Docker Desktop, you might have to increase the memory limit to 6gb for the Mackay Calculator. (See the advanced section on [this page](https://docs.docker.com/docker-for-mac/))

If running on a Mac, you might need to install the Unix command `realpath`. It can be installed with Homebrew by installing [coreutils](https://formulae.brew.sh/formula/coreutils).

Run the script to process the spreadsheet with:
```bash
bash process_spreadsheet.sh <path-to-excel-model>
```

This will take a few hours to finish and the results will be found in a folder called `model`.

### 2. Running and Hosting the Web App
There are two main options for running and hosting the web application: locally and through Azure.

#### Local Hosting
Copy the two files `interface.py` and `_interface2050.cpython-39-x86_64-linux-gnu.so` into the `server_code` directory of this `Template2050Calculator` repository.

Make sure you have Docker installed and are inside the top directory of this repository.

Build the docker image with:
```bash
docker-compose build
```

Run the server with:
```
docker-compose up
```

The server can be stopped with `Ctrl+C` or `docker-compose down`.

The Web App will be available in your browser at `localhost:3030`.

#### Azure Hosted Web App

More details to come. Much the same as local hosting, but involves uploading the compiled model to Azure and setting up some configuration and a domain name in Azure.

## Customising the Web App

This template is fit for use as a fully functioning Web App out of the box, however is intended to be taken and customised. There are two main ways to edit what appears in your calculator:
1. Editing the metadata in the spreadsheet.
2. Editing the Anvil app itself.

The spreadsheet metadata includes:
 - WebOutputs Summary Table: graph title, postition, tab, subtab, axis unit, named range
 - Example Pathways
 - Output Lever details: names, groups, tooltips

The Anvil App can be edited by using the online Anvil editor. This will require making a free Anvil account and creating your own project then force-pushing this repo to that project. Note: you will need to create a `master` branch and push that to Anvil.
