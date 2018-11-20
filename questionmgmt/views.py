from django.shortcuts import render

# Create your views here.


from lxml.html import document_fromstring
import json
import requests
import re
import urllib


# Generic Functions
def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    return query

def mid(s, offset, amount):
    return s[offset:amount]



# Question Import From Edoola
cookies = {
    '_ga': 'GA1.2.290460516.1542006845',
    'csrftoken': 'RZfxEUJOTOczvUr8kGAFQf8lYYXMpxEt',
    'sessionid': 'k8jnuqbwzsf09zc0qkk8cdvpghj5kqyq',
    '_gid': 'GA1.2.2040430800.1542631858',
    '_gat': '1',
}

headers = {
    'Pragma': 'no-cache',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://careeranna.edoola.com/manage/content/',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
}


# Folders Download
def download_folders():
    obj = {}

    params = (
        ('folder_id', ''),
    )

    response_folders = requests.get('http://careeranna.edoola.com/manage/content/', headers=headers, params=params, cookies=cookies)
    output_folderlist = response_folders.content
    doc_folders = document_fromstring(output_folderlist)
    folder_table = (doc_folders.xpath("//table[contains(@id, 'folder_table')]/tr/td"))


    list_folders = []

    for folder in folder_table:
        folderobj = {}
        folder_name = ""
        folder_id = ""
        folder_id = folder.xpath("./@id")[0]
        folder_name = cleanstring(folder.text_content())
        folderobj = {"folder_id":folder_id,"folder_name":folder_name}
        list_folders.append(folderobj)

    obj = {'folders':list_folders}
    return  obj

# Tests Download in a folder
def download_tests_infolder(folder_id='1962'):
    obj = {}
    params = (
        ('folder_id', folder_id),
    )
    response_tests = requests.get('http://careeranna.edoola.com/manage/content/list/', headers=headers, params=params, cookies=cookies)
    output_testlist = response_tests.content
    doc_test = document_fromstring(output_testlist)
    tests_table = (doc_test.xpath("//table[contains(@class,'table')]/tr"))

    list_tests = []
    row = 0
    for test in tests_table:
        try:
            td = test.xpath("./td")
            test_obj = {}
            vanilla_link = td[0].xpath("./a/@href")[0]
            test_name = td[0].text_content()
            type = td[1].text_content()
            date_modified = td[2].text_content()
            question_count = td[3].text_content()
            score_count = td[4].text_content()
            questions_link = ("http://careeranna.edoola.com" + vanilla_link.replace("/detail/", '/questions/'))
            details_link = ("http://careeranna.edoola.com" + vanilla_link)
            test_details_link = questions_link
            test_obj = {"name":cleanstring(test_name),
                        "details_link":details_link,
                        "question_link":questions_link,
                        "type":cleanstring(type),
                        "date_modified":cleanstring(date_modified),
                        "score_count":score_count,
                        "question_count":question_count}
            list_tests.append(test_obj)
        except:
            None
    obj = {'tests':list_tests}
    return obj



def download_questions(question_link = 'http://careeranna.edoola.com/manage/tests/questions/cat-2018-sectional-test-19-verbal-ability-and-reading-comprehension-1/',details_link = 'http://careeranna.edoola.com/manage/tests/detail/xat-mock-subhankar-qa_di-1/'):
    obj = {}
    response_details = requests.get(details_link, headers=headers, cookies=cookies)
    output_details = response_details.content
    paper_details_start = output_details.find("question_paper =",1)
    paper_details_end = output_details.find("paged_questions =",1)

    paper_details_data = (mid(output_details, paper_details_start + 17, paper_details_end)).replace(";\n        ", "")
    paper_details_data_json = json.loads(paper_details_data)

    page_num = 1
    params = (
        ('page', str(page_num)),
    )
    questions_list = []
    response_questions = requests.get(question_link, headers=headers, params=params, cookies=cookies)
    ques_content = response_questions._content
    question_json = json.loads(ques_content)
    page = question_json['paged_questions']['page']
    has_next = page['has_next']
    questions_list = question_json['paged_questions']['questions']
    while has_next:
        page_num = page_num + 1
        params = (
            ('page', str(page_num)),
        )
        response_questions = requests.get(question_link,headers=headers, params=params, cookies=cookies)
        ques_content = response_questions._content
        question_json = json.loads(ques_content)
        page = question_json['paged_questions']['page']
        has_next = page['has_next']
        new_questions = question_json['paged_questions']['questions']
        questions_list.extend(new_questions)
    pure_question = []
    passages = []
    for ques in questions_list:
        try:
            if ques['question_number'] == "P":
                passages.append(ques)
            elif int(ques['question_number'])>=1:
                pure_question.append(ques)
        except:
            None
    obj = {'passages':passages,'questions':pure_question,'details':paper_details_data_json}
    return obj


def download_question_image(link):
    urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")






