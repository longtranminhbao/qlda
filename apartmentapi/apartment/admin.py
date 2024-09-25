import cloudinary
from django.contrib import admin
from django.db import models  # Thêm import này
from django.db.models import Count, Sum
from django.template.response import TemplateResponse
from django.utils.html import mark_safe
from apartment.models import *
from django.urls import path  # Thêm import này
from django import forms
from django.utils.dateparse import parse_date
from django.contrib.auth.hashers import make_password  # Thêm import này


class ApartmentAdminSite(admin.AdminSite):
    site_header = 'Apartment Management'

    def get_urls(self):
        return [
            path('apartment-stats/', self.stats_view, name='apartment-stats'),
            path('survey-stats/', self.survey_stats, name='survey-stats'),
        ] + super().get_urls()

    def stats_view(self, request):
        selected_period = request.GET.get('period', 'month')
        group_by = {'month': models.functions.TruncMonth, 'quarter': models.functions.TruncQuarter,
                    'year': models.functions.TruncYear}.get(selected_period, models.functions.TruncMonth)

        revenue_stats = ResidentFee.objects.filter(status='Đã đăng ký').annotate(
            period=group_by('payment_date')
        ).values('period').annotate(
            total_revenue=Sum('fee__price')
        ).order_by('period')

        return TemplateResponse(request, 'admin/revenue_stats.html', {
            'period': selected_period,
            'revenue_stats': revenue_stats,
        })

    def survey_stats(self, request):
        survey_id = request.GET.get('survey_id', '1')
        survey = Survey.objects.get(id=survey_id)
        questions = survey.questions.all()
        question_stats = []
        for question in questions:
            total_responses = Answer.objects.filter(question=question).count()
            choice_stats = (
                Answer.objects.filter(question=question)
                .values('choice__content_choice')
                .annotate(choice_count=Count('id'))
                .order_by('choice__content_choice')
            )
            for stat in choice_stats:
                stat['percentage'] = (stat['choice_count'] / total_responses) * 100 if total_responses > 0 else 0
            question_stats.append({
                'question': question.content,
                'stats': choice_stats,
            })

        surveys = Survey.objects.all()

        context = {
            'surveys': surveys,
            'question_stats': question_stats,
        }

        return TemplateResponse(request, 'admin/survey_stats.html', context)


admin_site = ApartmentAdminSite(name='apartment')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class ResidentAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'apartment']
    search_fields = ['user_info__first_name', 'user_info__last_name']


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'floor', 'room']
    search_fields = ['name']
    list_filter = ['floor', 'room']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['fee_name', 'price']
    search_fields = ['fee_name']


class ResidentFeeAdmin(admin.ModelAdmin):
    list_display = ['payment_method', 'payment_proof', 'payment_date', 'status', 'amount', 'resident',
                    'fee']
    search_fields = ['payment_method', 'resident__user_info__first_name',
                     'resident__user_info__last_name']
    list_filter = ['payment_date', 'status', ]


class ReservationVehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'status']
    search_fields = ['vehicle_number']
    list_filter = ['status']


class ElectronicLockerItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'apartment']
    search_fields = ['name']
    list_filter = ['name']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['status', 'item_name', 'electronic_lock', 'received_date']
    search_fields = ['item_name']
    list_filter = ['status']


class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'data_expire', 'status']
    search_fields = ['title']
    list_filter = ['data_expire', 'status']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['survey', 'content']
    search_fields = ['content']
    list_filter = ['survey']


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'content_choice', 'letter']
    search_fields = ['content_choice']
    list_filter = ['question']


class ResponseAdmin(admin.ModelAdmin):
    list_display = ['survey', 'resident_id', 'submitted_at']
    search_fields = ['resident_id']
    list_filter = ['survey', 'submitted_at']


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['response', 'question', 'choice']
    search_fields = ['response__resident_id']
    list_filter = ['response', 'question', 'choice']


class ReportAdmin(admin.ModelAdmin):
    list_display = ['resident', 'title', 'content', 'status']
    search_fields = ['title', 'content']
    list_filter = ['status']


class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user_info', 'area']
    search_fields = ['user_info__first_name', 'user_info__last_name']


class User_Admin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'role', 'username', 'created']
    search_fields = ['username', 'id']
    list_filter = ['id', 'sex']

    forms = UserForm

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.password = make_password(form.cleaned_data['password'])
        obj.save()


admin_site.register(User, User_Admin)
admin_site.register(Resident, ResidentAdmin)
admin_site.register(Service, ServiceAdmin)
admin_site.register(Manager, ManagerAdmin)
admin_site.register(Apartment, ApartmentAdmin)
admin_site.register(ReservationVehicle, ReservationVehicleAdmin)
admin_site.register(ResidentFee, ResidentFeeAdmin)
admin_site.register(ElectronicLockerItem, ElectronicLockerItemAdmin)
admin_site.register(Item, ItemAdmin)
admin_site.register(Survey, SurveyAdmin)
admin_site.register(Question, QuestionAdmin)
admin_site.register(Choice, ChoiceAdmin)
admin_site.register(Response, ResponseAdmin)
admin_site.register(Report, ReportAdmin)
admin_site.register(Answer, AnswerAdmin)
