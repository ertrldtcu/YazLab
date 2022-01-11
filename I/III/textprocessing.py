from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import re

def read_pdf(path):
    fp = open(path, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    c = 0
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        text = retstr.getvalue()
        c += 1

    fp.close()
    return text


def find_students_name(text):

    regex = "Adı Soyadı: (.*)\\n"
    names = re.findall(regex, text)
    
    if names is not None:
        while(True):
            willbreak = True
            for i,name in enumerate(names):
                if name.endswith(" "):
                    names[i] = name[:-1]
                    willbreak = False
            if willbreak:
                break
        return names

    return "Öğrenci isimleri bulunamadı."


def find_students_number(text):
    
    regex = "Öğrenci No: (\d*)"
    numbers = re.findall(regex, text)

    if numbers is not None:
        return numbers

    return "Öğrenci numaraları bulunamadı."


def find_date(text):
    
    day = "(\d{2}|\d{1})"
    month = "(\d{2})"
    year = "(\d{4})"
    sorter = "([\s]|[\-]|[\/]|[\.])"
    regex = day + sorter + month + sorter + year

    date = re.search(regex, text)
    if date is not None:
        return date.group()

    return "Tarih bulunamadı."


def find_period(text):

    sorter = "[\s]|[\-]|[\/]|[\.]"
    regex = "(\d*)"
    period = re.findall(regex, text)
    
    periodstr = ""
    month = int(period[2])
    year = int(period[4])

    periodstr = ""
    if month < 7:
        if month > 2:
            periodstr = str(year - 1) + "-" + str(year) + " Bahar Dönemi"
        else:
            periodstr = str(year - 1) + "-" + str(year) + " Güz Dönemi"
    else:
        periodstr = str(year) + "-" + str(year + 1) + " Güz Dönemi" 

    return periodstr


def find_keywords(text):
    
    text = text.replace("\n"," ")
    regex = "Anahtar\s*kelimeler: (.*)"
    keywords = re.findall(regex, text)

    if len(keywords) > 0:
        
        keywords = keywords[0][0:keywords[0].find('.')]

        while(keywords != keywords.replace(" ,", ",")):
            keywords = keywords.replace(" ,", ",")
        while(keywords != keywords.replace(",  ", ", ")):
            keywords = keywords.replace(",  ", ", ")
        while(keywords != keywords.replace("  ", " ")):
            keywords = keywords.replace("  ", " ")

        keywords = keywords.strip()

        return keywords

    return "Anahtar kelimeler bulunamadı."


def find_lesson(text):

    regex = "BÖLÜMÜ\s*(.*)"
    lesson = re.findall(regex, text)
    if lesson is not None:
        lesson = lesson[0]
        return lesson.strip()

    return "Ders bulunamadı."

def find_title(text, lesson):

    text = text.replace("\n","")
    regex = lesson + "(.*)"
    title = re.findall(regex, text)
    
    title = title[0].strip()

    title = title[0:title.find("   ")]

    return title


def find_teachers(text):

    regex = "(.*)\s+\\n?Danışman, Kocaeli Üniv."
    teachers = [teacher for teacher in re.findall(regex, text) if teacher]
    if len(teachers) > 0:
        for i,teacher in enumerate(teachers):
            teachers[i] = teacher.strip()
        return ", ".join(teachers)

    return "Hocalar bulunamadı."


def find_juries(text):

    regex = "(.*)\s+\\n?Jüri Üyesi, Kocaeli Üniv"
    juries = [jury for jury in re.findall(regex, text) if jury]
    
    if len(juries) > 0:
        for i,jury in enumerate(juries):
            juries[i] = jury.strip()
        return ", ".join(juries)
    
    return "Jüriler bulunamadı."


def find_summary(text):
    
    text = text.replace("\n","")
    regex = "ÖZET(.*)Anahtar"
    summary = [s for s in re.findall(regex, text) if s]
    if len(summary) > 0:

        summary = summary[0]

        while(summary.find('ÖZET')):
            summary = summary[summary.find('ÖZET'):]
        
        while(summary != summary.replace("  ", " ")):
            summary = summary.replace("  ", " ")

        return summary[5:]

    return "Özet bulunamadı."
