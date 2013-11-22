
from achievements.models import Achievement
from achievements.criteria import achievement_descriptions

def create_achievements():
    if len(Achievement.objects.all()) != len(achievement_descriptions):
        for a in Achievement.objects.all():
            a.delete()
        for a in achievement_descriptions:
            Achievement.objects.create(title=a[0], description=a[1])

if __name__ == "__main__":
    create_achievements()