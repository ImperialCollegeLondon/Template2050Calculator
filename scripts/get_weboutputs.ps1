$ErrorActionPreference = "Stop"
$path = Resolve-Path $args[0]

docker run --pull always --rm -it -v ${path}:/input.xlsx -v ${pwd}:/work --workdir /work ghcr.io/imperialcollegelondon/calc2050_get_weboutputs:latest python /get_weboutputs.py /input.xlsx
