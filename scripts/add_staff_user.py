# execute in django_shell_plus

email_word="esc5222"
my_group = Group.objects.get(name='staff')
user = User.objects.get(email__contains=email_word)
user.is_staff=True
user.save()
my_group.user_set.add(user)