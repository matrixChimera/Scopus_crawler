# _*_ coding:utf-8 _*_
# Developer: https://github.com/matrixChimera
# Time: 2020/4/20
# File name: merge_ris.py
# IDE: PyCharm
"""
Merge .ris files in the articles/citingArticles folder into one file.

"""

# ★★★Please define the folder：
def merge_results(folder='articles'):
    """
    Merge .ris files in the articles/citingArticles folder into one file.

    Args:
        folder (str): 'articles' (default) or 'citingArticles', defines the folder including .ris files to merge.

    Returns:
        A file named by the minimal year to the maximal,
            including all information in .ris files in the articles/citingArticles folder

    """

    import os
    # Define the folder including .ris files to merge:
    current_path = os.getcwd()
    folder_name = os.path.join(current_path, 'Output', folder)

    # region Extract all files (except .DS_Store of Mac) in the folder
    file_list = []
    for file in os.listdir(folder_name):
        if file != '.DS_Store':
            file_list.append(file)
    # endregion

    # Define the name of output:
    year_list = [int(year[0:-4]) for year in file_list]
    combination_name = os.path.join(folder_name, '{}-{}.ris'.format(min(year_list), max(year_list)))

    # Iteration: append each individual .ris file to the output
    for file in file_list:
        with open(os.path.join(folder_name, file)) as f_read:
            file_content = f_read.read()
        with open(combination_name, 'a') as f_write:
            f_write.write(file_content)


if __name__ == '__main__':
    merge_results(folder='articles')



