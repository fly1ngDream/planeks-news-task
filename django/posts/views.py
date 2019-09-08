from urllib.parse import quote_plus

from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.views import generic
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect


from comments.models import Comment


from .models import Post
from users.models import CustomUser
from .forms import PostForm
from comments.forms import CommentForm


class PostListView(generic.ListView):
    '''
    List all posts
    '''
    model = Post
    template_name = 'post_list.djhtml'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('Search')
        if query:
            object_list = self.model.objects.filter(Q(title__icontains = query) |
                                                    Q(content__icontains = query))
        else:
            object_list = self.model.objects.filter(created__lte=timezone.now())
        return object_list


class PostDetailView(SuccessMessageMixin, FormMixin, generic.DetailView):
    '''
    Show post details
    '''
    model = Post
    form_class = CommentForm
    template_name = 'post_detail.djhtml'
    success_url = "."
    success_message = 'Your comment was successfully added.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['share_string'] = quote_plus(self.object.content)

        form = CommentForm(self.request.POST or None)

        context['comment_form'] = form

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        form = context['comment_form']

        if form.is_valid():
            content_data = form.cleaned_data.get('content')
            parent_obj = None

            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None

            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(
                                        author = self.request.user,
                                        content = content_data,
                                        parent = parent_obj,
                                    )

            subscribed_addresses = new_comment.post.subscribers.values_list('email', flat=True)
            mail_subject = 'New comment'
            current_site = get_current_site(request)
            message = render_to_string('new_comment.djhtml', {
                'post': new_comment.post,
                'domain': current_site.domain,
            })
            email = EmailMessage(
                mail_subject, message, to=subscribed_addresses
            )
            email.send()

        return self.form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().created > timezone.now():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.CreateView):
    '''
    Creates new post
    '''
    form_class = PostForm
    template_name = 'post_create.djhtml'
    login_url = 'users:login'
    success_message = 'Post was successfully created.'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.edit.UpdateView):
    '''
    Updates a post
    '''
    form_class = PostForm
    model = Post
    template_name = 'post_update.djhtml'
    login_url = 'login'
    success_message = 'Post was successfully updated.'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        if (
            not self.request.user.is_staff
            and not self.request.user.is_superuser
            and (self.request.user != self.get_object().author
                or self.get_object().created > timezone.now())
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    '''
    Removes a post
    '''
    model = Post
    template_name = 'post_delete.djhtml'
    success_url = reverse_lazy('post_list')
    login_url = 'login'
    success_url = reverse_lazy('posts:post_list')
    success_message = 'Post was successfully removed.'

    def dispatch(self, request, *args, **kwargs):
        if (
            not self.request.user.is_staff
            and not self.request.user.is_superuser
            and (self.request.user != self.get_object().author
                or self.get_object().created > timezone.now())
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


def attachment_download_view(self, slug):
    '''
    View that allows to download a post attachment
    '''
    file_path = Post.objects.get(slug=slug).attachment.path
    file_name = (
        Post.objects.get(slug=slug).slug + Post.objects.get(slug=slug).get_attachment_ext()
    )

    myfile = open(file_path, 'rb')
    response = HttpResponse(myfile, content_type ='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response

def subscribe_view(self, slug, pk):
    '''
    View that allows to subscribe for a new post comments
    '''
    if pk != None:
        user = CustomUser.objects.get(pk=pk)
        post = Post.objects.get(slug=slug)

        post.subscribers.add(user)
        post.save()

    return HttpResponseRedirect(post.get_absolute_url())

def unsubscribe_view(self, slug, pk):
    '''
    View that allows to unsubscribe from a new post comments
    '''
    if pk != None:
        user = CustomUser.objects.get(pk=pk)
        post = Post.objects.get(slug=slug)

        post.subscribers.remove(user)
        post.save()

    return HttpResponseRedirect(post.get_absolute_url())
