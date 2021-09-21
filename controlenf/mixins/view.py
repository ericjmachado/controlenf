import json

from rest_framework.generics import get_object_or_404


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


class CompanyContextView(object):
    lookup_company = "companies_pk"

    def get_serializer_context(self):
        from core import models
        context = super(CompanyContextView, self).get_serializer_context()
        context["company"] = get_object_or_404(models.Company, pk=self.kwargs.get("companies_pk"))
        return context
