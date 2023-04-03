import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from LoginPage.models import SessionMeta
from HomePage.models import LanguageMeta, UserMeta, UserProgress
from ProfilePage.models import UserProfile
from authentication import validateSession

#
# Returns the base HOME page
#
def index(request:HttpRequest):
    if validateSession(request):
        user = UserMeta.objects.filter(uuid=request.COOKIES.get('user_id'))[0]
        userProfile = UserProfile.objects.filter(userMeta=user)[0]
        if userProfile.language_learning.count() == 0:
            return redirect('customize/')
        return render(request, 'HomePage/index.html', {'last_language_used': userProfile.last_language_used})
    else:
        return redirect('login/')

#
# Logging out AJAX
#
def logOut(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        for ses in SessionMeta.objects.filter(userMeta__uuid=request.COOKIES.get("user_id")):
            ses.delete()
        return JsonResponse({})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/home/')

#
# See if profile is completely customized
#
def checkIfUserProfileCustomized(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        userProfile = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
        if len(userProfile.interests) == 0 or userProfile.native_language == None:
            return JsonResponse({'complete': False})
        return JsonResponse({'complete': True})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('/home/')

#
# Load Chapters in Home Page
#
def loadChapters(request:HttpRequest):
    # See if AJAX Request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':

        # get language object
        language = LanguageMeta.objects.filter(uuid=request.GET.get('last_language_used'))
        if len(language) != 0:

            # Load JSON Data in DICT 
            json_data = ''
            with open('./language_documents/' + language[0].name.lower() + "/" + language[0].name.lower() + ".json", encoding='utf-8') as f:
                json_data = f.read()
            
            data = json.loads(json_data)

            # Create Context Object to send
            context = {'chapters': [], 'language': language[0].name}
            overallChapterNum = 0

            userProfile = UserProfile.objects.filter(userMeta=request.COOKIES.get('user_id'))[0]
            userProgress = UserProgress.objects.filter(userMeta=request.COOKIES.get('user_id'), languageMeta = language[0])[0]

            chapterNum = 0
            # Add Chapter data from json to context object FOR "normalChapters"
            for chapters in data['normalChapters']:
                overallChapterNum += 1
                chapterNum += 1
                les_dict = []
                
                lessonNum = 0
                for les in chapters.get('lessons'):
                    lessonNum += 1

                    lessonProgress = userProgress.isCompleted('normalChapters', chapterNum, lessonNum)
                    lessonLocked = userProgress.isLocked('normalChapters', chapterNum, lessonNum)

                    les_dict.append({'lessonNum':str(lessonNum), 'lesson_title': les.get('lesson_title'), 'lesson_description': les.get('lesson_description'), 'lessonLocked': lessonLocked, 'lessonProgress': lessonProgress})
                
                # Check if all lessons are locked
                chapterLocked = True
                for les in les_dict:
                    if not les.get('lessonLocked'):
                        chapterLocked = False
                        break

                context.get('chapters').append({'chapterNum': str(overallChapterNum), 'chapter_title': chapters.get('chapter_title'), 'chapter_description': chapters.get('chapter_description'), 'type':'NC', 'lessons': les_dict, 'chapterLocked': chapterLocked})
            
            chapterNum = 0
            # Add Chapter data from json to context object FOR "travellingChapters"
            if 'travelling' in userProfile.interests:
                for chapters in data['travellingChapters']:
                    overallChapterNum += 1
                    chapterNum += 1
                    les_dict = []
                    
                    lessonNum = 0
                    for les in chapters.get('lessons'):
                        lessonNum += 1

                        lessonProgress = userProgress.isCompleted('travellingChapters', chapterNum, lessonNum)
                        lessonLocked = userProgress.isLocked('travellingChapters', chapterNum, lessonNum)

                        les_dict.append({'lessonNum':str(lessonNum), 'lesson_title': les.get('lesson_title'), 'lesson_description': les.get('lesson_description'), 'lessonLocked': lessonLocked, 'lessonProgress': lessonProgress})
                    
                    # Check if all lessons are locked
                    chapterLocked = True
                    for les in les_dict:
                        if not les.get('lessonLocked'):
                            chapterLocked = False
                            break

                    context.get('chapters').append({'chapterNum': str(overallChapterNum), 'chapter_title': chapters.get('chapter_title'), 'chapter_description': chapters.get('chapter_description'), 'type':'TC', 'lessons': les_dict, 'chapterLocked': chapterLocked})
            
            chapterNum = 0
            # Add Chapter data from json to context object FOR "readingChapters"
            if 'reading' in userProfile.interests:
                for chapters in data['readingChapters']:
                    overallChapterNum += 1
                    chapterNum += 1
                    les_dict = []
                    
                    lessonNum = 0
                    for les in chapters.get('lessons'):
                        lessonNum += 1

                        lessonProgress = userProgress.isCompleted('readingChapters', chapterNum, lessonNum)
                        lessonLocked = userProgress.isLocked('readingChapters', chapterNum, lessonNum)

                        les_dict.append({'lessonNum':str(lessonNum), 'lesson_title': les.get('lesson_title'), 'lesson_description': les.get('lesson_description'), 'lessonLocked': lessonLocked, 'lessonProgress': lessonProgress})
                    
                    # Check if all lessons are locked
                    chapterLocked = True
                    for les in les_dict:
                        if not les.get('lessonLocked'):
                            chapterLocked = False
                            break

                    context.get('chapters').append({'chapterNum': str(overallChapterNum), 'chapter_title': chapters.get('chapter_title'), 'chapter_description': chapters.get('chapter_description'), 'type':'RC', 'lessons': les_dict, 'chapterLocked': chapterLocked})
            
            chapterNum = 0
            # Add Chapter data from json to context object FOR "gamingChapters"
            if 'gaming' in userProfile.interests:
                for chapters in data['gamingChapters']:
                    overallChapterNum += 1
                    chapterNum += 1
                    les_dict = []
                    
                    lessonNum = 0
                    for les in chapters.get('lessons'):
                        lessonNum += 1

                        lessonProgress = userProgress.isCompleted('gamingChapters', chapterNum, lessonNum)
                        lessonLocked = userProgress.isLocked('gamingChapters', chapterNum, lessonNum)

                        les_dict.append({'lessonNum':str(lessonNum), 'lesson_title': les.get('lesson_title'), 'lesson_description': les.get('lesson_description'), 'lessonLocked': lessonLocked, 'lessonProgress': lessonProgress})
                    
                    # Check if all lessons are locked
                    chapterLocked = True
                    for les in les_dict:
                        if not les.get('lessonLocked'):
                            chapterLocked = False
                            break

                    context.get('chapters').append({'chapterNum': str(overallChapterNum), 'chapter_title': chapters.get('chapter_title'), 'chapter_description': chapters.get('chapter_description'), 'type':'GC', 'lessons': les_dict, 'chapterLocked': chapterLocked})
                
            # Render the section of the page to send
            html = render_to_string('HomePage/chaptersRender.html', context=context)
            return JsonResponse({'html': html})
        else:
            return JsonResponse({'error_message': 'Could not find the language'}, status=400)
    # If it is not a AJAX request
    else:
        if request.META.get('HTTP_REFERER'):
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('/home/')

#
# Lesson HTML Page
#
def loadLessonGame(request:HttpRequest, language_name:str, chapter_type:str, chapterNum:int, lessonNum:int):
    if validateSession(request):
        userProfile = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
        if userProfile.language_learning.count() == 0:
            return redirect('/customize/')
        
        # Get Chapter Type
        chapterType = ''
        if chapter_type == 'NC':
            chapterType = 'normalChapters'
        elif chapter_type == 'TC':
            chapterType = 'travellingChapters'
        elif chapter_type == 'RC':
            chapterType = 'readingChapters'
        elif chapter_type == 'GC':
            chapterType = 'gamingChapters'
        
        if not UserProgress.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0].isLocked(chapterType=chapterType, chapterNum=chapterNum, lessonNum=lessonNum):
            return render(request, 'HomePage/lessonGame.html', {'last_language_used': userProfile.last_language_used, 'language_name': language_name, 'chapter_type': chapter_type, 'chapterNum': chapterNum, 'lessonNum': lessonNum})
        return redirect('/')
    else:
        return redirect('/login/')

#
# Get Next question AJAX
#
def loadNextQuestion(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':

        # Get JSON Data in Dict
        json_data = ''
        with open('./language_documents/' + request.GET.get('language_name').lower() + "/" + request.GET.get('language_name').lower() + ".json", encoding='utf-8') as f:
            json_data = f.read()
            
        data = json.loads(json_data)

        # Get Chapter Type
        chapter_type = ''
        if request.GET.get('chapter_type') == 'NC':
            chapter_type = 'normalChapters'
        elif request.GET.get('chapter_type') == 'TC':
            chapter_type = 'travellingChapters'
        elif request.GET.get('chapter_type') == 'RC':
            chapter_type = 'readingChapters'
        elif request.GET.get('chapter_type') == 'GC':
            chapter_type = 'gamingChapters'

        # Data to send
        question_data = {}
        question_type = ''

        # Getting question data and also which type of question it is
        chapterNum = 0
        for chapters in data[chapter_type]:
            chapterNum += 1
            if int(request.GET.get('chapterNum')) == chapterNum:
                lessonNum = 0
                for les in chapters.get('lessons'):
                    lessonNum += 1
                    if int(request.GET.get('lessonNum')) == lessonNum:
                        questionNumber = 0
                        question_found = False
                        for question in les.get('flashcard_questions'):
                            questionNumber += 1
                            if questionNumber - 1 == int(request.GET.get('current_question')):
                                question_found = True
                                question_data = question
                                question_type = 'flashcard'
                                break
                        if not question_found:
                            for question in les.get('translating_questions'):
                                questionNumber += 1
                                if questionNumber - 1 == int(request.GET.get('current_question')):
                                    question_found = True
                                    question_data = question
                                    question_type = 'translating'
                                    break
                        break
                break
        
        # Rendering the page according to what kind of question it is
        if question_type == 'flashcard':
            html = render_to_string('HomePage/flashcard.html', context=question_data)
        elif question_type == 'translating':
            html = render_to_string('HomePage/translating.html', context=question_data)
        # if question not found, that means the lesson has ended
        else:
            userProgress = UserProgress.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'), languageMeta=LanguageMeta.objects.filter(name=request.GET.get('language_name'))[0])[0]
            
            userProgress.setCompleted(chapterType=chapter_type, chapterNum=int(request.GET.get('chapterNum')), lessonNum=int(request.GET.get('lessonNum')), isCompleted=True)
            
            html = render_to_string('HomePage/lessonEnd.html')
        return JsonResponse({'html':html})
    else:
        if request.META.get('HTTP_REFERER'):
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('/home/')

#
# Load Chapter Quiz 
#
def loadChapterQuiz(request:HttpRequest, language_name:str, chapter_type:str, chapterNum:int):
    if validateSession(request):
        userProfile = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
        if userProfile.language_learning.count() == 0:
            return redirect('/customize/')
        
        # Get Chapter Type
        chapterType = ''
        if chapter_type == 'NC':
            chapterType = 'normalChapters'
        elif chapter_type == 'TC':
            chapterType = 'travellingChapters'
        elif chapter_type == 'RC':
            chapterType = 'readingChapters'
        elif chapter_type == 'GC':
            chapterType = 'gamingChapters'
        
        if not UserProgress.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0].isLocked(chapterType=chapterType, chapterNum=chapterNum, lessonNum=1):
            return render(request, 'HomePage/chapterQuiz.html', {'last_language_used': userProfile.last_language_used, 'language_name': language_name, 'chapter_type': chapter_type, 'chapterNum': chapterNum})
        return redirect('/')
    else:
        return redirect('/login/')

def loadNextQuizQuestion(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':

        # Get JSON Data in Dict
        json_data = ''
        with open('./language_documents/' + request.GET.get('language_name').lower() + "/" + request.GET.get('language_name').lower() + ".json", encoding='utf-8') as f:
            json_data = f.read()
            
        data = json.loads(json_data)

        # Get Chapter Type
        chapter_type = ''
        if request.GET.get('chapter_type') == 'NC':
            chapter_type = 'normalChapters'
        elif request.GET.get('chapter_type') == 'TC':
            chapter_type = 'travellingChapters'
        elif request.GET.get('chapter_type') == 'RC':
            chapter_type = 'readingChapters'
        elif request.GET.get('chapter_type') == 'GC':
            chapter_type = 'gamingChapters'

        # Data to send
        question_data = {}
        question_type = ''

        # Getting question data and also which type of question it is
        chapterNum = 0
        for chapters in data[chapter_type]:
            chapterNum += 1
            if int(request.GET.get('chapterNum')) == chapterNum:
                questionNumber = 0
                for quiz in chapters.get('quiz_questions'):
                    questionNumber += 1
                    if questionNumber - 1 == int(request.GET.get('current_question')):
                        question_data = quiz
                        question_type = 'quiz'
                        break
                break
        
        # Rendering the page according to what kind of question it is
        if question_type == 'quiz':
            html = render_to_string('HomePage/quiz.html', context=question_data)
        # if question not found, that means the lesson has ended
        else:
            userProgress = UserProgress.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'), languageMeta=LanguageMeta.objects.filter(name=request.GET.get('language_name'))[0])[0]
            
            html = render_to_string('HomePage/lessonEnd.html')
        return JsonResponse({'html':html})
    else:
        if request.META.get('HTTP_REFERER'):
            return redirect(request.META.get('HTTP_REFERER'))
        return redirect('/home/')