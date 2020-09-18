from video_app.models import Video, UserProfile
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        field = '__all__'


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
def getuser(request):
    if not request.user.is_superuser():
        return Response({'msg': 'auth fail'}, status=status.HTTP_403_FORBIDDEN)
    user_list = User.objects.all()
    serializer = UserSerializer(user_list, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def modifyuser(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        user.profile.nickname = nickname
        user.set_password(password)
        user.save()
        user.profile.save()
        return Response({'msg': 'rename success'}, status=status.HTTP_201_CREATED)
    if request.method == 'GET':
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
def createuser(request):
    if not request.user.is_superuser:
        body = {"msg": "Auth fail"}
        return Response(body, status=status.HTTP_403_FORBIDDEN)
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    choice = request.POST.get('choices')
    print(username, password, email, choice)
    if len(User.objects.filter(username=username)) > 0:
        return Response({'msg': 'username already exist'}, status=status.HTTP_403_FORBIDDEN)
    elif password == "":
        return Response({'msg': 'the password is invalid'}, status=status.HTTP_403_FORBIDDEN)
    else:
        newuser = User(username=username, email=email)
        newuser.set_password(password)
        newuser.save()
        profile = UserProfile(choice=choice, belong_to=newuser)
        profile.save()

        return Response({'msg':'create user success'},status=status.HTTP_201_CREATED)



class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=1)

    class Meta:
        model = Video
        fields = '__all__'
        depth = 1  # 多往下渲染一层json（渲染owner）


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication,))
def video(request):
    print(request.user)
    print(request.auth)
    if request.method == 'GET':
        video_list = Video.objects.order_by('-id')
        if request.auth:
            if request.user == 'admin':
                serializer = VideoSerializer(video_list, many=True)
                body = {
                    'data': serializer.data,
                    'showMode': True
                }
                return Response(body)
            serializer = VideoSerializer(video_list, many=True)
            return Response(serializer.data)
        else:
            serializer = VideoSerializer(video_list[:5], many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        body = {
            'body': serializer.errors,
            'msg': '40001'
        }
        return Response(body, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@authentication_classes((TokenAuthentication,))
def video_card(request, id):
    video_card = Video.objects.get(id=id)
    if request.method == 'PUT':
        serializer = VideoSerializer(video_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if request.user.profile == video_card.owner:
            video_card.delete()
            return Response({'msg': 'A-OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'you cant do this'}, status=status.HTTP_403_FORBIDDEN)




