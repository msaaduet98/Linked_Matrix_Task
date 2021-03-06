from django.http import HttpResponseForbidden
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from django.conf import settings

CACHE_TTL = 60

class CacheIp(object):
    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        diamondUsers = {'127.0.0.1'}
        silverUsers = {}
        bronzeUsers = {}

        visitLimitDiamond = 9
        visitLimitSilver = 4
        visitLimitBronze = 1

        if request.META['REMOTE_ADDR'] in cache:
            cache.set('counter', cache.get('counter') + 1, timeout=60)        
        else:
            cache.set('counter',0,timeout=20)
            if request.META['REMOTE_ADDR'] in diamondUsers:
                cache.set(request.META['REMOTE_ADDR'], 'diamond', timeout=60)
            elif request.META['REMOTE_ADDR'] in silverUsers:
                cache.set(request.META['REMOTE_ADDR'], 'silver', timeout=60)
            elif request.META['REMOTE_ADDR'] in bronzeUsers:
                cache.set(request.META['REMOTE_ADDR'], 'bronze', timeout=60)

        
        if cache.get(request.META['REMOTE_ADDR']) == 'diamond':
            if cache.get('counter') > visitLimitDiamond:
                return HttpResponseForbidden('<h1>Forbidden Access!!!!!!!!You Have Visited more than TEN times in a minute')
            else:
                return response
        
        elif cache.get(request.META['REMOTE_ADDR']) == 'silver':
            if cache.get('counter') > visitLimitSilver:
                return HttpResponseForbidden('<h1>Forbidden Access!!!!!!!!You Have Visited more than FIVE times in a minute')
            else:
                return response

        elif cache.get(request.META['REMOTE_ADDR']) == 'bronze':
            if cache.get('counter') > visitLimitBronze:
                return HttpResponseForbidden('<h1>Forbidden Access!!!!!!!!You Have Visited more than TWO times in a minute')
            else:
                return response
        
        else:
            if cache.get('counter') > 0:
                return HttpResponseForbidden('<h1>Forbidden Access!!!!!!!!You Have Visited more than ONE times in a minute')
            else:
                return response

                
             

        
            
       