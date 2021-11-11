from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, status
from knox.models import AuthToken
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, ProfileSerializer, ProfileUpdateSerializer
from .models import Profile
from django.utils.datastructures import MultiValueDictKeyError


class UserView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('profile_id') is None:
            profile_serializer = ProfileSerializer(
                Profile.objects.all(), many=True)
            # user 전체 리스트 get
            return Response(profile_serializer.data, status=200)
        else:
            profile_id = kwargs.get('profile_id')
            profile_serializer = ProfileSerializer(
                get_object_or_404(Profile, id=profile_id))
            return Response(profile_serializer.data, status=200)
            # user 개인 정보 get


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response(
            {
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LogoutAPI(APIView):
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ProfileAPI(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        profile_list = ProfileSerializer(
            Profile.objects.filter(user_id=request.data["user_id"]), many=True)
        return Response(profile_list.data, status=200)


class ProfileCreateAPI(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileUpdateAPI(generics.UpdateAPIView):
    lookup_field = 'user_id'
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer


'''
class ProfileUpdateAPI(generics.UpdateAPIView):
    serializer_class = Profile2Serializer

    def post(self, request, **kwargs):
        try:
            profile_id = kwargs.get('profile_id')
            profile = Profile.objects.get(id=profile_id)
            profile.nick_name = request.data['nick_name']
            profile.disliked = request.data['disliked']
            #image = request.FILES['profileImage']
            #profile.profile_image = image
            profile.save()
        except MultiValueDictKeyError:
            #profile.save()
            profile = None
        return Response(status=200)

'''