from django.http import HttpResponse
from django.shortcuts import render
import main.models as models


def index(request):
    args = {
        'battles': [
            {
                'battle': battle,
                'battlers': [
                    {
                        'battler': battler,
                        'vote': models.Vote.objects.filter(battle=battle, battler=battler).count
                    }
                    for battler in battle.battlers.all()
                ]
            }
            for battle in models.Battle.objects.all()
        ]
    }
    return render(request, 'index.html', args)


def set_vote_api(request):
    if request.method == 'POST' and request.user is not None:
        round_id = request.POST.get('round_id')
        battler_id = request.POST.get('battler_id')
        models.Vote(battle=models.Battle.objects.get(id=round_id), voter=request.user,
                    battler=models.User.objects.get(id=battler_id)).save()
        return HttpResponse('1')
    return HttpResponse('0')
