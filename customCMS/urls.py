from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('login_admin', views.admin_login),
    path('home_cms', views.HomeCMSView.as_view({'get': 'home_cms_list'})),
    path('activated_home_cms', views.ActvatedHomeCMSView.as_view({'get': 'activated_list'})),
    path('edit_home_cms/<int:pk>', views.EditHomeCMS.as_view()),
    path('active_home_cms/<int:pk>', views.ActiveHomeCMS.as_view()),
    path('category_cms', views.CategoryCMSView.as_view({'get': 'category_cms_list'})),
    path('edit_category_cms/<int:pk>', views.EditCategoryCMS.as_view()),
    path('activated_category_cms', views.ActvatedCategoryCMSView.as_view({'get': 'activated_list'})),
    path('active_category_cms/<int:pk>', views.ActiveCategoryCMS.as_view()),
    path('contact_cms', views.ContactCMSView.as_view({'get': 'contact_cms_list'})),
    path('edit_contact_cms/<int:pk>', views.EditContactCMS.as_view()),
    path('activated_contact_cms', views.ActivatedContactCMSView.as_view({'get': 'activated_list'})),
    path('active_contact_cms/<int:pk>', views.ActiveContactCMS.as_view()),
    path('about_cms', views.AboutCMSView.as_view({'get': 'about_cms_list'})),
    path('edit_about_cms/<int:pk>', views.EditAboutCMS.as_view()),
    path('activated_about_cms', views.ActivatedAboutCMSView.as_view({'get': 'activated_list'})),
    path('active_about_cms/<int:pk>', views.ActiveAboutCMS.as_view()),
    path('cms_category', views.CategoryView.as_view({'get': 'category_cms_list'})),
    path('edit_category/<int:pk>', views.EditCategory.as_view()),
    path('category_status/<int:pk>', views.CategoryStatus.as_view()),
    path('footer_cms', views.FooterCMSView.as_view({'get': 'footer_list'})),
    path('activated_footer_cms', views.ActivatedFooterCMSView.as_view({'get': 'activated_list'})),
    path('edit_footer_cms/<int:pk>', views.EditFooterCMS.as_view()),
    path('active_footer_cms/<int:pk>', views.ActiveFooterCMS.as_view()),
    path('edit_contact_form/<int:pk>', views.EditContactForm.as_view()),
    path('get_contact_form/<int:pk>', views.GetContactForm.as_view()),
    path('get_inactive_home_components/<int:pk>', views.GetInactiveComponents.as_view()),
    path('get_active_home_components/<int:pk>', views.GetActiveComponents.as_view()),
]
