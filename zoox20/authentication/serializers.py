from rest_framework import serializers

from .models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""
    
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    
    # use for validate user
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        _email = validated_data['email']
        _password = validated_data['password']
        upper = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        lower = [i.lower() for i in upper]
        number = ["1","2","3","4","5","6","7","8","9","0"]
        def check(ls, s):
            for i in s:
                if i in ls:
                    return True
            return False
        uc = check(upper, _password)
        lc = check(lower, _password)
        nc = check(number, _password)
        ec = check(["@", "."], _email)
        
        if not ec:
            raise serializers.ValidationError(
            'Invalid email.'
            )
        
        if not (uc and lc and nc):
            raise serializers.ValidationError(
            'Password must have word in A-Z and a-z and number.'
            )

        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.IntegerField(default=0)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
      
        
        return {
            'email': user.email,
            'username': user.username,
            'id': user.id,
            'token': user.token,
        }
        
class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token','id')

        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        """Performs an update on a User."""
        
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        username = validated_data.pop('username', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if email is not None:
            raise serializers.ValidationError(
                'Can\'t change email !'
            )
            
        if username is not None:
            raise serializers.ValidationError(
                'Can\'t change username !'
            )

        if password is not None:
            _password = password
            upper = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
            lower = [i.lower() for i in upper]
            number = ["1","2","3","4","5","6","7","8","9","0"]
            def check(ls, s):
                for i in s:
                    if i in ls:
                        return True
                return False
            uc = check(upper, _password)
            lc = check(lower, _password)
            nc = check(number, _password)
            
            if not (uc and lc and nc):
                raise serializers.ValidationError(
                'Password must have word in A-Z and a-z and number.'
                )
            instance.set_password(password)

        instance.save()

        return instance