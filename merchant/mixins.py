from django.shortcuts import redirect


class MerchantUserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("home")
        return super(MerchantUserMixin, self).dispatch(request, *args, **kwargs)