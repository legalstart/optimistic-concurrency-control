import inspect

from rest_framework import status
from rest_framework.response import Response


def optimistic_concurrency_control(compute_etag_func):
    """
    Class decorator for Django and DRF views to setup optimistic concurrency
    control for some HTTP methods.
    Reference:
    https://blog.4psa.com/rest-best-practices-managing-concurrent-updates/

    Example usage:
        @optimistic_concurrency_control({'PUT', 'PATCH'}, compute_etag_func)

    Where `compute_etag_func` is a function with the following signature:
        viewInstance, request -> str

    This function should implement the etag computation for the underlying
    resource.

    The flow is the following:
        - if the incoming request doesn't have a If-Match header, then a 403
        response is sent.
        - if the incoming request has a if-Match header, then we compare its
        value with the result if compute_etag_func. If it doesn't match, the
        a 412 response is sent. If it matches, then the view is exectued as
        usual.

    Notes:
        * This implementation doesn't take the If-UnModified-Since header into
        account
        * the request parameter in the compute_etag_func can be used to
        identify the underlying resource, if viewInstance is not sufficient to
        do so
        * It doesn't make sense to use this decorator on safe methods (such as
        GET or HEAD) which don't modify resources.
    :param compute_etag_func: (func) :: viewInstance -> str
    :return: (cls) A decorated view with opitmistic concurrency control
    """
    def cls_decorator(cls):
        get_meth = cls.get
        cls.get = get_decorator(get_meth)

        put_meth = cls.put
        cls.put = put_decorator(put_meth)
        return cls

    def get_decorator(meth):
        def g(self, request, *args, **kwargs):
            resp = meth(self, request, *args, **kwargs)
            resp['etag'] = compute_etag_func(self)
            return resp
        return g

    def put_decorator(meth):
        def g(self, request, *args, **kwargs):
            if 'HTTP_IF_MATCH' not in request.META:
                return Response(status=status.HTTP_403_FORBIDDEN)
            etag = request.META['HTTP_IF_MATCH']
            if etag != compute_etag_func(self):
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)
            resp = meth(self, request, *args, **kwargs)

            resp['etag'] = compute_etag_func(self)
            return resp
        return g

    return cls_decorator
