import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse
from HomePage.models import LanguageMeta, UserMeta, UserProgress
from ProfilePage.models import UserProfile
from authentication import validateSession

def index(request:HttpRequest):
    if validateSession(request):
        user = UserMeta.objects.filter(uuid=request.COOKIES.get('user_id'))[0]
        userProfile = UserProfile.objects.filter(userMeta=user)[0]
        if userProfile.language_learning.count() != 0:
            return redirect('/')
        return render(request, 'CustomizePage/index.html', {'languages': LanguageMeta.objects.all()})
    else:
        return redirect('/login/')

def addLanguageLearning(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        
        # Adding Learning Language
        language = LanguageMeta.objects.filter(uuid=request.POST.get('language_id'))[0]
        userProfile = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
        userProfile.language_learning.add(language)
        userProfile.last_language_used = language
        userProfile.save()

        # Add User Progress
        with open('./language_documents/' + language.name.lower() + "/" + language.name.lower() + ".json", encoding='utf-8') as f:
            json_data = f.read()
            
        data = json.loads(json_data)
        progress = {'progress': []}

        chapterNum = 0
        for chapters in data['normalChapters']:
            chapterNum += 1
            les_dict = []

            lessonNum = 0
            for lesson in chapters.get('lessons'):
                lessonNum += 1
                if chapterNum == 1:
                    les_dict.append({'lessonNum': lessonNum, 'completed':False, 'locked': False})
                else:
                    les_dict.append({'lessonNum': lessonNum, 'completed':False, 'locked': True})

            progress.get('progress').append({'chapterNum': chapterNum, 'type':'normalChapters', 'lessons': les_dict})
        
        chapterNum = 0
        for chapters in data['travellingChapters']:
            chapterNum += 1
            les_dict = []

            lessonNum = 0
            for lesson in chapters.get('lessons'):
                lessonNum += 1
                les_dict.append({'lessonNum': lessonNum, 'completed':False, 'locked': True})

            progress.get('progress').append({'chapterNum': chapterNum, 'type':'travellingChapters', 'lessons': les_dict})

        chapterNum = 0
        for chapters in data['readingChapters']:
            chapterNum += 1
            les_dict = []

            lessonNum = 0
            for lesson in chapters.get('lessons'):
                lessonNum += 1
                les_dict.append({'lessonNum': lessonNum, 'completed':False, 'locked': True})

            progress.get('progress').append({'chapterNum': chapterNum, 'type':'readingChapters', 'lessons': les_dict})
        
        chapterNum = 0
        for chapters in data['gamingChapters']:
            chapterNum += 1
            les_dict = []

            lessonNum = 0
            for lesson in chapters.get('lessons'):
                lessonNum += 1
                les_dict.append({'lessonNum': lessonNum, 'completed':False, 'locked': True})

            progress.get('progress').append({'chapterNum': chapterNum, 'type':'gamingChapters', 'lessons': les_dict})
        
        userProgress = UserProgress(userMeta=UserMeta.objects.filter(uuid=request.COOKIES.get('user_id'))[0], languageMeta=language)
        userProgress.set_data(progress)
        userProgress.save()

        return JsonResponse({'success': True})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('customize/')
    
def getNativeLanguagePage(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        languages_learning = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0].language_learning.all()
        return HttpResponse(render(request, 'CustomizePage/nativeLan.html', {'languages': LanguageMeta.objects.all(), 'learning_language':languages_learning}))
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('customize/')

def addNativeLanguage(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        
        # Adding Naitve Language
        language = LanguageMeta.objects.filter(uuid=request.POST.get('language_id'))[0]
        userProfile = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
        userProfile.native_language = language
        userProfile.save()

        return JsonResponse({'success': True})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('customize/')
    
def getInterestPage(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        return HttpResponse(render(request, 'CustomizePage/interest.html', {'interests': ['Travelling', 'Reading', 'Gaming']}))
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('customize/')
    
def addInterest(request:HttpRequest):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        
        # Adding Interest
        interests = request.POST.get('selectedCheckboxes').split(',')
        userProfile = UserProfile.objects.filter(userMeta__uuid=request.COOKIES.get('user_id'))[0]
        userProfile.interests = interests
        userProfile.save()

        return JsonResponse({'success': True})
    else:
        if request.META.get("HTTP_REFERER"):
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect('customize/')