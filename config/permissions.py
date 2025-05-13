from rest_framework import permissions

class IsAuthenticatedAndDesktop(permissions.BasePermission):
    """ Faqat autentifikatsiya qilingan va "Desktop" turidagi qurilmadan kirgan foydalanuvchilarga ruxsat beradi"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.META.get('HTTP_USER_AGENT', '').lower().find('desktop') != -1

class IsAdminOrReadOnly(permissions.BasePermission):
    """ Administratorlar uchun to'liq ruxsat, qolganlar uchun faqat o'qish uchun ruxsat. Bu ozida bor lekin permissionsni"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
