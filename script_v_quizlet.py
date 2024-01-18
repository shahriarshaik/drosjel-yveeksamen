import os
from bs4 import BeautifulSoup

def process_html_file(file_name ):

    # Get the base name of the file without the extension
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    output_file_name = os.path.join('quizlet fil', "output" + '.txt')

    # Open the HTML file and read its content
    with open(file_name, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all divs with class 'course_quiz_element'
    quiz_elements = soup.find_all('div', class_='course_quiz_element')

    # Open the output file
    with open(output_file_name, 'a', encoding='utf-8') as output_file:
        # Loop through all found quiz elements
        for quiz_element in quiz_elements:
            # Parse the required elements within each quiz element
            qnum_element = quiz_element.find('span', class_='course_quiz_qnum')
            qnum = ' '.join(qnum_element.text.split()) if qnum_element else 'Not found'
            title_element = quiz_element.find('span', class_='quiz_element_title')
            title = ' '.join(title_element.text.split()) if title_element else 'Not found'
            options = [' '.join(fg.text.split()) for fg in quiz_element.find_all('div', class_='form-group')]
            #options = '\n'.join(options)  # Join options with newline
            right_answer_element = quiz_element.find('input', {'name': lambda x: x and x.startswith('right_')})
            right_answer = right_answer_element.get('value') if right_answer_element else 'Not found'
            explanation_element = quiz_element.find('div', class_='explanationText')
            explanation = ' '.join(explanation_element.text.split()) if explanation_element else 'Not found'
            # Write the parsed data to the output file
            output_file.write(f'{title}\t')

            try:
                # Find the correct option
                correct_option = options[int(right_answer) - 1][3:]

                # Write only the correct option to the file
                output_file.write(f'{correct_option}                                                    ')
            except Exception as e:
                print(f'Error in file {file_name} at question number {qnum}: {str(e)}')

            # No need to write the explanation
            output_file.write(f'{explanation}\n')

def process_all_html_files_in_folder(folder_path):
    # Get a list of all files in the directory
    all_files = os.listdir(folder_path)

    # Filter the list for non-empty HTML files
    html_files = [file for file in all_files if file.endswith('.html') and os.path.getsize(os.path.join(folder_path, file)) > 0]

    filecounter = 0
    # Process all non-empty HTML files
    for html_file in html_files:
        filecounter += 1
        print(f'Processing file {html_file}')
        process_html_file(os.path.join(folder_path, html_file))
    print(f'Processed {filecounter} files')

# Call the function with the folder path
process_all_html_files_in_folder('html filer')