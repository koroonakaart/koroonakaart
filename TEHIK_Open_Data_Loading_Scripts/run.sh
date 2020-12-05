declare -A output_array
output_array[git_output]=$(git -C .. pull origin 2>&1 > /dev/null)
output_array[pip_output]=$(pip3 install -r requirements.txt 2>&1 > /dev/null)
output_array[deaths_scraper]=$(python3 deaths_scraper.py 2>&1 > /dev/null)
output_array[main_python]=$(python3 main.py 2>&1 > /dev/null)
cd ../koroonakaart
output_array[npm]=$(npm run build 2>&1 > /dev/null)
cd - 2>&1 > /dev/null

# Output errors
echo "git_output: ${output_array[git_output]}
pip_output: ${output_array[pip_output]}
deaths_scraper: ${output_array[deaths_scraper]}
npm: ${output_array[npm]}
main_python: ${output_array[main_python]}"
