from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view()),
    url(r'^add/$', views.Add.as_view()),

    url(r'^task/show/(?P<taskid>\d+)/$', views.TaskShow.as_view()),
    url(r'^task/del/(?P<taskid>\d+)/$', views.TaskDel.as_view()),
    url(r'^task/cmd/(?P<taskid>\d+)/$', views.TaskCmd.as_view()),
    url(r'^task/fileadd/(?P<taskid>\d+)/$', views.FileAdd.as_view()),

    url(r'^regist/$', views.UserReg.as_view()),
    url(r'^login/$', views.UserLogin.as_view()),
    url(r'^logout/$', views.UserLogout.as_view()),
    url(r'^edit/(?P<taskid>\d+)/$', views.Edit.as_view()),

    url(r'^test/$', views.TestView.as_view()),

]