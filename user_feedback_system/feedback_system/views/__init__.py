from .auth_views import (
    register_view,
    change_password_view
)
from .dashboard import dashboard_view
from .feedback_views import (
    submit_feedback,
    feedback_list_view,
    export_feedback_csv
)
from .home import home_redirect_view
__all__=[
    register_view,
    dashboard_view,
    submit_feedback,
    feedback_list_view,
    change_password_view,
    export_feedback_csv,
    home_redirect_view
]