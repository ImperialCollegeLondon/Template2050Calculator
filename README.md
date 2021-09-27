# Template2050Calculator
A template for automatically converting [2050 Calculator](https://www.imperial.ac.uk/2050-calculator) models into web applications. The layout is based off the [UK Mackay Carbon Calculator](https://mackaycarboncalculator.beis.gov.uk/overview/emissions-and-primary-energy-consumption) and is a simple design that can be customised further. It uses [Anvil](https://anvil.works) to create the web app using Python.

## Web App Setup Process
To go from a functioning excel model to a web app requires 2 main steps before it is ready to deploy: convert the model into an executable, then test the web app locally and customise as desired. There are a few parts to each step, detailed below.

### Getting Started

We strongly recommend forking or importing a copy of the Template2050Calculator repository on GitHub. The code can then be cloned to a local machine for development. The following dependencies must be installed for the conversion process and testing/customisation of the web app:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

If working on Windows or Mac there is a small amount of extra configuration required for Docker. On these platforms Docker has a default memory usage cap of 2 Gb. This is likely to be exceeded; for reference, conversion of the Mackay Calculator requires around 4 Gb of memory. See the advanced section on [this page](https://docs.docker.com/docker-for-mac/) to increase the memory usage cap.

### 1) Convert Excel Model

#### a) Prepare Excel Model

Converting the spreadsheet successfully requires certain named ranges to be present. The named ranges specified contain the necessary data and metadata for the conversion process. The following named ranges must be present as they are in the Mackay Calculator spreadsheet.

 - Inputs - `input.lever.ambition`, `input.lever.start`, `input.lever.end`.
 - Outputs - `output.lever.names`, `output.lever.descriptions` and `output.lever.example.ambition`, plus whatever outputs (graphs) are desired and detailed in the summary table. Note: the Mackay Calculator has a typo in the summary table, change the contents of cell `WebOutputs!G771` to `output.land.map.numberunits`.

The following named ranges must be present in addition to those that are in the Mackay Calculator spreadsheet.
 - `outputs_summary_table` - covers the summary table (titled "Outputs to Webtool Summary" in the Mackay Calculator) in the `WebOutputs` sheet. This should include the column headers as the first row. For instance in the Mackay Calculator this would cover `WebOutputs!C31:N68`.
 - A series of ranges, one for each group of levers, named according to the convention `output.lever.group?` where `?` is a number. These ranges must be two columns wide with the name of a lever group in the top-left cell and names of each individual lever in the right-hand column. For instance, in the Mackay Calculator `output.lever.group1` would cover `Control!B70:C81`, `output.lever.group2` would cover `Control!B82:C89` and so on.

The following should be checked carefully:
 - Contents of the `weboutputs_summary_table` range:
   - For the "Webtool Page" column, entries of "Warnings" will mark an output as a warning icon, all other entries will be used as the name of the tab for the output.
   - For the "Webtool Tab" column, entries must be "Not required" for Warnings and desired sub-tab name for all other outputs.
   - For the "Position column", entries for Warnings should be numeric indicating order of appearance, but for other outputs must be one of "Top", "Bottom" or "Page".
   - For the "Graph Type" column, entries must be one of "Stacked Area with overlying Line(s)", "Line", "Sankey/Flow", "Map" or "Icon"
 - Ranges for individual outputs should cover data series names in the first column and all data up to 2100.

#### b) Run Conversion

On Mac/Linux run:
```bash
bash scripts/convert_spreadsheet.sh path/to/spreadsheet
```

On Windows (Powershell) run:
```
.\scripts\convert_spreadsheet.ps1 path\to\spreadsheet
```

This will take a few hours to finish and consume several Gb of memory. Once completed there should be two new files (`_interface2050.cpython-39-x86_64-linux-gnu.so`) and `interface.py` in the `server_code` directory.

### 2) Run App

#### a) Extract Metadata

The above conversion process focuses on extracting the details of the computational model however there is additional metadata in the spreadsheet that is needed by the web app. Getting this metadata is much faster than the conversion process so wherever possible static data from the spreadsheet is extract in this step. If you make changes to data in the spreadsheet e.g. change a lever description you will need to re-run this step to update the web app. In most cases, only if changes are made to the computational aspects of the model will you need to re-run the conversion process.

On Mac/Linux run:
```bash
bash scripts/get_weboutputs.sh path/to/spreadsheet
```

On Windows (Powershell) run:
```
.\scripts\get_weboutputs.ps1 path\to\spreadsheet
```

#### b) Update Configuration File

Several aspects of the site can be configured via the included `app_config.yml` file. This file follows the YAML format and allows access to configuration settings that are expected to change between models from different countries e.g. the longitude and latitude to use for map outputs. Each setting in the file is commented and must be adjusted to match the new model.

#### c) Test App

To run a test server locally run:
```
docker-compose up
```

Then open `localhost:3030` in a web browser. All being well the app should load and you'll be able to try it out. Make sure to check that each output is behaving as expected.

The server can be stopped with `Ctrl+C` or `docker-compose down`.

#### d) Customise

You can now start changing the appearance and behaviour of the web app as desired. See the [Anvil documentation](https://anvil.works/docs/overview) to get familiar with the framework. Any changes made whilst the server is running should be automatically picked up when the browser page is refreshed.

This template is fit for use as a fully functioning Web App out of the box, however is intended to be taken and customised. There are two main ways to edit what appears in your calculator:
1. Editing the metadata in the spreadsheet.
2. Editing the Anvil app itself.

The spreadsheet metadata includes:
 - WebOutputs Summary Table: graph title, postition, tab, subtab, axis unit, named range
 - Example Pathways
 - Output Lever details: names, groups, tooltips

The Anvil App can be edited by using the online Anvil editor. This will require making a free Anvil account and creating your own project then force-pushing this repo to that project.

Once you have created a new app in Anvil named `Template2050Calculator`, add it as a remote named `anvil` to this repo with:
```bash
git remote add anvil <ssh-link>
```

Where `<ssh-link>` can be found under `Settings->Share App->Clone with Git`. It is the url section (it should begin with `ssh` and end with `.git`).

Now that you have the remote you will need to create a `master` branch and push that to Anvil:
```bash
git checkout -b master
git push -u anvil master
```

Now return to Anvil and refresh the page. The editor should be updated with this repo! You can now begin graphically editing the layout of the graph. Anvil has very detailed [documentation on the Anvil Editor](https://anvil.works/docs/editor).

### Deployment

The Dockerfile in the repository can be used to build a Docker image suitable for deploying in a range of hosting services. Whilst the Anvil web server is suitable for direct production usage we recommend combining it with a suitable reverse proxy. A docker image can be built for example with:
```
docker build -t calc2050_site:latest .
```

In production the image can be run using some variation of the below.
```
docker run calc2050_site:latest anvil-app-server --data-dir /anvil-data --app /apps/Template2050Calculator --disable-tls --port 3030 --origin https://calc2050template.azurewebsites.net/
```

The value for `--origin` should be substituted with the correct domain under which the site will be hosted. The `--disable-tls` flag is used on the assumption that the container will be placed behind a suitable reverse proxy that will handle TLS. For more information about available options see the `anvil-app-server` [README](https://github.com/anvil-works/anvil-runtime#advanced-configuration).

Upon request, deployment can be carried out on Azure Cloud under the resources of the 2050 Calculators project. 
