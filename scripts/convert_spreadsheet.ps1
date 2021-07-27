$ErrorActionPreference = "Stop"
$path = Resolve-Path $args[0]

docker run --pull always --rm -it -v ${path}:/opt/excel_to_code/input.xlsx:ro -v ${pwd}:/opt/excel_to_code/work/ ghcr.io/imperialcollegelondon/calc2050_excel_to_code:main bash ./run.sh
Copy-Item -Path .\model\_interface2050.cpython-39-x86_64-linux-gnu.so -Destination .\server_code\
Copy-Item -Path .\model\interface2050.py -Destination .\server_code\
