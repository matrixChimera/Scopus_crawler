# _*_ coding:utf-8 _*_
# Developer: https://github.com/matrixChimera
# Time: 2020-04-20
# File name: advanced_query_articles.py
# IDE: PyCharm
"""
Crawl information (citation, bibliography, abstract, fund and other information) of papers searched by advanced query
    on Scopus (www.scopus.com) via Selenium.
Before executing this program, please define/modify parameters in settings.py.
Specially, this program subdivides YEARS into subyear(s), then combines your QUERY and a subyear repeatedly for advanced search,
    given that we can only manually download at most 2000 results per batch on Scopus.

"""

import os
import time
import re
from prettytable import PrettyTable

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import values that you should define before execution:
from settings import *


def log_in(access):
    """
    Log in Scopus via your institution (by your username, password, and institution name) or cookies of Scopus' URL.

    Args:
        access (str): 'institution' or 'cookies', defines the way you log in, respectively.

    Returns:
        Logged in or not. If you failed to log in, this program will be stopped.
    """
    try:
        if access == 'institution':
            # If you didn't give cookies of the URL with Scopus' access, please log in via institution

            # Show the current process:
            print('Logging in via your institution ...')

            # Go to the URL of getting access on Scopus for institution users:
            browser.get(
                'https://id.elsevier.com/as/authorization.oauth2?platSite=SC%2Fscopus&ui_locales=en_US&scope=openid+profile+email+els_auth_info+els_analytics_info+urn%3Acom%3Aelsevier%3Aidp%3Apolicy%3Aproduct%3Ainst_assoc&response_type=code&redirect_uri=https%3A%2F%2Fwww.scopus.com%2Fauthredirect.uri%3FtxGid%3Dbc6f0c0ea70010df705a26ab6916511f&state=checkAccessLogin&authType=SINGLE_SIGN_IN&prompt=login&client_id=SCOPUS')
            # Input, submit, and choose your institution:
            print('-- Inputting, submitting, and choosing your institution ...')
            institution_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#bdd-email')))
            institution_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#bdd-els-searchBtn')))
            institution_input.send_keys(INSTITUTION)
            institution_submit.click()
            institution_choice = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#bdd-institution-resultList > form:nth-child(1) > button')))
            institution_choice.click()
            login_scopus = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#bdd-elsPrimaryBtn')))
            login_scopus.click()

            # Redirect to the VPN of your institution. Input and submit your username and password:
            print(
                '-- Redicrecting to the VPN of your institution. Inputting and submitting your username and password ...')
            username_institution = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#username')))
            password_institution = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#password')))
            submit_institution = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#fm1 > table > tbody > tr:nth-child(4) > td > input[type=submit]')))
            username_institution.send_keys(USERNAME)
            password_institution.send_keys(PASSWORD)
            submit_institution.click()

            # Test whether you successfully logged in:
            print('-- Testing whether you successfully logged in ...')
            browser.get('https://www.scopus.com/search/form.uri?display=advanced')
            time.sleep(
                SLEEPTIME_LONG)  # Please lengthen this waiting time, when you can successfully log in manually but not via this program.
            judge = len(re.findall(r'advanced', browser.current_url))
            if judge > 0:
                print('-- Successfully logged in!')
            if judge == 0:
                print('-- Failed to log in.')
                os._exit(0)
        elif access == 'cookies':
            # If you gave cookies of the URL with Scopus' access, log in via cookies:

            # Show the current process:
            print('Logging in via cookies ...')

            # Go to the URL of advanced search on Scopus:
            browser.get('https://www.scopus.com/search/form.uri?display=advanced')

            # Add cookies to the website of Scopus:
            print('-- Adding cookies ...')
            for name, value in COOKIES.items():
                browser.add_cookie({
                    'name': name,
                    'value': value})

            # Test whether you successfully logged in:
            print('-- Testing whether you successfully logged in ...')
            # Go to the URL of advanced search on Scopus:
            browser.get('https://www.scopus.com/search/form.uri?display=advanced')
            time.sleep(
                SLEEPTIME_LONG)  # Please lengthen this waiting time, when your network can successfully log in manually but not via this program.
            judge = len(re.findall(r'advanced', browser.current_url))
            if judge > 0:
                print('-- Successfully logged in!')
            if judge == 0:
                print('-- Failed to log in.')
                os._exit(0)
        else:
            print('''Failed to log in. Please confirm information about logging in within settings.py''')
            os._exit(0)
    except TimeoutException:
        print('Try again ...')
        log_in(access)


