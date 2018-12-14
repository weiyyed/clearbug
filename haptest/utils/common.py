
class Parse_url():

    func=None
    @classmethod
    def parse_url(cls,request,**kwargs):
        #解析
        app=kwargs.pop('app')
        cls.func=kwargs.pop('func')
        id=kwargs.pop('id',None)
        app=__import__('%s.views'%app)
        views=getattr(app,'views')
        views_func=getattr(views,'func')
        return views_func(request,id) if id else views_func(request)

