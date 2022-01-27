from firebase_admin import messaging

def get_content(type, obj):
    if type == "new_comment":
        title = "새로운 댓글이 달렸어요"
        body = obj.text 
    elif type == "new_subcomment":
        title = "새로운 대댓글이 달렸어요"
        body = obj.text
    elif type =="new_message":
        title = "새로운 쪽지가 왔어요"
        body = obj.text
    elif type == "test":
        title = "test입니다."
        body = f"{obj.name}에게 알림보냄."

    return title, body

def send_push(type, obj, token):
    registration_token = token # 클라이언트의 FCM 토큰
    title, body = get_content(type, obj)

    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=registration_token,
    )

    response = messaging.send(message)
