from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Thread, Comment, VotingOption
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'forum/category_list.html', {'categories': categories})

def thread_list_student(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_list_student.html', {'threads': threads})
def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'forum/thread_list.html', {'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    category = thread.category
    upvote_count = thread.upvotes.count()
    voting_options = thread.voting_options.all() if thread.enable_voting else None

    # Handle the submission of comments
    if request.method == 'POST':
        text = request.POST['text']
        comment = Comment.objects.create(thread=thread, user=request.user, text=text)
        # Redirect to the specific comment
        return redirect(f'{request.path}#comment-{comment.id}')

    # Get all comments and check if they belong to the current user
    comments = thread.comments.all()
    comments_with_user_status = [
        (comment, comment.user == request.user) for comment in comments
    ]

    return render(request, 'forum/thread_detail.html', {
        'thread': thread,
        'category': category,
        'upvote_count': upvote_count,
        'voting_options': voting_options,
        'comments_with_user_status': comments_with_user_status,  # Pass the combined list
    })


@login_required
def upvote_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.user in thread.upvotes.all():
        thread.upvotes.remove(request.user)
    else:
        thread.upvotes.add(request.user)
    return redirect('thread_detail', thread_id=thread.id)

@login_required
def create_thread(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category_name = request.POST['category']
        category = Category.objects.get(name=category_name)

        # Create and save the new thread
        thread = Thread.objects.create(
            title=title,
            content=content,
            category=category,
            created_by=request.user,
        )

        # If voting is enabled, handle creation of voting options
        if 'enable_voting' in request.POST and request.POST['enable_voting'] == 'on':
            thread.enable_voting = True
            thread.save()

            # Create voting options from form input
            options = request.POST.getlist('options[]')
            for option_text in options:
                if option_text:
                    VotingOption.objects.create(thread=thread, option_text=option_text)

        return redirect('thread_list')  # Redirect to the thread list page

    categories = Category.objects.all()
    return render(request, 'forum/create_thread.html', {'categories': categories})


@login_required
def vote_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if thread.enable_voting:
        if request.method == 'POST':
            selected_option_id = request.POST.get('vote')
            selected_option = get_object_or_404(VotingOption, id=selected_option_id)
            
            # Update the votes (if you're storing votes)
            selected_option.votes += 1
            selected_option.save()
        
        return redirect('thread_detail', thread_id=thread.id)
    else:
        return HttpResponse("Voting is not enabled for this thread.", status=400)

# =================================================================
# STUDENT 
# =================================================================

def thread_detail_student(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    category = thread.category
    upvote_count = thread.upvotes.count()
    voting_options = thread.voting_options.all() if thread.enable_voting else None

    # Handle the submission of comments
    if request.method == 'POST':
        text = request.POST['text']
        comment = Comment.objects.create(thread=thread, user=request.user, text=text)
        # Redirect to the specific comment
        return redirect(f'{request.path}#comment-{comment.id}')

    # Get all comments and check if they belong to the current user
    comments = thread.comments.all()
    comments_with_user_status = [
        (comment, comment.user == request.user) for comment in comments
    ]

    return render(request, 'forum/thread_detail_student.html', {
        'thread': thread,
        'category': category,
        'upvote_count': upvote_count,
        'voting_options': voting_options,
        'comments_with_user_status': comments_with_user_status,  # Pass the combined list
    })


