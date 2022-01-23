from django.db import models

from user.models import User


# Create your models here.
class MessageRoom(models.Model):
    # {board.name}에서 작성된 {user.nickname}의 댓글을 통해 시작된 쪽지입니다.
    # 글내용: ~~
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_room_user1', null = False)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_room_user2', null = False)
    user1_active = models.BooleanField(default=True)
    user2_active = models.BooleanField(default=True)

class Message(models.Model):
    # is_announce : "안내"이면 True
    # _active : 유저가 삭제 처리했을시 True, 아니면 False

    message_room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE, related_name='message', null = False)
    is_announce = models.BooleanField(default=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender', null = False)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_receiver', null = False)
    sender_active = models.BooleanField(default=True)
    receiver_active = models.BooleanField(default=True)
    text = models.CharField(max_length=128, null = False)
