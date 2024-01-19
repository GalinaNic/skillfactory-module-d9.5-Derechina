from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post


class PostFilter(FilterSet):
    created_date = DateFilter(
        field_name='post_time',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte',
        label='Поиск по дате',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'post_time': ['gt'],
        }
