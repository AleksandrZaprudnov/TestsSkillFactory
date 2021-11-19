from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post
from .forms import DateInputWidget


class NewsFilter(FilterSet):

    title_icon = CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок (сод.)')
    user_name_icon = CharFilter(field_name='author__users_id__name', lookup_expr='icontains', label='Имя польз. (сод.)')
    datetime_created__gte = DateFilter(field_name='datetime_created', lookup_expr='gte', label='Дата (>=)', widget=DateInputWidget)

    class Meta:

        model = Post

        fields = {
            # 'title': ['icontains'],
        }

