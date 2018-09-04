from django.contrib import admin
from .models import User,Complaints,DepartmentDetails,DepartmentAdmins_list,ComplaintAssignment,Comments
#admin.site.register(User)
#admin.site.unregister(User)
#admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Complaints)
admin.site.register(DepartmentDetails)
admin.site.register(DepartmentAdmins_list)
admin.site.register(ComplaintAssignment)
admin.site.register(Comments)
# Register your models here.
