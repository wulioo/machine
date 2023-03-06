from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.system.models import SysMenu
from apps.user.models import SysRole
from apps.user.serializers import UserRolesSerializer, UserRolesAddSerializer, UserRolesPutSerializer

User = get_user_model()


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        user = User.objects.filter(username=request.data['username']).first()
        result = {
            "user": {
                "authorities": [
                    {
                        "authority": "admin"
                    }
                ],
                "dataScopes": [],
                "roles": [
                    "admin"
                ],
                "user": {
                    "avatarName": "avatar.jpeg",
                    "avatarPath": "/home/eladmin/avatar/avatar.jpeg",
                    "createTime": "2018-08-23 09:11:56",
                    "dept": {
                        "id": 2,
                        "name": "研发部"
                    },
                    "email": "admin@el-admin.vip",
                    "enabled": True,
                    "gender": "男",
                    "id": 1,
                    "isAdmin": True,
                    "jobs": [
                        {
                            "id": 11,
                            "name": "全栈开发"
                        }
                    ],
                    "nickName": "管理员",
                    "password": "$2a$10$Egp1/gvFlt7zhlXVfEFw4OfWQCGPw0ClmMcc6FjTnvXNRVf9zdMRa",
                    "phone": "18888888888",
                    "pwdResetTime": "2020-05-03 16:38:31",
                    "roles": [
                        {
                            "dataScope": "全部",
                            "id": 1,
                            "level": 1,
                            "name": "超级管理员"
                        }
                    ],
                    "updateBy": "admin",
                    "updateTime": "2020-09-05 10:43:31",
                    "username": "admin"
                }
            },
            "token": serializer.validated_data['access']
        }
        return Response(result)


class UserRolesList(viewsets.ModelViewSet):
    queryset = SysRole.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'content': serializer.data, 'totalElements': len(serializer.data)})

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserRolesSerializer
        elif self.action == 'create':
            return UserRolesAddSerializer
        elif self.action == "update":
            return UserRolesAddSerializer

    # def get_queryset(self):
    #     return SysRole.objects.all()
class UserRolesLevel(mixins.ListModelMixin, GenericViewSet):

    def list(self, request, *args, **kwargs):
        return Response({"level": 1})


class UserRolesMenu(mixins.CreateModelMixin, GenericViewSet):
    queryset = SysRole.objects.all()

    # serializer_class = UserRolesPutSerializer

    def create(self, request, *args, **kwargs):
        id = request.data['id']
        menus = [k['id'] for k in request.data['menus']]
        role = SysRole.objects.filter(id=id).first()
        role.menus.all()
        query_menus = SysMenu.objects.filter(menu_id__in=menus)
        for val in role.menus.all():
            role.menus.remove(val)

        for val in query_menus:
            role.menus.add(val)

        return Response({})
