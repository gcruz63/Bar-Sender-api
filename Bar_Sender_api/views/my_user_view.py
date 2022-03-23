"""View module for handling requests about user"""
from Bar_Sender_api.models import MyUser
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class MyUserView(ViewSet):
    """Trove user view"""

    def list(self, request):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user
        """

        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user
        """

        try:
            myUser = MyUser.objects.get(pk=pk)
            serializer = MyUserSerializer(myUser)
            return Response(serializer.data)
        except MyUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=False)
    def current(self, request):
        """Only get actors back that are currently active on a book"""

        my_user = MyUser.objects.get(user=request.auth.user)
        serializer = MyUserSerializer(my_user)
        return Response(serializer.data)
    # @action(methods=['put'], detail=True)
    # def author(self, request, pk):
    #     """Put request to is_staff"""

    #     user = User.objects.get(pk=pk)
    #     admin_list = User.objects.filter(is_staff=True, is_active=True)
    #     serialized = UserSerializer(admin_list, many=True)

    #     if len(serialized.data) <= 1 and user.is_staff is True:
    #         return Response({'message': 'Cannot be changed- this is the only active admin remaining'}, status=status.HTTP_409_CONFLICT)
    #     else:
    #         user.is_staff = False
    #         user.save()
    #         return Response({'message': 'User is now an author'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def activate(self, request, pk):
        """Put request to active"""

        user = MyUser.objects.get(pk=pk)
        user.active = True
        user.save()

        return Response({'message': 'User has been activated'}, status=status.HTTP_204_NO_CONTENT)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """
    class Meta:
        model = MyUser
        depth = 1
        fields = ['id', 'user', 'account_type']


class MyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for user types
    """

    user = UserSerializer(many=False)

    class Meta:
        model = MyUser
        fields = ['id', 'bio', 'user', 'account_type']
