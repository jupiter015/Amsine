import uuid
import json
from django.db import models

# Create your models here.
class UserMeta(models.Model):
    role_choices = (("user", "Normal User"), ("admin", "Powerful User"))
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    role = models.CharField(max_length=10, choices=role_choices, default="user")
    username = models.CharField(max_length=8, unique=True)
    email_id = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.uuid)

class LanguageMeta(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=19)
    document_path = models.FileField(upload_to='HomePage/language_documents/')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class UserProgress(models.Model):
    userMeta = models.ForeignKey(UserMeta, on_delete=models.CASCADE, related_name="home_user_progresses")
    languageMeta = models.ForeignKey(LanguageMeta, on_delete=models.SET_NULL, null=True, related_name="home_user_progresses")
    progress = models.JSONField(null=True)

    def set_data(self, data):
        self.progress = json.dumps(data)
    
    def get_data(self) -> dict:
        return json.loads(self.progress)
    
    def isLocked(self, chapterType:str, chapterNum:int, lessonNum:int) -> bool:
        islocked = True
        for chp in self.get_data().get('progress'):
            if chp.get('chapterNum') == chapterNum and chp.get('type') == chapterType:
                for lesProgress in chp.get('lessons'):
                    if lesProgress.get('lessonNum') == lessonNum:
                        islocked = lesProgress.get('locked')
                        break
                break
        return islocked
    
    def isCompleted(self, chapterType:str, chapterNum:int, lessonNum:int) -> bool:
        isCompleted = True
        for chp in self.get_data().get('progress'):
            if chp.get('chapterNum') == chapterNum and chp.get('type') == chapterType:
                for lesProgress in chp.get('lessons'):
                    if lesProgress.get('lessonNum') == lessonNum:
                        isCompleted = lesProgress.get('completed')
                        break
                break
        return isCompleted
    
    def setLocked(self, chapterType:str, chapterNum:int, lessonNum:int, isLocked: bool):
        progress = self.get_data()
        for chp in progress.get('progress'):
            if chp.get('chapterNum') == chapterNum and chp.get('type') == chapterType:
                for lesProgress in chp.get('lessons'):
                    if lesProgress.get('lessonNum') == lessonNum:
                        lesProgress['locked'] = isLocked
                        break
                break
        self.set_data(progress)
        self.save()
        return

    def setCompleted(self, chapterType:str, chapterNum:int, lessonNum:int, isCompleted: bool):
        progress = self.get_data()
        doUnlockInterestChapters = False
        doUnlockNextChapter = False
        for chp in progress.get('progress'):
            if chp.get('chapterNum') == chapterNum and chp.get('type') == chapterType:
                amount_of_lessons = len(chp.get('lessons'))
                for lesProgress in chp.get('lessons'):
                    if lesProgress.get('lessonNum') == lessonNum:
                        lesProgress['completed'] = isCompleted
                        break
                if lessonNum == amount_of_lessons:
                    if chapterType == "normalChapters" and chapterNum >= 2:
                        doUnlockInterestChapters = True
                    doUnlockNextChapter = True
                break
        self.set_data(progress)
        self.save()
        if doUnlockNextChapter:
            self.setLocked(chapterType, chapterNum + 1, 1, False)
            self.setLocked(chapterType, chapterNum + 1, 2, False)
            self.setLocked(chapterType, chapterNum + 1, 3, False)
        if doUnlockInterestChapters:
            self.setLocked("readingChapters", 1, 1, False)
            self.setLocked("readingChapters", 1, 2, False)
            self.setLocked("readingChapters", 1, 3, False)

            self.setLocked("gamingChapters", 1, 1, False)
            self.setLocked("gamingChapters", 1, 2, False)
            self.setLocked("gamingChapters", 1, 3, False)

            self.setLocked("travellingChapters", 1, 1, False)
            self.setLocked("travellingChapters", 1, 2, False)
            self.setLocked("travellingChapters", 1, 3, False)
        return
    
    def __str__(self):
        return str(self.userMeta.uuid)

    