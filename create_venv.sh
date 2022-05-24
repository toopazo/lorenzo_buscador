# Remove any previous venv
rm -r venv

# Install virtualenv
python_ver=$(./create_venv.py --pver); ${python_ver} -m venv venv
# python3.7 -m venv venv
# python3.8 -m venv venv
# python3.9 -m venv venv

# Activate venv
source venv/bin/activate

# Install libraries
pip install scrapy
pip install extruct
pip install jsonlines
pip install wget
pip install PyPDF2
pip install bs4
pip install requests
