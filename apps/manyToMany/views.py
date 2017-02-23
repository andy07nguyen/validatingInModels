from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Pet

# Create your views here.
def index(request):
    try:

        user = User.objects.get(id=request.session['id'])
    except:
        print "User not working for whatever reason"
    newpet = Pet.objects.get(id=2)
    user.pets.add(newpet)
    userpets = user.pets.all()
    for pet in userpets:
        print pet.name, pet.habitat, pet.id


    return render(request, 'manytoMany/index.html')

def process(request):
    print "Made it to the process route!"
    user = User.objects.validate(request.POST)
    if user[0] == False: # we know that if user[0] is False, then user[1] is the errors array
        for i in user[1]:
            messages.error(request, i)
    else:
        # We know that user[0] is true, and if user[0] is true, then user[1] is the newuser we just created
        request.session['id'] = user[1].id
        # so now we know what should be in our session
        print "got the session", request.session['id']
        return redirect('/success')

    return redirect('/')

def success(request):
    if 'id' in request.session: # someone set a session with us and allowed to see the success page
        return render(request, 'manyToMany/success.html')
    else:
        messages.error(request, "You must log in to view the requested page")
        return redirect('/')


def processPet(request):
    newpet = Pet.objects.petValidate(request.POST)
    if newpet[0] == True:
        messages.info(request, "Your pet was created!")
    else:
        messages.info(request, "Your pet died in transit")
    return redirect('/success')
