#!/bin/bash

echo "Testing on Magnetites_DandP"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Magnetites/Magnetites_DandP.csv

echo "Testing on Other_oxides_ASD_main"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Oxides/Other_oxides_ASD_main.csv

echo "Testing on Sulfates_RELAB_plus_Nicolet2"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_plus_Nicolet2.csv

echo "Testing on Sulfates_Crowley_spectra2"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_Crowley_spectra2.csv

echo "Testing on Sulfates_ASD"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_ASD.csv
