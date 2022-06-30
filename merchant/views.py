from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from .mixins import MerchantUserMixin
from django.views import generic
from cart.models import Order, Product
from .forms import ProductForm

# Create your views here.
class MerchantView(LoginRequiredMixin, MerchantUserMixin, generic.ListView):
    template_name = 'merchant/merchant.html'
    queryset = Order.objects.filter(ordered=True).order_by('-ordered_date')
    paginate_by = 20
    context_object_name = 'orders'
    
    
class ProductListView(LoginRequiredMixin, MerchantUserMixin, generic.ListView):
    template_name = 'merchant/product_list.html'
    queryset = Product.objects.all()
    paginate_by = 20
    context_object_name = 'products'
    
    
class ProductCreateView(LoginRequiredMixin, MerchantUserMixin, generic.CreateView):
    template_name = 'merchant/product_create.html'
    form_class = ProductForm
    
    def get_success_url(self):
        return reverse('merchant:product-list')
    
    def form_valid(self, form):
        form.save()
        return super(ProductCreateView, self).form_valid(form)
    
    
class ProductUpdateView(LoginRequiredMixin, MerchantUserMixin, generic.UpdateView):
    template_name = 'merchant/product_create.html'
    form_class = ProductForm
    queryset = Product.objects.all()
    
    def get_success_url(self):
        return reverse('merchant:product-list')
    
    def form_valid(self, form):
        form.save()
        return super(ProductCreateView, self).form_valid(form)
    
    
class ProductDeleteView(LoginRequiredMixin, MerchantUserMixin, generic.DeleteView):
    template_name = 'merchant/product_delete.html'
    queryset = Product.objects.all()
    
    def get_success_url(self):
        return reverse('merchant:product_list')
