from rest_framework import permissions
from .models import *

class InviteUserPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_invite_user == True:
            return True
        return False
    
class KickUserPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_kick_user == True:
            return True
        return False
    
class EditUserPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        curr_project = Project.objects.get(pk = request.data["project"])

        if curr_project.created_by == request.user:
            return True

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_edit_user_permissions == True:
            return True
        return False
    
class CreateTaskPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_create_task == True:
            return True
        return False
    
class DeleteTaskPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_delete_task == True:
            return True
        return False
    
class EditTaskPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_edit_task == True:
            return True
        return False
    
class CheckoutTaskPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        if request.data["status"] != "F":
            return True 

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_checkout_task == True:
            return True
        return False
    
class SetUserPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_set_user_to_task == True:
            return True
        return False
    
class DeleteProjectPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_delete_project == True:
            return True
        return False
    
class EditProjectPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_edit_project == True:
            return True
        return False
    
class FinishProjectPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):

        item = Permissions.objects.get(user = request.user, project = request.data["project"])
        if item.can_finish_project == True:
            return True
        return False

    