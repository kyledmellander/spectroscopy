#!/bin/bash

echo "Testing on Magnetites"
echo "1"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Magnetites/Magnetites_DandP.csv
echo "2"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Magnetites/Magnetites_ASD.csv
echo "3"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Magnetites/Magnetites_Maya.csv
echo "4"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Magnetites/Magnetites_OceanOptics.csv
echo "5"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Magnetites/Magnetites_RELAB_plus_Nicolet.csv

echo "Testing on Other_oxides"
echo "6"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Oxides/Other_oxides_ASD_main.csv
echo "7"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Oxides/Other_oxides_ASD_hematite.csv
echo "8"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Oxides/Other_oxides_ASD_other.csv
echo "9"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Oxides/Other_oxides_DandP.csv
echo "10"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Oxides/Other_oxides_OceanOptics.csv
echo "11"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Oxides/Other_oxides_RELAB_plus_Nic.csv

echo "Testing on Sulfates_"
echo "12"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_ASD.csv
echo "13"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_ASD2.csv
echo "14"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_Crowley_spectra.csv
echo "15"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_DandP.csv
echo "16"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_OceanOptics.csv
echo "17"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_archive.csv
echo "18"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_archive2.csv
echo "19"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_archive3.csv
echo "20"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_archive4.csv
echo "21"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_archive5.csv
echo "22"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_archive6.csv
echo "23"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_plus_Nicolet.csv
echo "24"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_plus_Nicolet2.csv
echo "25"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_RELAB_plus_Nicolet3.csv
echo "26"
python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_Crowley_spectra2.csv

#echo "Testing on Sulfates_Crowley_spectra2"
#python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_Crowley_spectra2.csv

#echo "Testing on Sulfates_ASD"
#python src/static_in_pro/our_static/py/dataParser.py ~/cs49x/Samples/Sulfates/Sulfates_ASD.csv
