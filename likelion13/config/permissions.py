from rest_framework.permissions import BasePermission,IsAuthenticatedOrReadOnly
from rest_framework.permissions import SAFE_METHODS
from django.utils import timezone

class TimePossible(IsAuthenticatedOrReadOnly):
    def has_permission(self,request,view):
        # 부모 먼저 검사
        if not super().has_permission(request,view):
            return False
        # 시간 검사
        current_time = timezone.localtime(timezone.now())
        if 0 <= current_time.hour < 6:
            print("0시부터 6시 까지는 게시판을 이용하실 수 없습니다")
            return False
        return True
    
    
class WriterPossible(TimePossible):
    def has_object_permission(self,request,view,obj):
        # 읽기 권한은 모두에게 허용, 작성자만 수정 권한 부여
        if request.method in SAFE_METHODS:
            return True
        print(f"{obj.user} : {request.user}")
        return obj.user == request.user #처음에 모르고 obj.owner 썼는데 post에는 user밖에 없으니까 500 에러 나겠지