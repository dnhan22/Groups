from django.db import models

# Create your models here.
import re
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        usersWithEmail = User.objects.filter(email = postData['email'])

        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) < 2:
            errors["fname"] = "First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "Last name should be at least 2 characters"
        if len(postData['email']) < 1:
            errors["emailBlank"] = "Email is required"
        if len(usersWithEmail) > 0:
            errors['emailTaken'] = "Email is taken already!"
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['emailPattern'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['passwordlength'] = "Password must be at least 8 characters"
        if postData['confirmPassword'] != postData['password']:
            errors['pwMatch'] = "Password and confirm password must match"
        print(errors)
        return errors
    
    def login_validator(self, postData):
        usersWithEmail = User.objects.filter(email = postData['email'])
        
        print ("printing usersWithEmail below:")
        print (usersWithEmail)
        print ("printing a user")
        errors = {}
        if len(postData['email'])<1:
            errors['emailrequired'] = "You must enter an email"
        if len(postData['password'])<1:
            errors['passwordrequired'] = "You must enter a password"
        if len(usersWithEmail)<1:
            errors['emailNotFound'] = "This email is not registered"
        else:
            user = usersWithEmail[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("password match")
                
            else:
                print("failed password")
                errors['passwordInvalid'] = "The password is incorrect"
        print(errors)
        return errors

class OrganizationManager(models.Manager):
    def org_validator(self, postData):
        errors = {}
        if len(postData['orgname'])<1:
            errors['orgname'] = "You must enter a organization name"
        if len(postData['desc'])<1:
            errors['desc'] = "You must enter a description"
        return errors



class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Organization(models.Model):
    organization = models.CharField(max_length=255)
    description = models.TextField (null=True)
    creator = models.ForeignKey(User, related_name="org_created", on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField (User, related_name="org_joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = OrganizationManager()
