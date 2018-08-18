import os
from channels.layers import get_channel_layer
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INT2018.settings')
django.setup()
application = get_channel_layer()