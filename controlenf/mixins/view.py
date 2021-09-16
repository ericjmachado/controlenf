import json


class ManageDataMixin(object):
    def manage_data(self, request, *args, **kwargs):
        return request.data

    def dispatch(self, request, *args, **kwargs):
        if request.method in ["POST", "PATCH", "PUT"]:
            body = request.body
            try:
                request._body = body.decode("utf-8").encode("utf-8")
            except Exception:
                request._body = body.decode("cp1252").encode("utf-8")
            buff = self.initialize_request(request, *args, **kwargs)
            request._body = json.dumps(self.manage_data(buff, *args, **kwargs)).encode(
                "utf-8"
            )
        return super(ManageDataMixin, self).dispatch(request, *args, **kwargs)