def advanced_search():
    """
    Advanced search by the given QUERY and subyear. Extract the number of results searched.

    """
    try:
        # Show the current process:
        print('\nAdvanced searching by query in {} ...'.format(subyear))

        # Go to the URL of advanced search:
        # (It may sometimes take more than 20 seconds to step towards the next step)
        browser.get('https://www.scopus.com/search/form.uri?display=advanced')

        print('-- Inputting and submitting the QUERY (and the subyear) ...')
        # Find input box. Input query in the subyear:
        query_input_entry = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#SCAdvSearchInputBox')))
        query_input_entry.click()
        time.sleep(SLEEPTIME_SHORT)
        query_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#searchfield')))
        # Clear the input box:
        time.sleep(SLEEPTIME_SHORT)
        query_input.clear()
        # Input query:
        time.sleep(SLEEPTIME_SHORT)
        query_with_subyear = '{} AND PUBYEAR = {}'.format(QUERY, subyear)
        query_input.send_keys(query_with_subyear)
        # Find submit button. Submit query:
        query_submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#advSearch')))
        query_submit.click()
        # (It may sometimes take more than 20 seconds to step towards the next step)

        print('-- Extracting the number of results searched ...')
        # Show the number of results in the subyear:
        time.sleep(SLEEPTIME_MEDIUM)
        results_number = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#searchResFormId > div:nth-child(2) > div > header > h1 > span.resultsCount')))
        # Extracting text of element may sometimes be unsuccessful, thus extract repeatedly:
        time.sleep(SLEEPTIME_SHORT)
        results_number_text = results_number.text
        extract_count = 0
        while results_number_text == '':
            extract_count += 1
            results_number_text = browser.find_element_by_css_selector(
                '#searchResFormId > div:nth-child(2) > div > header > h1 > span.resultsCount').text
            if extract_count > 100:
                print('-- Failed to extract the number of results in {}.'.format(subyear))
                break
        # Delete the group separator (,)(千位分隔符):
        results_number_text = re.sub(r'(,?)', '', results_number_text)
        results_number_int = int(results_number_text)
        print('-- There are altogether {} papers to download.'.format(results_number_int))
        # Print alert when the number of results in the subyear is beyond the downloading limit per batch:
        if results_number_int > 2000:
            print('''!!!ALEART!!!
    The number of papers in {} is beyond the limit of 2000 per batch. Please subdivide the search for 【{}】.'''.format(
                subyear, subyear))
        # Extract the number of results for summary:
        summary_dict[str(subyear)].append(results_number_int)
    except:
        # Switch the value of fail_to_download to 1:
        global fail_to_download
        fail_to_download = 1


def select_all_results():
    """
    Select all results (more or less information about articles, depending on the export settings of your Scopus account) to export.
    (Please, in advance, manually login in via your institution (and your account),
        and set up your export settings via https://www.scopus.com/export/settings.uri?)

    """
    try:
        # Show the current process:
        print('\nSelecting all results to export ...')

        # Find and click selectAll button (via JavaScript and wait for several seconds, because .click() of Selenium may sometimes not work):
        time.sleep(SLEEPTIME_MEDIUM)
        if browser.find_element_by_css_selector('#mainResults-allPageCheckBox').get_attribute('checked') != 'checked':
            browser.execute_script('document.getElementById("mainResults-allPageCheckBox").click()')

        # Find and click export option button (wait for several seconds for that #export_results can be clicked):
        time.sleep(SLEEPTIME_SHORT)
        export_option_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#export_results')))
        export_option_button.click()

        print('-- Extracting the number of results to export ...')
        # Show the number of total papers to export:
        time.sleep(SLEEPTIME_SHORT)
        total_papers_export = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#selectedDocsForExport')))
        # Extracting text of element may sometimes be unsuccessful, thus extract repeatedly:
        time.sleep(SLEEPTIME_SHORT)
        total_papers_export_text = total_papers_export.text
        extract_count = 0
        while total_papers_export_text == '':
            extract_count += 1
            total_papers_export_text = browser.find_element_by_css_selector('#selectedDocsForExport').text
            if extract_count > 100:
                print('-- Failed to extract the number of total papers to export in {}.'.format(subyear))
                break
        if total_papers_export_text != '':
            print('--', total_papers_export_text)

        # Please, in advance, manually login in via your institution (and your account),
        # and set up your export settings via https://www.scopus.com/export/settings.uri?
        print('''-- You have selected the results' all information in ris format to export.
    (Please, in advance, manually log in and set up your export settings.)''')
    except:
        # Switch the value of fail_to_download to 1:
        global fail_to_download
        fail_to_download = 1


def download():
    """
    Export all results.

    """
    try:
        # Find export button. Click export button:
        print('-- Finding export button ...')
        time.sleep(SLEEPTIME_SHORT)
        export_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#exportTrigger')))
        export_button.click()
        print('\nDownloading results ...')
    except:
        # Switch the value of fail_to_download to 1:
        global fail_to_download
        fail_to_download = 1


