import os
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basic.settings')
application = get_channel_layer()