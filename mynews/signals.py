import django.dispatch


comments_done = django.dispatch.Signal(providing_args=["publisher_text", "title_text", "pub_date"])

news_done = django.dispatch.Signal(providing_args=["toppings", "size"])