def download_wait():
    """
    Wait to finish downloading and judge whether results were successfully downloaded or not.

    Returns:
        fail_to_download (int): 0 or 1, implies results were successfully downloaded or not, respectively.
        fail_count (int): times of unsuccessful downloading and trying again.

    """
    download_seconds = 0
    download_wait = True
    while download_wait and download_seconds < DOWNLOAD_TIMEOUT:
        time.sleep(1)
        download_wait = False
        for filename in os.listdir(directory):
            if filename.endswith('.crdownload'):
                download_wait = True
        download_seconds += 1
    if os.listdir(directory) != []:
        nonScopus_count = 0
        for filename in os.listdir(directory):
            if re.findall(r'scopus', filename) != []:
                os.rename(os.path.join(directory, filename), os.path.join(directory, f'{subyear}.ris'))
                print('-- Downloaded results in {}.'.format(subyear))
                # Switch the value of fail_to_download to 0:
                global fail_to_download
                fail_to_download = 0
                break
            else:
                nonScopus_count += 1
        if nonScopus_count == len(os.listdir(directory)):
            print('-- Failed to download results in {}. (The file does not exist)'.format(subyear))
            # Switch the value of fail_to_download to 1:
            fail_to_download = 1
            # Increase the value of fail_count:
            global fail_count
            fail_count += 1
    else:
        print('-- Failed to download results in {}. (The file does not exist)'.format(subyear))
        # Switch the value of fail_to_download to 1:
        fail_to_download = 1
        # Increase the value of fail_count:
        fail_count += 1


def main():
    """
    Workflow of advanced_query_articles.

    Returns:
        If the fail_to_download equals 1, try this workflow again until the fail_count is less than the times limit to trying (to download) again.

    """
    if fail_count < TRY_AGAIN_TIMES:
        # Zero the value of fail_to_download:
        global fail_to_download
        fail_to_download = 0

        advanced_search()
        select_all_results()
        download()
        download_wait()

        if fail_to_download == 1:
            # Try again
            print('\nFailed to download results in {}. Try again ...'.format(subyear))
            main()
    else:
        print('\n★ Failed to download results in {}. (Tried {} times)'.format(subyear, TRY_AGAIN_TIMES))


if __name__ == '__main__':
    # region Define the directory for storaging results
    if not os.path.exists(os.path.join('Output', 'articles')):
        os.makedirs(os.path.join('Output', 'articles'))
    directory = os.path.join(os.getcwd(), 'Output', 'articles')
    # endregion

    # region Set the browser's options
    options = webdriver.ChromeOptions()
    # Headless:
    options.add_argument('--headless')
    # Add user-agent:
    options.add_argument(
        'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"')
    # No loading images:
    options.add_argument('blink-settings=imagesEnabled=false')
    prefs = {'profile.managed_default_content_settings.images': 2,
             'profile.default_content_settings.popups': 0,
             'download.default_directory': directory}
    options.add_experimental_option('prefs', prefs)
    # endregion

    # Launch a Chrome browser:
    browser = webdriver.Chrome(options=options)

    # Set the implicitly wait time of Selenium:
    wait = WebDriverWait(browser, WAIT_TIME)

    # region Log in via your institution or cookies
    # Timing starts:
    login_start = time.perf_counter()

    log_in(access=ACCESS)

    # Timing ends:
    login_end = time.perf_counter()
    login_execution_time = login_end - login_start
    print('Time of logging in is: {:.2f} s'.format(login_execution_time))
    # endregion

    # region Iteration: search and download articles' information in ris format in every year (i.e. "subyear") by query
    # Timing starts:
    main_start = time.perf_counter()
    # Create a dictionary to storage the information on the summary of results downloaded:
    summary_dict = {}

    for subyear in YEARS:
        # Timing starts:
        subyear_start = time.perf_counter()

        summary_dict[str(subyear)] = []
        # Initialize the value of fail_count and fail_to_download at the beginning of every iteration in every year:
        fail_count = 0
        fail_to_download = 0
        print('\n\n', '#' * 20, subyear, '#' * 20)
        main()
        # Extract the value of fail_to_download for summary:
        summary_dict[str(subyear)].append(fail_to_download)

        # Timing ends:
        subyear_end = time.perf_counter()
        subyear_execution_time = subyear_end - subyear_start
        # Extract the execution time for summary:
        summary_dict[str(subyear)].append(round(subyear_execution_time, 2))

    # Timing ends:
    main_end = time.perf_counter()
    main_execution_time = main_end - main_start
    # endregion

    # region Print the summary of this execution
    print('\n\n', '#' * 20, 'summary', '#' * 20)
    # Print in table-like format:
    summary_table = PrettyTable(['Year', 'Results', 'Failed', 'ExecutionTime'])
    for key, value in summary_dict.items():
        summary_table.add_row([key, value[0], value[-2], value[-1]])
    summary_table.add_column('Index', [index for index in range(1, len(summary_dict) + 1)])
    print(summary_table)
    # Print the execution time:
    print(f'''LogInTime: {round(login_execution_time, 2)}s = {round(login_execution_time / 60, 2)}min
MainTime: {round(main_execution_time, 2)}s = {round(main_execution_time / 60, 2)}min
Average of {round(main_execution_time / len(YEARS), 2)}s = {round(main_execution_time / len(YEARS) / 60, 2)}min per year to download''')
    # endregion

    # Close the browser:
    browser.quit()
