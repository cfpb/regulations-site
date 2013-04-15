class TableOfContentsLayer(object):
    def __init__(self, layer):
        self.layer = layer

        if not settings.configured:
            settings.configure(TEMPLATE_DEBUG=False, 
                TEMPLATE_LOADERS=('django.template.loaders.filesystem.Loader',), 
                TEMPLATE_DIRS = ('templates/',))

    def apply_layer(self, text_index):
        
