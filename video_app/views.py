from django.shortcuts import render, Http404, redirect, HttpResponse
from video_app.models import Video, Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from video_app.form import LoginForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def listing(request, cate=None):
    context = {}
    if cate is None:
        vids_list = Video.objects.all()
    if cate == 'editors':
        vids_list = Video.objects.filter(editor_choice=True)
    else:
        vids_list = Video.objects.all()
    page_robot = Paginator(vids_list, 9)
    page_num = request.GET.get('page')
    try:
        vids_list = page_robot.page(page_num)
    except EmptyPage:
        vids_list = page_robot.page(page_robot.num_pages)
        # raise Http404('empty page')
    except PageNotAnInteger:
        vids_list = page_robot.page(1)
    context['vids_list'] = vids_list
    return render(request, 'listing.html', context)


def login_index(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to='list')
    context['form'] = form
    return render(request, 'register_login.html', context)


def register_index(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')
    context['form'] = form
    return render(request, 'register_login.html', context)


def detail(request, id):
    context = {}
    vid_info = Video.objects.get(id=id)
    voter_id = request.user.profile.id
    likes_count = Ticket.objects.filter(choice='like').count()
    try:
        user_ticket_for_this_video = Ticket.objects.get(voter_id=voter_id, video_id=id)
        context['user_ticket'] = user_ticket_for_this_video
    except:
        pass
    context['vid_info'] = vid_info
    context['likes_count'] = likes_count
    return render(request, 'detail.html', context)


def detail_vote(request, id):
    voter_id = request.user.profile.id
    try:
        user_ticket_for_this_video = Ticket.objects.get(voter_id=voter_id, video_id=id)
        user_ticket_for_this_video.choice = request.POST['vote']
        user_ticket_for_this_video.save()
    except ObjectDoesNotExist:
        new_ticket = Ticket(voter_id=voter_id, video_id=id, choice=request.POST['vote'])
        new_ticket.save()
    return redirect(to='detail', id=id)

