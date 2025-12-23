import django_tables2 as tables
from django_tables2.utils import A # Alias for Accessor

from apps.user.models import User


class UserTable(tables.Table):

    class Meta:
        model = User
        exclude = (
            'password', 'is_staff', 'is_superuser',
            'date_joined', 'last_login')
        sequence = (
            'id', 'name', 'role',
            'occupation', 'village', 'taluka', 'district', 'state', 'pin_code',
            'mobile_number_1', 'mobile_number_2',
            'age', 'gender', 'is_active'
            )
        order_by = 'id'
        template_name = 'django_tables2/bootstrap5.html'
        attrs = {
            'id' : 'user_table_01',
            'class' : 'table table-striped',
            'thead' : {'class': 'thead-dark',}
        }


    id = tables.LinkColumn(
        'user_detail',
        args=[A('pk')],
        # attrs={
        #     'td': {
        #         'style': 'max-width:20px;'
        #     }
        # }
    )
    username = tables.LinkColumn(
        'user_detail',
        args=[A('pk')],
    )
    name = tables.LinkColumn(
        'user_detail',
        args=[A('pk')],
    )
    gender = tables.LinkColumn(
        visible=False
    )
    age = tables.LinkColumn(
        visible=False
    )
    username = tables.LinkColumn(
        visible=False
    )
    last_login = tables.LinkColumn(
        visible=False
    )
    date_joined = tables.LinkColumn(
        visible=False
    )
    taluka = tables.LinkColumn(
        visible=False
    )
    pin_code = tables.LinkColumn(
        visible=False
    )
    mobile_number_2 = tables.LinkColumn(
        visible=False
    )
    profile_picture = tables.LinkColumn(
        visible=False
    )

