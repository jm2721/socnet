from achievements.models import Achievement
from users.models import User, WallPost

achievement_descriptions = [("Reaching out", "Sent 1 friend request"),
                            ("Friendly", "Reach 50 friends"),
                            ("Super Friendly", "Reach 100 friends"),
                            ("Politician", "Reach 500 friends"),
                            ("Outspoken", "Post 50 wall posts"),
                            ("Social climber", "Post 150 wall posts"),
                            ]

def get_achievement(title):
    return Achievement.objects.get(title=title)

def check_criteria(calling_user, user_points, title, wallposts=False):
    if wallposts:
        return len(WallPost.objects.filter(poster=calling_user)) >= user_points and not calling_user.has_achievement(Achievement.objects.get(title=title))
    else:
        return len(calling_user.friends.all()) >= user_points and not calling_user.has_achievement(Achievement.objects.get(title=title))

def check_achievements(caller_id):
    calling_user = User.objects.get(pk=caller_id)

    if check_criteria(calling_user, 50, "Friendly"):
        calling_user.achievements.add(get_achievement("Friendly"))
    if check_criteria(calling_user, 100, "Super Friendly"):
        calling_user.achievements.add(get_achievement("Super Friendly"))
    if check_criteria(calling_user, 500, "Politician"):
        calling_user.achievements.add(get_achievement("Politician"))

    if check_criteria(calling_user, 50, "Outspoken", True):
        calling_user.achievements.add(Achievement.objects.get(title="Outspoken"))
    if check_criteria(calling_user, 150, "Social climber", True):
        calling_user.achievements.add(Achievement.objects.get(title="Social climber"))