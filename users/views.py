from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, status
from knox.models import AuthToken

from config.settings import *
from recipe.detect_ingrd.views_detect import *
from recipe.models import Ingredients
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
            Profile.objects.get(user_id=request.data["user_id"]))
        return Response(profile_list.data, status=200)


class ProfileCreateAPI(APIView):
    def post(self, request):
        disliked_List = Ingredients.objects.filter(name__in = request.data["disliked"])
        disliked_id_List=[]
        for ingrd in disliked_List:
            disliked_id_List.append(ingrd.id)
        request.data["disliked"] = disliked_id_List

        try:
            base64Image = request.data['profile_img']
            base64Image = encodebase64(base64Image)

            if not os.path.exists(PROFILE_ROOT):
                os.makedirs(PROFILE_ROOT)
            user_profile_path = os.path.join(PROFILE_ROOT, (str(request.data["user_id"])+".jpg"))
            user_profile_url = MEDIA_URL + 'profile/'+(str(request.data["user_id"])+".jpg")
            request.data['profile_img'] = FRONT_HOST+user_profile_url
            cv2.imwrite(user_profile_path, base64Image)
            serializers = ProfileSerializer(data=request.data)
        except:
            serializers = ProfileSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

class ProfileUpdateAPI(APIView):
    def post(self, request):
        user_id = request.data["user_id"]
        profile = Profile.objects.get(user_id = user_id)

        try:
            disliked_List = Ingredients.objects.filter(name__in = request.data["disliked"])
            disliked_id_List=[]
            for ingrd in disliked_List:
                disliked_id_List.append(ingrd.id)
            request.data["disliked"] = disliked_id_List
        except:
            user_id = request.data["user_id"]

        try:
            base64Image = request.data['profile_img']
            base64Image = encodebase64(base64Image)


            if not os.path.exists(PROFILE_ROOT):
                os.makedirs(PROFILE_ROOT)
            user_profile_path = os.path.join(PROFILE_ROOT, (str(user_id)+".jpg"))
            user_profile_url = MEDIA_URL + 'profile/'+(str(user_id)+".jpg")
            request.data['profile_img'] = FRONT_HOST+user_profile_url
            cv2.imwrite(user_profile_path, base64Image)

            serializers = ProfileSerializer(profile, data=request.data)
        except:
            serializers = ProfileSerializer(profile, data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)

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