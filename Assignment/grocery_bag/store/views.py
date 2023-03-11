from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView,DeleteView
# Create your views here.
from django.shortcuts import render, redirect
from store.forms.authforms import CustomerCreationForm,CustomerLoginForm
from django.contrib.auth import authenticate, login as loginUser, logout as logoutUser
# from .models import Post, User
from django.contrib import messages
from .models import Item
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    data = Item.objects.all()
    user = request.user
    context = {'data':data,'user':user}
    return render(request, 'store/home.html', context)


class ItemListView(ListView):
    model = Item
   
    def get_queryset(self):
        si = self.request.GET.get("si")
        print(si)
        if si == None:
            si = ""
        print(si)
        return Item.objects.filter(date = si).order_by("-id")

class ItemCreateView(CreateView):
    model = Item
    fields = ['name','quantity','status','date']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            super().post(self, request, *args, **kwargs)
            messages.success(request, "item created successfully")
            return redirect('/youritem')
        else:
            messages.error(request, 'please enter the date in "YYYY-MM-DD" format')
            return render(request, 'store/item_form.html', {'form':form})

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return redirect('/youritem')


    
class ItemUpdateView(UpdateView):
    model = Item
    # fields = '__all__'
    fields =  ['name','quantity','status','date']

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            super().post(self, request, *args, **kwargs)
            messages.success(request, "item updated successfully")
            return redirect('/youritem')
        else:
            messages.error(request, 'please enter the date in "YYYY-MM-DD" format')
            return render(request, 'store/item_form.html', {'form':form})

    

# class ItemDeleteView(DeleteView):
#     model = Item

def deleteView(request, pk):
    obj = Item.objects.filter(id = pk)
    obj.delete()
    messages.success(request, "Item deleted successfully")
    items = Item.objects.filter(user= request.user)
    context = {'data':items}
    return render(request, 'store/userlist.html',context)

def searchView(request):
    si = request.GET.get('si')
    if si == None:
        si = ""
        data = Item.objects.all()
        context = {'data':data,"si":si}
        return render(request, 'store/search.html', context)
    else:
        try:
            data = Item.objects.filter(date = si).order_by("-id")
            context = {'data':data,'si':si}
            return render(request, 'store/search.html', context)
        except:
            data = ''
            context = {'data':data,'si':si}
            return render(request, 'store/search.html',context )


def your_item(request):
    items = Item.objects.filter(user= request.user)
    context = {'data':items}
    return render(request, 'store/userlist.html', context)
            



def signup(request):
    ''' create user '''
    if request.method == "GET":
        form = CustomerCreationForm()
        context = {
            'form':form
        }
        return render(request, 'store/signup.html',context = context)
    else:
        form = CustomerCreationForm(request.POST) 
        
        if form.is_valid():
            user1 = form.cleaned_data['Username']
            present_user = User.objects.filter(username=user1)
            if present_user:
                messages.error(request, "this username is already exist")
                return render(request, 'store/signup.html',{'form':form})
            user = form.save()
            user.email = user.username
            user.username = form.cleaned_data['Username']
            messages.success(request,"Your account is created")
            return redirect('/login')

           
        context = {
            'form':form
            }
        return render(request, 'store/signup.html',context = context)


def login(request):
    ''' Login User '''
    if request.method == 'GET':
        form = CustomerLoginForm()
        return render(request, 'store/login.html',context = {'form':form})
    else:
        form = CustomerLoginForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password= password)
            if user:
                loginUser(request, user)   # it will save user in session
                messages.success(request,"Login sucessfull")
                return redirect('homepage')
            else:
                pass
        else:
            return render(request, 'store/login.html',context = {'form':form})
        


def logout(request):
    # request.session.clear() # this will clear the session or logout we can also use logout fn for this
    logoutUser(request)
    messages.success(request,"Logout Successfull")
    return redirect('/login')