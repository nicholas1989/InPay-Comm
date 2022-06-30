class IntiatePaymentView(generic.FormView):
    template_name = 'cart/initiate-payment.html'
    form_class = PaymentForm  
    
    def get_success_url(self):
        return reverse("cart:make-payment") 
   
    def form_valid(self, form): 
        payment = form.save(commit=False)
        order = get_or_set_order_session(self.request)
        payment.order = order
        payment.save()
        return super(IntiatePaymentView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(IntiatePaymentView, self).get_context_data(**kwargs)
        context["ETRANZACT_PUBLIC_KEY"] = settings.ETRANZACT_PUBLIC_KEY
        return context
    
    
class ThankYouView(generic.TemplateView):
    template_name = 'cart:thanks.html'
    
    
"""

class PaymentView(generic.FormView):
    template_name = 'cart/payment.html'
    form_class = PaymentForm                                                                                         
    

    def form_valid(self, form):
        return redirect("/")


    def get_context_data(self, **kwargs):
        user = self.request.user
        if not user.customer:
            credo_customer = customers.add(
                full_name=user.username, email="email", phone_number="phone_number", 
                billing_address1="billing_address2", billing_address2="billing_address2", 
                district="district", state="state"
            )
            user.customer = credo_customer["id"]
            user.customer.save()
            
        order = get_or_set_order_session(self.request)
            
        new_payment = payment.initiate_payment(
            amount = order.get_raw_total(), currency='NGN', 
            customer_name = user.customer, customer_email= user.customer.email, 
            customer_phone= user.customer.phone_number, trans_ref='iy67f64hvc62', 
            payment_options='CARD,BANK', redirect_url='https://github.com/BdVade/credo-python'
        )
        
        
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["ETRANZACT_PUBLIC_KEY"] = settings.ETRANZACT_PUBLIC_KEY
        context["ETRANZACT_SECRET_KEY"] = new_payment["ETRANZACT_SECRET_KEY"]
        return context 
        
    """








    class CustomerCreateView(generic.FormView):
    template_name = 'cart/customer.html'
    form_class = CustomerForm
    
    def get_success_url(self):
        return reverse("cart:payment") 
    
    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        customer = form.save(commit=False)

        if not customer:
            customer = customers.add(
                full_name=form.cleaned_data['customer_name'], 
                email=form.cleaned_data['email'],
                order = form.cleaned_data['order'],
                phone_number=form.cleaned_data['phone_number'],
                billing_address1=None, billing_address2=None, district=None,
                state=None,facebook_username=None,
                instagram_username=None, twitter_username=None
            )
            
            customer.order = order
        customer.save()
        return super(CustomerCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(CustomerCreateView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context
    
    
class PaymentView(generic.TemplateView):
    template_name = 'cart/payment.html'
    
    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["ETRANZACT_SECRET_KEY"] = settings.ETRANZACT_SECRET_KEY
        context["order"] = get_or_set_order_session(self.request)
        context['CALLBACK_URL'] = self.request.build_absolute_uri(reverse("cart:thanks"))
        return context
    
    
class VerifyPaymentView(generic.TemplateView):
    pass


class ThankYouView(generic.TemplateView):
    template_name = 'cart/thanks.html'





class IntiatePaymentView(generic.FormView):
    template_name = 'cart/initiate-payment.html'
    form_class = PaymentForm  
    
    def get_success_url(self):
        return reverse("cart:verify-payment") 
   
    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        payment = form.save(commit=False)
        payment.order = order
        payment.save()
        return super(IntiatePaymentView, self).form_valid(form)
    

    def get_context_data(self, **kwargs):
        context = super(IntiatePaymentView, self).get_context_data(**kwargs)
        context["ETRANZACT_SECRET_KEY"] = settings.ETRANZACT_PUBLIC_KEY
        context["order"] = get_or_set_order_session(self.request)
        return context
    


class VerifyPaymentView(generic.View):
    def get_verify_payment(self, *args, **kwargs):
        payment = get_object_or_404(Payment, id=kwargs['ref'])
        order = get_or_set_order_session(self.request)
        verified = payment.verify_payment()
        if verified:
            order.ordered = True
            messages.success("Verification Successful")
        else: 
            messages.error("Verification Failed.")
        return redirect('/')

'''

class VerifyPaymentView(generic.TemplateView):
    template_name = 'cart/verify-payment.html'
    
    
    def get_context_data(self, **kwargs):
        context = super(VerifyPaymentView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        return context
        
                        
    '''